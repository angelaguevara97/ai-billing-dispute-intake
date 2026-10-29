# ai-billing-dispute-intake
AI-assisted billing dispute extraction with structured outputs, invoice validation, and human review using synthetic data.
# AI Billing Dispute Intake

A personal portfolio project that turns unstructured billing-dispute messages into structured records, validates them against synthetic invoices, and prepares a queue for human review.

**Status:** Under construction. This README defines the intended workflow; implementation and evaluation results will be added as they are completed.

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

> Hi, invoice INV-1001 for Harbor Demo Logistics includes a $150 storage charge we think was added twice. Please check it.

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
