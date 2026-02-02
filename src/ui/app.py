import sys
from pathlib import Path

# -------------------------------------------------
# Configura o caminho do projeto para imports
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from src.core.bank_reconciliation.engine import BankReconciliationEngine
from src.services.validators import validate_bank_statement, validate_ledger


# -------------------------------------------------
# Configuração da página
# -------------------------------------------------
st.set_page_config(
    page_title="Suite de Conciliação Contábil",
    layout="centered"
)

st.title("📊 Suite de Conciliação Contábil")
st.caption(
    "Interface demonstrativa para conciliação bancária automatizada. "
    "Todos os dados utilizados são fictícios."
)

# -------------------------------------------------
# Card de apresentação
# -------------------------------------------------
st.markdown(
    """
    <div style="background-color:#f5f7fa;
                padding:20px;
                border-radius:10px;
                border-left:5px solid #4f8bf9;
                margin-bottom:20px;">
        <strong>Objetivo da aplicação</strong><br>
        Demonstrar o processo de conciliação bancária de forma automatizada,
        clara e auditável, com foco em governança, confiabilidade das informações
        e redução de riscos operacionais.
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------
# Função auxiliar para nomes amigáveis
# -------------------------------------------------
def ajustar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={
        "documento": "Documento",
        "valor": "Valor",
        "descricao_banco": "Descrição (Banco)",
        "descricao_razao": "Descrição (Razão)",
        "descricao": "Descrição",
        "status": "Status"
    })


# -------------------------------------------------
# Upload de arquivos
# -------------------------------------------------
st.header("1️⃣ Envio dos arquivos")

col1, col2 = st.columns(2)

with col1:
    bank_file = st.file_uploader(
        "Extrato bancário (CSV)",
        type=["csv"]
    )

with col2:
    ledger_file = st.file_uploader(
        "Razão contábil (CSV)",
        type=["csv"]
    )

# -------------------------------------------------
# Processamento e resultados
# -------------------------------------------------
if bank_file and ledger_file:
    try:
        bank_df = pd.read_csv(bank_file)
        ledger_df = pd.read_csv(ledger_file)

        validate_bank_statement(bank_df)
        validate_ledger(ledger_df)

        st.success("Arquivos validados com sucesso.")

        if st.button("▶️ Executar conciliação"):
            engine = BankReconciliationEngine(bank_df, ledger_df)
            result = engine.reconcile()

            st.divider()
            st.header("2️⃣ Resultado da conciliação")

            # Métricas
            m1, m2, m3 = st.columns(3)
            m1.metric("Itens conciliados", len(result["reconciled"]))
            m2.metric("Pendências no banco", len(result["pending_bank"]))
            m3.metric("Pendências contábeis", len(result["pending_ledger"]))

            # Tabelas
            with st.expander("✅ Itens conciliados", expanded=True):
                st.dataframe(
                    ajustar_colunas(result["reconciled"]),
                    use_container_width=True
                )

            with st.expander("⚠️ Pendências no banco"):
                st.dataframe(
                    ajustar_colunas(result["pending_bank"]),
                    use_container_width=True
                )

            with st.expander("⚠️ Pendências contábeis"):
                st.dataframe(
                    ajustar_colunas(result["pending_ledger"]),
                    use_container_width=True
                )

            st.divider()
            st.header("3️⃣ Exportação")

            st.download_button(
                "📥 Baixar itens conciliados (CSV)",
                result["reconciled"].to_csv(index=False),
                file_name="itens_conciliados.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Erro ao processar os arquivos: {e}")

else:
    st.info("Envie o extrato bancário e o razão contábil para iniciar a conciliação.")

# -------------------------------------------------
# Rodapé
# -------------------------------------------------
st.divider()
st.caption(
    "Projeto demonstrativo de portfólio • Dados fictícios • "
    "Desenvolvido por Tatiana Duarte"
)

