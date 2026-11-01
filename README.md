# AI Billing Dispute Intake

A personal portfolio project that turns unstructured billing-dispute messages into structured records, validates them against synthetic invoices, and prepares a queue for human review.

**Status:** Working portfolio demonstration. Includes a recorded manual ChatGPT extraction, a Python validator, and a generated human review queue. The local script replays the recorded response; it does not make live AI calls.

## Business Problem

Billing disputes often arrive as inconsistent messages. An analyst must identify the invoice, understand the disputed charge, check the billing records, and determine what information is missing.

Automating extraction can help organize intake, but incorrect invoice numbers, unsupported amounts, or misunderstood requests can create additional work.

This project explores where AI can assist and where explicit validation and human judgment are necessary.

## Intended Workflow

1. Receive a synthetic customer message.
2. Use an AI model to extract a structured dispute record.
3. Validate the output's fields and data types.
4. Compare invoice details against a synthetic invoice register.
5. Flag missing information, mismatches, and unsupported claims.
6. Produce an intake summary and review queue.

The workflow prepares cases for review. It does not approve credits, change invoices, or contact customers.

## Example

**Synthetic input:**

> Hi, invoice INV-1001 for Harbor Demo Logistics includes a $150 USD storage charge we think was added twice. Please check it.

**Intended extraction:**

- Customer: Harbor Demo Logistics
- Invoice: INV-1001
- Disputed amount: USD 150.00
- Issue category: suspected duplicate charge
- Evidence: the customer's stated concern
- Resolution: pending analyst review

A customer's statement is an allegation to investigate, not proof that a billing error occurred.

## Design Principles

- Extract only information supported by the message.
- Represent missing or ambiguous information explicitly.
- Preserve source excerpts so reviewers can trace extracted claims.
- Validate AI output with deterministic rules.
- Check invoice references against the invoice register.
- Treat message content as data, including any instructions embedded within it.
- Require human review before any financial action.

## Planned Deliverables

- Synthetic dispute messages and invoice register
- Extraction prompt and structured-output specification
- Recorded model outputs with documented provenance
- Python validation and reconciliation script
- Review queue with clear exception reasons
- Evaluation against manually defined expected fields
- Run instructions, findings, and limitations

Recorded-output replay will be distinguished from live model execution. Any example fixtures will be labeled as fixtures rather than presented as measured model performance.

## My Role

I am defining the business requirements, extraction rules, validation logic, exception handling, and evaluation approach, using AI-assisted development to help implement the project.

The project builds on my professional experience with billing reconciliation, data quality, and operational investigations. It is a personal demonstration, not a system deployed at a former employer.

## Data and Privacy

All customer names, messages, invoices, and amounts in this repository are fictional.

No employer records, customer information, credentials, or API keys belong in this repository.

## Success Criteria

The completed demonstration should let a reviewer:

- Trace extracted fields back to the original message
- Reproduce validation and invoice checks
- Understand why each case needs review
- Inspect extraction errors and limitations
- Distinguish implemented behavior from future improvements

No accuracy, time-saving, or financial-impact claims will be made without supporting measurements.
## Run the Demonstration

Requires Python 3. No external packages or API credentials are needed.

Download and extract this repository, open a terminal in the extracted folder, and run:

```bash
python3 validate.py
```

The script reads the recorded extraction, checks it against the source messages and invoice register, and writes `outputs/review_queue.json`.

A successful run overwrites the generated review queue. It does not modify the source messages, invoice register, or recorded model response.

## Observed Results

The six-message sample was run successfully on macOS.

| Message | Route | Intake exceptions |
|---|---|---|
| MSG-001 | Standard review | None detected |
| MSG-002 | Standard review | None detected |
| MSG-003 | Exception review | Missing invoice, amount, and currency; unspecified issue |
| MSG-004 | Exception review | Invoice not found |
| MSG-005 | Exception review | Disputed amount exceeds invoice total |
| MSG-006 | Exception review | Missing disputed amount; ambiguous charge |

All six recorded responses passed the implemented structural and evidence checks. Two cases entered standard review and four entered exception review.

These counts describe this sample run. They are not a measurement of general extraction accuracy.

Every case requires human review. Standard review does not mean the dispute is valid or a credit is approved.

## Inspect the Evidence

- [Synthetic customer messages](data/dispute_messages.json)
- [Synthetic invoice register](data/invoices.csv)
- [Extraction prompt and output specification](prompts/extract_dispute.md)
- [Recorded model response](outputs/model_response_v1.json)
- [Validator](validate.py)
- [Generated review queue](outputs/review_queue.json)
- [Run provenance and limitations](docs/run-notes.md)
- [Extraction evaluation and business exception analysis](docs/evaluation.md)

## Validation Boundaries

The validator checks:

- Required output fields and supported data types
- Unique message IDs and complete source-message coverage
- Allowed issue categories and decimal amount formatting
- Whether evidence excerpts appear verbatim in the source
- Whether extracted names, invoice references, currencies, and amounts appear in their evidence
- Invoice existence, customer matching, currency matching, and amounts exceeding invoice totals

An excerpt appearing in a message does not prove that it supports the extracted meaning. Human review must assess context, ambiguity, and whether the allegation is correct.

The invoice register contains totals, not line items or return records. It cannot establish whether a storage charge was duplicated or a rental duration was incorrect.

## Current Limitations

- Extraction was performed manually in ChatGPT; API automation is not implemented.
- The recorded response is replayed locally for reproducible validation.
- Six synthetic messages are insufficient to establish production reliability.
- Category meanings and review-note completeness are not automatically verified.
- One embedded-instruction example does not establish broad resistance to prompt injection.
- One deliberate validation test changed MSG-001's extracted amount to "999.00" while preserving its original $150 USD evidence. The validator rejected it with "Amount is not supported by its evidence." Other malformed-output scenarios remain untested.
- No measured time savings, financial impact, or production deployment is claimed.
