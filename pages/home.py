# pages/home.py

import streamlit as st

def pagina_home():
    """Conteúdo da Página Inicial."""
    st.title("Bem-vindo(a) à A Fadinha Bordados! ✨")
    st.markdown("---")
    
    st.header("Sua Parceira em Personalização de Bordados")
    st.write("""
        Somos especializados em transformar ideias em arte têxtil. 
        Utilizamos tecnologia de ponta e materiais de alta qualidade para garantir que cada peça seja única e duradoura.
    """)
    
    if st.session_state.get('logged_in'):
        st.success(f"Você está logado(a) como {st.session_state.username}.")
        st.info("Navegue até **Nossos Serviços** para fazer seu pedido personalizado.")
    else:
        st.info("Faça seu **Login** ou **Cadastre-se** na barra lateral para começar a fazer pedidos!")
        
    st.markdown("---")
    
    st.subheader("Nosso Diferencial")
    st.write("* **Qualidade Garantida:** Fios resistentes e cores vibrantes.")
    st.write("* **Atendimento Personalizado:** Transformamos sua ideia em realidade.")
    st.write("* **Agilidade:** Entrega rápida e eficiente.")
