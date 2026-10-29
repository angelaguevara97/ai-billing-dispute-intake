"""Validate recorded AI extraction and prepare a human review queue."""

import csv
import json
import re
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = {
    "message_id", "customer_name", "invoice_id", "disputed_amount",
    "currency", "issue_category", "evidence", "review_notes",
}
EVIDENCE_FIELDS = {
    "customer_name", "invoice_id", "disputed_amount",
    "currency", "issue_category",
}
CATEGORIES = {
    "suspected_duplicate", "rental_duration", "unrecognized_charge",
    "ambiguous_charge", "unspecified",
}


def load_json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def index_unique(records, field):
    """Reject duplicate identifiers instead of silently overwriting them."""
    result = {}
    for record in records:
        identifier = record[field]
        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError(f"Invalid identifier: {field}")
        if identifier in result:
            raise ValueError(f"Duplicate identifier: {identifier}")
        result[identifier] = record
    return result


def check_structure(record, source_text):
    """Check format and traceability, not the meaning of the claim."""
    if set(record) != FIELDS:
        raise ValueError("Unexpected or missing output fields.")

    for field in ("customer_name", "invoice_id", "disputed_amount", "currency"):
        value = record[field]
        if value is not None and (
            not isinstance(value, str) or not value.strip()
        ):
            raise ValueError(f"{field} must be a nonempty string or null.")

    if record["issue_category"] not in CATEGORIES:
        raise ValueError("Unsupported issue category.")

    notes = record["review_notes"]
    if not isinstance(notes, list) or not all(
        isinstance(note, str) and note.strip() for note in notes
    ):
        raise ValueError("review_notes must be an array of nonempty strings.")

    evidence = record["evidence"]
    if not isinstance(evidence, dict) or set(evidence) != EVIDENCE_FIELDS:
        raise ValueError("Invalid evidence fields.")

    for field in EVIDENCE_FIELDS:
        excerpt = evidence[field]
        if record[field] is None:
            if excerpt is not None:
                raise ValueError(f"Null {field} requires null evidence.")
        elif (
            not isinstance(excerpt, str)
            or not excerpt.strip()
            or excerpt not in source_text
        ):
            raise ValueError(f"Missing or nonverbatim evidence for {field}.")

    for field in ("customer_name", "invoice_id", "currency"):
        if record[field] is not None and record[field] not in evidence[field]:
            raise ValueError(f"{field} is not present in its evidence.")

    amount = record["disputed_amount"]
    if amount is not None:
        if not re.fullmatch(r"(0|[1-9][0-9]*)\.[0-9]{2}", amount):
            raise ValueError("Amount must be a nonnegative decimal string.")

        # Check numeric support in the excerpt; meaning still needs review.
        numbers = re.findall(
            r"(?<![\w.])[0-9]+(?:\.[0-9]{1,2})?(?![\w.])",
            evidence["disputed_amount"],
        )
        if Decimal(amount) not in [Decimal(number) for number in numbers]:
            raise ValueError("Amount is not supported by its evidence.")

    if record["currency"] not in (None, "USD"):
        raise ValueError("Unsupported currency.")


def invoice_checks(record, invoices):
    """Identify intake exceptions without deciding dispute validity."""
    flags = []

    for field in ("customer_name", "invoice_id", "disputed_amount", "currency"):
        if record[field] is None:
            flags.append(f"missing_{field}")

    invoice = invoices.get(record["invoice_id"])
    if record["invoice_id"] is not None and invoice is None:
        flags.append("invoice_not_found")

    if invoice is not None:
        if (
            record["customer_name"] is not None
            and record["customer_name"].strip().casefold()
            != invoice["customer_name"].strip().casefold()
        ):
            flags.append("customer_mismatch")

        if record["currency"] is not None:
            if record["currency"] != invoice["currency"]:
                flags.append("currency_mismatch")
            elif record["disputed_amount"] is not None:
                if Decimal(record["disputed_amount"]) > Decimal(
                    invoice["invoice_total"]
                ):
                    flags.append("amount_exceeds_invoice_total")

    if record["issue_category"] == "ambiguous_charge":
        flags.append("ambiguous_charge")
    if record["issue_category"] == "unspecified":
        flags.append("unspecified_issue")

    return flags


def main():
    messages = load_json("data/dispute_messages.json")
    responses = load_json("outputs/model_response_v1.json")
    if not isinstance(messages, list) or not isinstance(responses, list):
        raise ValueError("Messages and responses must be JSON arrays.")

    sources = index_unique(messages, "message_id")
    extracted = index_unique(responses, "message_id")

    if set(sources) != set(extracted):
        raise ValueError("Response IDs do not match source message IDs.")

    with (ROOT / "data/invoices.csv").open(
        newline="", encoding="utf-8"
    ) as file:
        invoices = index_unique(list(csv.DictReader(file)), "invoice_id")

    queue = []
    for message_id, source in sources.items():
        record = extracted[message_id]
        try:
            check_structure(record, source["text"])
        except ValueError as error:
            raise ValueError(f"{message_id}: {error}") from error

        flags = invoice_checks(record, invoices)
        queue.append({
            "message_id": message_id,
            "invoice_id": record["invoice_id"],
            "disputed_amount": record["disputed_amount"],
            "currency": record["currency"],
            "intake_route": (
                "exception_review" if flags else "standard_review"
            ),
            "flags": flags,
            "model_review_notes": record["review_notes"],
            "human_review_required": True,
        })

    # Write only after every response passes structural validation.
    destination = ROOT / "outputs/review_queue.json"
    destination.write_text(
        json.dumps(queue, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Validated recorded responses: {len(queue)}")
    for case in queue:
        reasons = ", ".join(case["flags"]) or "no intake exceptions"
        print(f"{case['message_id']}: {case['intake_route']} | {reasons}")
    print("All cases require human review. No financial action authorized.")
    print(f"Review queue saved to: {destination}")


if __name__ == "__main__":
    main()
