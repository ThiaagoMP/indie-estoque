import streamlit as st
import pandas as pd
from database.product import product_db
from database.transaction import transaction_db
from ui import sidebar

st.set_page_config(page_title="Histórico de Movimentações", layout="wide")

sidebar.render_sidebar()

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.switch_page("dashboard.py")

st.title("Histórico de Movimentações por Produto")

products = product_db.get_products(active_only=False)

if not products:
    st.info("Nenhum produto cadastrado.")
    st.stop()

product_map = {p[1]: p[0] for p in products}

selected_product = st.selectbox(
    "Selecione um produto",
    list(product_map.keys())
)

product_id = product_map[selected_product]

st.divider()

rows = transaction_db.get_transactions_by_product(product_id)

if not rows:
    st.info("Nenhuma movimentação registrada para este produto.")
    st.stop()

df = pd.DataFrame(
    rows,
    columns=["ID", "Data", "Tipo", "Quantidade", "Usuário", "Descrição"]
)

df.drop(columns=["ID"], inplace=True)

df["Data"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%Y %H:%M")

def color_type(val):
    if val == "ENTRADA":
        return "color: #2ecc71; font-weight: bold;"
    if val == "SAÍDA":
        return "color: #e74c3c; font-weight: bold;"
    return ""

styled_df = (
    df.style
    .applymap(color_type, subset=["Tipo"])
    .set_properties(**{
        "text-align": "center"
    })
)

df["Tipo"] = df["Tipo"].map({
    "INPUT": "ENTRADA",
    "OUTPUT": "SAÍDA"
})

st.subheader(f"Movimentações – {selected_product}")

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True
)
