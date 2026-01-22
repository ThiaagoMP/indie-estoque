import streamlit as st
from database.product import product_db
import sqlite3

from ui import sidebar

st.set_page_config(page_title="Produtos", layout="wide")

sidebar.render_sidebar()

if "product_message" not in st.session_state:
    st.session_state.product_message = None

if "product_message_type" not in st.session_state:
    st.session_state.product_message_type = None

if "edit_selected_product" not in st.session_state:
    st.session_state.edit_selected_product = None

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.switch_page("dashboard.py")

st.title("Cadastro de Produtos")

if st.session_state.product_message:
    if st.session_state.product_message_type == "success":
        st.success(st.session_state.product_message)
    else:
        st.error(st.session_state.product_message)

    st.session_state.product_message = None
    st.session_state.product_message_type = None

tab_create, tab_edit = st.tabs(["Cadastrar", "Editar / Remover"])

with tab_create:
    st.subheader("Novo Produto")

    with st.form("create_product_form", clear_on_submit=True):
        name = st.text_input("Nome do Produto")
        description = st.text_input("Descrição do Produto")
        submit_create = st.form_submit_button("Cadastrar")

    if submit_create:
        if not name.strip():
            st.error("Informe o nome do produto.")
        else:
            try:
                product_db.create_product(
                    name.strip(),
                    description.strip(),
                    1
                )
                st.session_state.product_message = "Produto cadastrado com sucesso."
                st.session_state.product_message_type = "success"
                st.rerun()

            except Exception as e:
                st.session_state.product_message = str(e)
                st.session_state.product_message_type = "error"
                st.rerun()

with tab_edit:
    st.subheader("Produtos Cadastrados")

    products = product_db.get_products(active_only=False)

    if not products:
        st.info("Nenhum produto cadastrado.")
    else:
        product_map = {p[1]: p for p in products}

        selected = st.selectbox(
            "Selecione um produto",
            list(product_map.keys()),
            index=(
                list(product_map.keys()).index(st.session_state.edit_selected_product)
                if st.session_state.edit_selected_product in product_map
                else 0
            )
        )
        st.session_state.edit_selected_product = selected

        product_id, name, description, active = product_map[selected]

        with st.form("edit_product_form"):
            new_name = st.text_input("Nome", value=name)
            new_description = st.text_input("Descrição do Produto", value=description)
            new_active = st.checkbox("Ativo", value=bool(active))

            submit_edit = st.form_submit_button("Salvar Alterações")

        if submit_edit:
            if not new_name.strip():
                st.error("Nome inválido.")
            else:
                try:
                    product_db.update_product(
                        product_id,
                        new_name.strip(),
                        new_description.strip(),
                        int(new_active)
                    )
                    st.session_state.product_message = "Produto atualizado com sucesso."
                    st.session_state.product_message_type = "success"
                    st.rerun()

                except Exception as e:
                    st.session_state.product_message = str(e)
                    st.session_state.product_message_type = "error"
                    st.rerun()

        if st.button("Remover Produto"):
            try:
                product_db.delete_product(product_id)
                st.session_state.product_message = "Produto removido com sucesso."
                st.session_state.product_message_type = "success"
                st.session_state.edit_selected_product = None

            except sqlite3.IntegrityError as e:
                st.session_state.product_message = str(e)
                st.session_state.product_message_type = "error"

            except Exception as e:
                st.session_state.product_message = str(e)
                st.session_state.product_message_type = "error"

            st.rerun()
