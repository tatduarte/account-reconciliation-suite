import pandas as pd

from src.core.bank_reconciliation.engine import BankReconciliationEngine
from src.services.validators import validate_bank_statement, validate_ledger


def run_test():
    bank_df = pd.read_csv("data/sample/extrato_demo.csv")
    ledger_df = pd.read_csv("data/sample/razao_demo.csv")

    validate_bank_statement(bank_df)
    validate_ledger(ledger_df)

    engine = BankReconciliationEngine(bank_df, ledger_df)
    result = engine.reconcile()

    print("\n=== RECONCILED ===")
    print(result["reconciled"])

    print("\n=== PENDING BANK ===")
    print(result["pending_bank"][["documento", "valor", "descricao"]])

    print("\n=== PENDING LEDGER ===")
    print(result["pending_ledger"][["documento", "valor", "descricao"]])


if __name__ == "__main__":
    run_test()

