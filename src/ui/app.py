import sys
from pathlib import Path

# Add project root to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from src.core.bank_reconciliation.engine import BankReconciliationEngine
from src.services.validators import validate_bank_statement, validate_ledger


st.set_page_config(
    page_title="Account Reconciliation Suite",
    layout="centered"
)

st.title("Account Reconciliation Suite")
st.caption(
    "Demonstrative interface for automated bank reconciliation "
    "(fictitious data only)."
)

st.divider()

st.header("1. Upload files")

bank_file = st.file_uploader(
    "Upload bank statement (CSV)",
    type=["csv"]
)

ledger_file = st.file_uploader(
    "Upload accounting ledger (CSV)",
    type=["csv"]
)

if bank_file and ledger_file:
    try:
        bank_df = pd.read_csv(bank_file)
        ledger_df = pd.read_csv(ledger_file)

        validate_bank_statement(bank_df)
        validate_ledger(ledger_df)

        st.success("Files validated successfully.")

        if st.button("Run reconciliation"):
            engine = BankReconciliationEngine(bank_df, ledger_df)
            result = engine.reconcile()

            st.divider()
            st.header("2. Results")

            st.subheader("✅ Reconciled")
            st.dataframe(result["reconciled"])

            st.subheader("⚠️ Pending – Bank")
            st.dataframe(result["pending_bank"])

            st.subheader("⚠️ Pending – Ledger")
            st.dataframe(result["pending_ledger"])

            st.divider()
            st.header("3. Export results")

            st.download_button(
                "Download reconciled (CSV)",
                result["reconciled"].to_csv(index=False),
                file_name="reconciled.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error: {e}")
