import pandas as pd


class BankReconciliationEngine:
    """
    Core engine responsible for bank reconciliation logic.
    This implementation is intentionally generic and demonstrative.
    """

    def __init__(self, bank_df: pd.DataFrame, ledger_df: pd.DataFrame):
        self.bank_df = bank_df.copy()
        self.ledger_df = ledger_df.copy()

    def normalize_data(self):
        """Normalize columns for comparison."""
        self.bank_df["valor"] = self.bank_df["valor"].astype(float)
        self.ledger_df["valor"] = self.ledger_df["valor"].astype(float)

        self.bank_df["documento"] = self.bank_df["documento"].fillna("").astype(str)
        self.ledger_df["documento"] = self.ledger_df["documento"].fillna("").astype(str)

    def reconcile(self):
        """
        Perform reconciliation based on document + value + type.
        Returns dictionaries with reconciliation results.
        """
        self.normalize_data()

        bank = self.bank_df.copy()
        ledger = self.ledger_df.copy()

        bank["status"] = "PENDING_BANK"
        ledger["status"] = "PENDING_LEDGER"

        reconciled = []

        for b_idx, b_row in bank.iterrows():
            match = ledger[
                (ledger["documento"] == b_row["documento"]) &
                (ledger["valor"] == b_row["valor"])
            ]

            if not match.empty:
                l_idx = match.index[0]
                reconciled.append({
                    "documento": b_row["documento"],
                    "valor": b_row["valor"],
                    "descricao_banco": b_row["descricao"],
                    "descricao_razao": ledger.loc[l_idx, "descricao"]
                })

                bank.at[b_idx, "status"] = "RECONCILED"
                ledger.at[l_idx, "status"] = "RECONCILED"

        return {
            "reconciled": pd.DataFrame(reconciled),
            "pending_bank": bank[bank["status"] != "RECONCILED"],
            "pending_ledger": ledger[ledger["status"] != "RECONCILED"]
        }
