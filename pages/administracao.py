# pages/administracao.py

import streamlit as st
import pandas as pd
import re
from database import get_all_users_list, add_user, get_all_users

MIN_PASSWORD_LENGTH = 6

def is_valid_email(email):
    """Verifica se o email possui um formato básico válido."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def pagina_administracao():
    """Conteúdo da Página de Administração (Gerenciamento de Usuários)."""
    
    if not st.session_state.get('logged_in') or not st.session_state.get('is_admin'):
        st.error("Acesso negado. Esta página é restrita a Administradores.")
        return
        
    st.title("Administração (Usuários) ⚙️")
    st.markdown("---")
    st.header(f"Olá, {st.session_state.username}! Gerenciamento de Usuários.")
    
    
    st.subheader("👥 Listagem de Usuários")
    
    try:
        users_data = get_all_users_list()
        df = pd.DataFrame(users_data)
        df['role'] = df['role'].apply(lambda x: '⭐ ADMIN' if x == 'admin' else 'CLIENTE')
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Não foi possível carregar a lista de usuários: {e}")

    st.markdown("---")
    st.subheader("➕ Criar Novo Usuário / Admin")

    with st.form("form_create_user"):
        
        col1, col2 = st.columns(2)
        with col1:
            new_user_name = st.text_input("Nome Completo", key="admin_new_name")
            new_user_email = st.text_input("Email de Cadastro", key="admin_new_email")
            new_user_password = st.text_input(f"Senha (mín. {MIN_PASSWORD_LENGTH} caracteres)", type="password", key="admin_new_password")
        
        with col2:
            new_user_cpf = st.text_input("CPF", max_chars=14, help="Opcional. Formato: 000.000.000-00", key="admin_new_cpf")
            new_user_address = st.text_area("Endereço Completo", key="admin_new_address")
            
            new_user_role = st.selectbox(
                "Permissão do Usuário:",
                options=["client", "admin"],
                format_func=lambda x: "Cliente" if x == "client" else "Administrador",
                key="admin_new_role"
            )
            
        submitted = st.form_submit_button("Criar Usuário")

        if submitted:
            if not all([new_user_name, new_user_email, new_user_password]):
                st.error("Preencha nome, email e senha.")
                return
            if not is_valid_email(new_user_email):
                st.error("Formato de email inválido.")
                return
            if len(new_user_password) < MIN_PASSWORD_LENGTH:
                st.error(f"A senha deve ter no mínimo {MIN_PASSWORD_LENGTH} caracteres.")
                return

            user_data = {
                "email": new_user_email, "name": new_user_name, "password": new_user_password,
                "cpf": new_user_cpf, "address": new_user_address, "role": new_user_role 
            }
            
            if add_user(user_data):
                st.success(f"Usuário '{new_user_name}' criado com sucesso como **{new_user_role.upper()}**!")
                st.session_state.users = get_all_users()
                st.rerun() 
            else:
                st.error(f"Erro: O email '{new_user_email}' já está cadastrado ou houve um erro no DB.")

pagina_administracao()