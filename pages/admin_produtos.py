# pages/admin_produtos.py

import streamlit as st
import pandas as pd
from database import add_product, get_all_products
from utils import save_uploaded_file

def pagina_admin_produtos():
    """Página dedicada ao Gerenciamento de Produtos (Acesso Restrito a Admin)."""
    
    if not st.session_state.get('logged_in') or not st.session_state.get('is_admin'):
        st.error("Acesso negado. Esta página é restrita a Administradores.")
        return
        
    st.title("Gerenciamento de Produtos 📦")
    st.markdown("---")

    st.header("➕ Cadastro de Novo Produto")
    
    with st.form("form_create_product"):
        prod_name = st.text_input("Nome do Produto", key="admin_prod_name")
        prod_description = st.text_area("Descrição", key="admin_prod_description")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            prod_price = st.number_input("Preço (R$)", min_value=0.01, format="%.2f", key="admin_prod_price")
        with col2:
            prod_stock = st.number_input("Estoque Inicial", min_value=0, step=1, key="admin_prod_stock")
        with col3:
            uploaded_file = st.file_uploader(
                "Imagem do Produto (Opcional)",
                type=["png", "jpg", "jpeg"],
                key="admin_prod_image_uploader"
            )
            
        product_submitted = st.form_submit_button("Salvar Produto")
        
        if product_submitted:
            if not prod_name or not prod_price:
                st.error("Preencha o Nome e o Preço do produto.")
            else:
                image_path = save_uploaded_file(uploaded_file)
                
                if add_product(prod_name, prod_description, prod_price, prod_stock, image_path):
                    st.success(f"Produto '{prod_name}' cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao cadastrar o produto no banco de dados. **Verifique o terminal Streamlit** para detalhes do erro SQL.") 

    st.markdown("---")
    st.header("📋 Produtos Cadastrados")
    
    products_data = get_all_products()
    if products_data:
        df_products = pd.DataFrame(products_data)
        df_products = df_products.rename(columns={'name': 'Produto', 'description': 'Descrição', 'price': 'Preço (R$)', 'stock': 'Estoque', 'image_path': 'Caminho Imagem', 'id': 'ID'})
        
        df_products['Preço (R$)'] = df_products['Preço (R$)'].apply(lambda x: f"R$ {x:.2f}".replace('.', ','))
        
        cols_to_display = ['ID', 'Produto', 'Preço (R$)', 'Estoque', 'Caminho Imagem']
        st.dataframe(df_products[cols_to_display], use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum produto cadastrado ainda.")

pagina_admin_produtos()