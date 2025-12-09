# app.py

import streamlit as st
from utils import COR_PRINCIPAL, LOGO_PATH, NUMERO_CONTATO
from pages.auth import pagina_login_cadastro
from pages.home import pagina_home
from pages.servicos import pagina_servicos
from pages.administracao import pagina_administracao
from pages.admin_produtos import pagina_admin_produtos 
from pathlib import Path
from database import initialize_db, get_all_users

def load_css(file_name):
    """Carrega o arquivo CSS e o injeta no Streamlit."""
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.sidebar.error("Arquivo CSS (style.css) não encontrado. Verifique o caminho.")
        
def inicializar_estado():
    """Inicializa as variáveis de estado de sessão e dados iniciais."""
    initialize_db()
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = "Convidado"
        st.session_state.user_email = ""
        st.session_state.is_admin = False 
    
    st.session_state.users = get_all_users() 
    
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'

def pagina_sair():
    """Função para encerrar a sessão do usuário."""
    st.session_state.logged_in = False
    st.session_state.username = "Convidado"
    st.session_state.user_email = ""
    st.session_state.is_admin = False
    st.session_state.page = 'Home'
    st.success("Sessão encerrada com sucesso!")
    st.rerun()

def main():
    """Função principal da aplicação Streamlit."""
    st.set_page_config(
        page_title="A Fadinha Bordados", 
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # 1. Carregar CSS externo
    load_css("style.css")
    
    # 2. Inicializar estado
    inicializar_estado()
    
    # 3. Exibir Logo na Sidebar
    if Path(LOGO_PATH).exists():
        st.sidebar.image(LOGO_PATH, width='stretch', output_format="PNG")
    else:
        st.sidebar.warning("Logo não encontrada! Usando título.")
        st.sidebar.header("A Fadinha Bordados")
        
    # 4. Gerenciamento de Autenticação e Navegação
    if not st.session_state.logged_in:
        pagina_login_cadastro()
        pagina_home() 
    else:
        st.sidebar.markdown(f"**Usuário:** {st.session_state.username} ({'Admin' if st.session_state.is_admin else 'Cliente'})")
        
        pages = ["Home", "Nossos Serviços"]
        
        if st.session_state.is_admin:
            pages.append("Gerenciar Produtos (Admin)") 
            pages.append("Administração (Usuários)") 

        pages.append("Sair")
        
        st.session_state.page = st.sidebar.radio("Navegação", pages, index=pages.index(st.session_state.page) if st.session_state.page in pages else 0)
        
        st.sidebar.markdown("---")
        
        # Roteamento
        if st.session_state.page == "Home":
            pagina_home()
        elif st.session_state.page == "Nossos Serviços":
            pagina_servicos()
        elif st.session_state.page == "Administração (Usuários)":
            if st.session_state.is_admin:
                pagina_administracao() 
            else:
                pagina_home() 
        elif st.session_state.page == "Gerenciar Produtos (Admin)":
            if st.session_state.is_admin:
                pagina_admin_produtos() 
            else:
                pagina_home() 
        elif st.session_state.page == "Sair":
            pagina_sair()

    # 5. Adicionar Contato e Link do WhatsApp (BOTTOM)
    clean_number = NUMERO_CONTATO.replace('+', '').replace(' ', '').replace('-', '')
    whatsapp_url = f"https://wa.me/{clean_number}"
    
    st.sidebar.markdown("---")
    # Este link deve usar estilo inline para garantir que funcione corretamente
    st.sidebar.markdown(f"""
        **Fale Conosco:**
        <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
            <button style="background-color: var(--whatsapp-color, #25D366); color: white; padding: 5px 10px; border: none; border-radius: 5px; cursor: pointer; display: block; width: 100%;">
                📲 WhatsApp {NUMERO_CONTATO}
            </button>
        </a>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
