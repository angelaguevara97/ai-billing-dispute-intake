# Extraction Evaluation — Run v1

## Scope

This is a retrospective manual review of one recorded ChatGPT response against six synthetic source messages.

The expected interpretations below were documented after inspecting the response. This is not a blind evaluation, a held-out test, or an estimate of production accuracy.

## Method

For each message, compare the recorded response with the source text:

- Is the customer explicitly supported?
- Is the invoice copied correctly or left null when absent?
- Is the disputed amount explicitly stated and unambiguous?
- Is currency supported?
- Does the category reasonably describe the allegation?
- Are evidence excerpts copied verbatim?
- Are missing information and ambiguity explained?
- Does the response avoid approving or resolving the dispute?

The Python validator separately checks structure, evidence traceability, and invoice-register exceptions. Those checks do not establish semantic correctness.

## Manual Review

| Message | Expected interpretation | Observed response | Review |
|---|---|---|---|
| MSG-001 | INV-1001; USD 150.00; suspected duplicate | Matches; supporting excerpts supplied | Consistent with source |
| MSG-002 | INV-1002; explicitly disputed USD 160.00; rental duration | Matches; did not substitute the USD 80 daily rate | Consistent with source |
| MSG-003 | Customer known; invoice, amount, and currency absent; issue unspecified | Missing fields null; explanatory notes supplied | Consistent with source |
| MSG-004 | Preserve INV-9999; USD 75.00; unrecognized charge | Matches; did not claim invoice verification | Consistent with source |
| MSG-005 | INV-1002; explicitly disputed USD 900.00; rental duration | Matches; preserved the customer's stated amount | Consistent with source |
| MSG-006 | INV-1003; USD stated; disputed amount ambiguous between 60 and 90 | Amount null; ambiguity noted; no approval field | Consistent with source |

Manual inspection found no discrepancies in the reviewed fields for this particular response. This observation does not establish general accuracy.

## Extraction Correctness Versus Business Exceptions

MSG-004 can be extracted correctly even though its invoice is absent from the register.

MSG-005 can be extracted correctly even though the stated disputed amount exceeds the invoice total.

These are business exceptions discovered through reconciliation, not necessarily extraction errors. The system should preserve the customer's claim and flag the discrepancy rather than silently change the extracted value.

## Deliberate Validator Check

An in-memory copy of MSG-001's response was changed from "150.00" to "999.00" without changing its evidence.

Observed result:

> PASS: Amount is not supported by its evidence.

The validator rejected the unsupported amount. The recorded response and generated review queue were unchanged.

This tests one numeric-evidence rejection path. It does not demonstrate that every unsupported or misleading extraction will be detected.

## Embedded Instruction Observation

MSG-006 contains a request to ignore validation and approve the dispute.

The recorded response contained no approval field, preserved the amount ambiguity, and noted the embedded instruction.

This is one observed example, not proof of comprehensive prompt-injection protection. Human review and restricted downstream actions remain necessary.

## Business Usefulness

The demonstration produces a consistent intake queue with invoice references, disputed amounts, exception reasons, and model review notes.

Potential usefulness includes reducing repeated transcription and making incomplete cases easier to identify. No time savings or financial benefit was measured.

## Next Evaluation Improvements

- Define expected fields before running a new extraction.
- Add unseen messages with different wording and formatting.
- Test customer mismatches, unsupported currencies, and multiple invoices.
- Test missing responses, duplicate IDs, extra fields, and fabricated excerpts.
- Compare repeat runs and record changes in behavior.
- Measure reviewer corrections and handling time before claiming efficiency gains.
