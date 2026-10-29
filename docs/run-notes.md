# Extraction Run Notes

## Run v1

- **Date:** October 29, 2026
- **Interface:** ChatGPT, manual conversation
- **Model label:** GPT-6.1 Sol, as reported by the user from the ChatGPT interface
- **Exact backend model identifier:** Not independently verified
- **Prompt:** prompts/extract_dispute.md
- **Source messages:** data/dispute_messages.json
- **Recorded response:** outputs/model_response_v1.json
- **Invoice register supplied to the model:** No
- **Response handling:** Preserved as returned, as reported by the user
- **API execution:** None; this was a manual ChatGPT run

## Initial Review

Manual inspection found that the response:

- Left absent invoice, amount, and currency fields null for MSG-003.
- Preserved the unknown invoice reference in MSG-004.
- Extracted the stated amount in MSG-005 without claiming invoice verification.
- Left the ambiguous disputed amount null for MSG-006.
- Included no approval field and noted the embedded instruction in MSG-006.

These observations are not an automated evaluation or evidence of general model accuracy.

## Reproduction Boundary

The planned Python workflow will replay this recorded response and validate it against the source messages and invoice register. Replay does not make a new model call.

A new ChatGPT run may produce different wording or results. This six-message demonstration is too small to establish production accuracy or broad resistance to embedded instructions.

## Human Review

Extracted claims remain unverified customer allegations. Passing structural and invoice checks does not prove a billing error or authorize a credit.
