# pages/auth.py

import streamlit as st
import re 
from database import add_user, get_all_users 

MIN_PASSWORD_LENGTH = 6

def is_valid_email(email):
    """Verifica se o email possui um formato básico válido."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def pagina_login_cadastro():
    """Gerencia o login e cadastro de usuários na sidebar em duas abas."""
    st.sidebar.header("🚪 Login / Cadastro")
    
    if 'users' not in st.session_state:
        st.session_state.users = get_all_users() 
    
    tab1, tab2 = st.sidebar.tabs(["Login", "Novo Cadastro"])

    # --- Tab 1: Login ---
    with tab1:
        st.subheader("Login de Cliente/Admin")
        login_email = st.text_input("Email", key="login_email_auth")
        login_password = st.text_input("Senha", type="password", key="login_password_auth")
        
        if st.button("Entrar", key="btn_login_auth"):
            if not login_email or not login_password:
                st.sidebar.error("Preencha email e senha para entrar.")
            
            elif login_email in st.session_state.users:
                user = st.session_state.users[login_email]
                
                if user['password'] == login_password:
                    st.session_state.logged_in = True
                    st.session_state.username = user['name']
                    st.session_state.user_email = login_email
                    st.session_state.is_admin = user['role'] == 'admin' 
                    st.sidebar.success(f"Bem-vindo(a), {st.session_state.username}!")
                    st.rerun()
                else:
                    st.sidebar.error("Email ou senha incorretos.")
            else:
                st.sidebar.error("Email ou senha incorretos.")

    # --- Tab 2: Novo Cadastro (PÚBLICO) ---
    with tab2:
        st.subheader("Crie sua Conta")
        
        new_name = st.text_input("Nome Completo", key="new_name_client")
        new_email = st.text_input("Email de Cadastro", key="new_email_client")
        new_password = st.text_input(f"Senha (mín. {MIN_PASSWORD_LENGTH} caracteres)", type="password", key="new_password_client")
        new_cpf = st.text_input("CPF (Obrigatório)", max_chars=14, help="Formato: 000.000.000-00", key="new_cpf_client")
        new_address = st.text_area("Endereço Completo (Obrigatório)", key="new_address_client")
        
        st.markdown("---")
        
        # CAMPO DE SELEÇÃO PÚBLICA DE ROLE (Mantido conforme última solicitação)
        new_role = st.selectbox(
            "Selecione o Tipo de Usuário:",
            options=["client", "admin"],
            format_func=lambda x: "Cliente" if x == "client" else "Administrador",
            key="new_user_role_public"
        )
        
        if st.button("Finalizar Cadastro", key="btn_cadastro_client"):
            
            if not all([new_name, new_email, new_password, new_cpf, new_address]):
                st.error("Preencha todos os campos obrigatórios!")
                return
            
            if not is_valid_email(new_email):
                st.error("Por favor, insira um formato de email válido.")
                return

            if len(new_password) < MIN_PASSWORD_LENGTH:
                st.error(f"A senha deve ter no mínimo {MIN_PASSWORD_LENGTH} caracteres.")
                return

            if new_email in st.session_state.users:
                st.error("Este email já está cadastrado. Tente fazer login.")
                return

            role = new_role 
            msg_success = f"Cadastro realizado com sucesso como **{role.upper()}**!"

            user_data = {
                "email": new_email, "name": new_name, "password": new_password,
                "cpf": new_cpf, "address": new_address, "role": role 
            }
            
            if add_user(user_data):
                st.session_state.users = get_all_users() 
                st.success(msg_success)
                st.info("Faça o login na aba ao lado.")
            else:
                st.error("❌ Erro interno ao salvar no banco de dados. Verifique o terminal Streamlit.")
    
    st.sidebar.markdown("---")