# pages/servicos.py

import streamlit as st
from database import add_order, get_all_products
from utils import save_uploaded_file

def pagina_servicos():
    """Conteúdo da Página de Nossos Serviços/Pedidos."""
    st.title("🧵 Nossos Serviços & Pedidos")
    st.markdown("---")
    
    if not st.session_state.get('logged_in'):
        st.warning("Por favor, faça login para visualizar e realizar pedidos.")
        return

    st.header(f"Bem-vindo(a), {st.session_state.get('username')}!")
    st.write("Selecione o produto ou serviço desejado e anexe uma imagem de referência para personalização (opcional).")

    products = get_all_products()
    
    if not products:
        st.info("Nenhum produto/serviço disponível no momento. O administrador precisa cadastrar produtos.")
        return

    product_options = {p['name']: p for p in products}
    product_names = list(product_options.keys())

    with st.form("form_order_product"):
        
        selected_product_name = st.selectbox(
            "Produto/Serviço Desejado:",
            product_names,
            key="order_product_name"
        )
        
        selected_product = product_options[selected_product_name]
        if selected_product.get('image_path'):
            try:
                st.image(selected_product['image_path'], caption=selected_product_name, width=200)
            except Exception:
                st.warning("Imagem do produto não encontrada no caminho especificado. O arquivo pode ter sido perdido na hospedagem online.")


        col1, col2 = st.columns(2)
        with col1:
            order_quantity = st.number_input(
                "Quantidade:",
                min_value=1,
                max_value=selected_product['stock'] if selected_product['stock'] > 0 else 100, 
                step=1,
                key="order_quantity"
            )
            
        with col2:
            reference_file = st.file_uploader(
                "Imagem de Referência/Personalização (Opcional)",
                type=["png", "jpg", "jpeg"],
                key="order_reference_image"
            )
            
        order_details = st.text_area(
            "Detalhes e Instruções para Personalização:",
            key="order_details",
            placeholder="Ex: Quero o bordado na cor azul royal e fonte cursiva."
        )
        
        order_submitted = st.form_submit_button("Finalizar Pedido")

        if order_submitted:
            reference_image_path = save_uploaded_file(reference_file)
            
            if add_order(
                user_email=st.session_state.user_email,
                product_name=selected_product_name,
                quantity=order_quantity,
                details=order_details,
                reference_image_path=reference_image_path
            ):
                st.success("🎉 Pedido de serviço enviado com sucesso! Entraremos em contato em breve.")
            else:
                st.error("❌ Erro ao registrar o pedido no banco de dados. Verifique o terminal Streamlit.")

pagina_servicos()
