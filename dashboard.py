import streamlit as st
from database.user import user_db
from database.transaction import transaction_db
from database.product import product_db
from ui import sidebar
import bcrypt

st.set_page_config(page_title="Sistema de Estoque", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "login"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "user_info_id" not in st.session_state:
    st.session_state.user_info_id = None

sidebar.render_sidebar()

if st.session_state.authenticated:
    st.title("Dashboard")
    st.write(f"Bem-vindo, **{st.session_state.user_info}**")

    st.divider()
    st.subheader("Consulta rápida de estoque")

    products = product_db.get_products(active_only=True)

    if not products:
        st.info("Nenhum produto cadastrado.")
    else:
        product_map = {p[1]: p[0] for p in products}

        selected_product = st.selectbox(
            "Selecione um produto",
            list(product_map.keys())
        )

        product_id = product_map[selected_product]
        quantity = transaction_db.get_product_balance(product_id)

        st.metric(
            label="Quantidade em estoque",
            value=quantity
        )

    st.divider()

elif st.session_state.page == "login":
    st.title("Sistema de Estoque")
    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")

    if submit:
        user = user_db.get_user(username)

        if user:
            hashed_password = user[2]

            if bcrypt.checkpw(password.encode(), hashed_password):
                st.session_state.authenticated = True
                st.session_state.user_info = username
                st.session_state.user_info_id = user[0]
                st.rerun()

        st.error("Usuário ou senha incorretos.")

    st.write("Não possui conta?")
    if st.button("Ir para Registro"):
        st.session_state.page = "register"
        st.rerun()

elif st.session_state.page == "register":
    st.title("Sistema de Estoque")
    st.subheader("Criar Nova Conta")

    with st.form("register_form"):
        new_user = st.text_input("Escolha um Usuário")
        new_pass = st.text_input("Escolha uma Senha", type="password")
        conf_pass = st.text_input("Confirme a Senha", type="password")
        submit_reg = st.form_submit_button("Cadastrar")

    if submit_reg:
        if new_pass != conf_pass:
            st.error("As senhas não coincidem.")
        elif not new_user or not new_pass:
            st.error("Preencha todos os campos.")
        else:
            if user_db.register_user(new_user, bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())):
                st.success("Conta criada com sucesso!")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Este nome de usuário já existe.")

    if st.button("Voltar para Login"):
        st.session_state.page = "login"
        st.rerun()