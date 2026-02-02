import pandas as pd


REQUIRED_BANK_COLUMNS = {
    "data_movimento",
    "descricao",
    "valor",
    "tipo",
    "documento"
}

REQUIRED_LEDGER_COLUMNS = {
    "data_lancamento",
    "conta",
    "descricao",
    "valor",
    "natureza",
    "documento"
}


def validate_dataframe(df: pd.DataFrame, required_columns: set, df_name: str):
    """Validate if dataframe has required structure."""
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(
            f"{df_name} is missing required columns: {', '.join(missing)}"
        )


def validate_bank_statement(df: pd.DataFrame):
    validate_dataframe(df, REQUIRED_BANK_COLUMNS, "Bank statement")


def validate_ledger(df: pd.DataFrame):
    validate_dataframe(df, REQUIRED_LEDGER_COLUMNS, "Accounting ledger")

