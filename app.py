import csv
import json
from decimal import Decimal
from pathlib import Path

import streamlit as st

from validate import check_structure, index_unique, invoice_checks

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="AI Billing Dispute Intake",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {max-width: 1250px; padding-top: 2rem; padding-bottom: 3rem;}
    [data-testid="stMetric"] {
        background: rgba(248,249,251,.9);
        border: 1px solid rgba(49,51,63,.10);
        padding: 14px 16px;
        border-radius: 12px;
    }
    .note {
        padding: 12px 14px;
        border: 1px solid rgba(49,51,63,.10);
        border-radius: 10px;
        background: rgba(248,249,251,.8);
        color: #6b7280;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


messages = load_json("data/dispute_messages.json")
responses = load_json("outputs/model_response_v1.json")
message_index = index_unique(messages, "message_id")
response_index = index_unique(responses, "message_id")

with (ROOT / "data/invoices.csv").open(newline="", encoding="utf-8") as file:
    invoices = index_unique(list(csv.DictReader(file)), "invoice_id")

st.title("AI Billing Dispute Intake")
st.markdown(
    '<div class="note">Interactive portfolio demonstration using fictional billing messages and synthetic invoice records. The recorded extraction is replayed for reproducibility; this app does not make live AI calls or authorize financial action.</div>',
    unsafe_allow_html=True,
)

st.subheader("Review a synthetic dispute")
selected_id = st.selectbox(
    "Example case",
    list(message_index),
    format_func=lambda message_id: f"{message_id} · {message_index[message_id]['text'][:70]}...",
)

source = message_index[selected_id]
record = response_index[selected_id]

left, right = st.columns([1.05, 1])
with left:
    st.markdown("#### Customer message")
    st.info(source["text"])
    st.caption("The message is untrusted source data. Instructions inside it do not override validation rules.")

with right:
    st.markdown("#### Recorded AI extraction")
    a, b = st.columns(2)
    a.metric("Invoice", record["invoice_id"] or "Missing")
    b.metric(
        "Disputed amount",
        f"${Decimal(record['disputed_amount']):,.2f}" if record["disputed_amount"] else "Missing",
    )
    st.write(f"**Customer:** {record['customer_name'] or 'Missing'}")
    st.write(f"**Issue category:** {record['issue_category'].replace('_', ' ').title()}")
    st.write(f"**Currency:** {record['currency'] or 'Missing'}")

try:
    check_structure(record, source["text"])
    structural_status = "PASS"
    structural_detail = "Required fields, types, and source-evidence checks passed."
except ValueError as error:
    structural_status = "REJECTED"
    structural_detail = str(error)

flags = invoice_checks(record, invoices)
route = "Exception review" if flags else "Standard review"

st.markdown("### Deterministic validation")
c1, c2, c3 = st.columns(3)
c1.metric("Structural validation", structural_status)
c2.metric("Intake route", route)
c3.metric("Human review", "Required")

if structural_status == "PASS":
    st.success(structural_detail)
else:
    st.error(structural_detail)

if flags:
    st.warning("Intake exceptions: " + ", ".join(flag.replace("_", " ") for flag in flags))
else:
    st.success("No intake exceptions detected. Standard review still requires human judgment.")

with st.expander("Evidence used for the extraction", expanded=True):
    evidence_rows = []
    for field, excerpt in record["evidence"].items():
        evidence_rows.append({
            "Field": field.replace("_", " ").title(),
            "Source excerpt": excerpt if excerpt is not None else "Not supplied",
        })
    st.dataframe(evidence_rows, use_container_width=True, hide_index=True)

if record["review_notes"]:
    with st.expander("Recorded model review notes", expanded=True):
        for note in record["review_notes"]:
            st.write(f"• {note}")

st.divider()
st.subheader("Why validation matters")
st.caption("Deliberately alter the extracted amount while keeping the original evidence. The validator should reject the unsupported value.")

original_amount = record["disputed_amount"]
if original_amount is not None:
    test_amount = st.text_input("Test extracted amount", value=original_amount)
    if st.button("Run validation test", type="primary"):
        altered = json.loads(json.dumps(record))
        altered["disputed_amount"] = test_amount
        try:
            check_structure(altered, source["text"])
            st.success("PASS: the amount is supported by the source evidence.")
        except ValueError as error:
            st.error(f"REJECTED: {error}")
else:
    st.info("This example intentionally has no single disputed amount. Choose a case with an extracted amount to run the alteration test.")

st.divider()
st.caption(
    "Portfolio demonstration only. All customers, messages, invoices, and amounts are fictional. "
    "The workflow prepares cases for analyst review and never approves credits, changes invoices, or contacts customers."
)
