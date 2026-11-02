# AI Billing Dispute Intake

A portfolio project that turns unstructured billing-dispute messages into structured records, validates them against synthetic invoices, and prepares a queue for human review.

## Live Project

**[Open the Live Interactive Demo](https://angel-guevara-ai-billing.streamlit.app/)**

The live Streamlit application lets reviewers test the workflow visually without downloading or running the repository.

## Business Problem

Billing disputes often arrive as inconsistent messages. An analyst must identify the invoice, understand the disputed charge, check the billing records, and determine what information is missing.

Automating extraction can help organize intake, but incorrect invoice numbers, unsupported amounts, or misunderstood requests can create additional work. This project demonstrates where AI can assist and where deterministic validation and human judgment remain necessary.

## Workflow

1. Receive a synthetic customer message.
2. Extract a structured dispute record.
3. Validate fields and data types.
4. Compare invoice details against a synthetic invoice register.
5. Flag missing information, mismatches, and unsupported claims.
6. Produce an intake summary and review route.
7. Require human review before any financial action.

The portfolio app replays a recorded AI extraction for reproducibility. It does not make live AI calls, approve credits, modify invoices, or contact customers.

## Design Principles

- Extract only information supported by the source message.
- Represent missing or ambiguous information explicitly.
- Preserve source excerpts so reviewers can trace extracted claims.
- Validate AI output with deterministic rules.
- Check invoice references against the invoice register.
- Treat embedded instructions in customer messages as untrusted source data.
- Require human review before financial action.

## Demonstrated Results

The six-message synthetic sample includes standard-review and exception-review cases involving missing information, invoices not found, unsupported amounts, and ambiguous charges.

A deliberate validation test changed a disputed amount while preserving the original evidence. The validator correctly rejected the altered extraction because the amount was not supported by its evidence.

These results describe the included synthetic sample only and are not claims of general model accuracy or production performance.

## Repository Contents

- `data/dispute_messages.json` — synthetic customer messages
- `data/invoices.csv` — synthetic invoice register
- `prompts/extract_dispute.md` — extraction prompt and output specification
- `outputs/model_response_v1.json` — recorded model response
- `validate.py` — deterministic validation and reconciliation logic
- `outputs/review_queue.json` — generated review queue
- `docs/run-notes.md` — provenance and limitations
- `docs/evaluation.md` — extraction evaluation and business exception analysis

## Run Locally

Requires Python 3. No external API credentials are needed.

```bash
python3 validate.py
```

## Validation Boundaries

The validator checks required fields, supported data types, message coverage, issue categories, decimal formatting, source evidence, invoice existence, customer matching, currency matching, and disputed amounts that exceed invoice totals.

An excerpt appearing in a message does not prove the allegation is correct. Human review must assess context and determine whether a billing error actually occurred.

## Data and Privacy

All customer names, messages, invoices, and amounts are fictional. No employer records, customer information, credentials, or API keys are used.

## Author

Angel Guevara
