import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("Estoque")

        if "user_info" in st.session_state:
            st.caption(f"{st.session_state.get('user_info') or 'Não logado'}")

        st.divider()

        if st.button("Dashboard"):
            st.switch_page("dashboard.py")

        if st.button("Cadastro de Produtos"):
            st.switch_page("pages/product_registration.py")

        if st.button("Registro de Movimentações"):
            st.switch_page("pages/transactions_registration.py")

        if st.button("Histórico de Movimentações por Produto"):
            st.switch_page("pages/product_transactions.py")

        st.divider()

        if st.button("Sair"):
            st.session_state.clear()
            st.switch_page("dashboard.py")