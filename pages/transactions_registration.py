import streamlit as st
from database.transaction import transaction_db
from database.product import product_db
from ui import sidebar

st.set_page_config(page_title="Movimentações", layout="wide")

sidebar.render_sidebar()

if "transaction_message" not in st.session_state:
    st.session_state.transaction_message = None

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.switch_page("dashboard.py")

st.title("Registro de Movimentações")

if st.session_state.transaction_message:
    st.success(st.session_state.transaction_message)
    st.session_state.transaction_message = None

products = product_db.get_products(active_only=True)

if not products:
    st.info("Nenhum produto disponível para movimentação.")
    st.stop()

product_map = {
    f"{p[1]} (ID {p[0]})": p[0] for p in products
}

with st.form("transaction_form"):
    product_label = st.selectbox("Produto", list(product_map.keys()))

    transaction_type = st.radio(
        "Tipo de Movimentação",
        ["ENTRADA", "SAIDA"]
    )

    quantity = st.number_input("Quantidade", min_value=1, step=1)
    description = st.text_input("Descrição (opcional)")

    submit = st.form_submit_button("Registrar")

if submit:
    try:
        t_type = "INPUT" if transaction_type == "ENTRADA" else "OUTPUT"

        transaction_db.create_transaction(
            user_id=st.session_state.user_info_id,
            product_id=product_map[product_label],
            t_type=t_type,
            quantity=quantity,
            description=description
        )

        st.session_state.transaction_message = "Movimentação registrada com sucesso."
        st.rerun()

    except Exception as e:
        st.error(f"Erro ao registrar movimentação: {e}")
