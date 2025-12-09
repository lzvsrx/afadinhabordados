# pages/admin_produtos.py

import streamlit as st
import pandas as pd
from database import add_product, get_all_products, get_product, update_product, delete_product
from utils import save_uploaded_file, IMAGE_FOLDER
from pathlib import Path

def display_product_table(products_data):
    """Exibe a lista de produtos em um DataFrame."""
    if products_data:
        df_products = pd.DataFrame(products_data)
        df_products = df_products.rename(columns={'name': 'Produto', 'description': 'Descrição', 'price': 'Preço (R$)', 'stock': 'Estoque', 'image_path': 'Caminho Imagem', 'id': 'ID'})
        
        df_products['Preço (R$)'] = df_products['Preço (R$)'].apply(lambda x: f"R$ {x:.2f}".replace('.', ','))
        
        cols_to_display = ['ID', 'Produto', 'Preço (R$)', 'Estoque', 'Caminho Imagem']
        st.dataframe(df_products[cols_to_display], use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum produto cadastrado ainda.")

def pagina_admin_produtos():
    """Página dedicada ao Gerenciamento de Produtos (Acesso Restrito a Admin)."""
    
    if not st.session_state.get('logged_in') or not st.session_state.get('is_admin'):
        st.error("Acesso negado. Esta página é restrita a Administradores.")
        return
        
    st.title("Gerenciamento de Produtos 📦")
    st.markdown("---")
    
    products_data = get_all_products()
    product_ids = [p['id'] for p in products_data]
    
    # 1. Abas para as operações
    tab_cadastrar, tab_modificar, tab_deletar, tab_listar = st.tabs([
        "➕ Cadastrar", 
        "✏️ Modificar", 
        "🗑️ Deletar", 
        "📋 Listar Todos"
    ])

    # --- TAB 1: Cadastrar Novo Produto ---
    with tab_cadastrar:
        st.header("Cadastrar Novo Produto")
        with st.form("form_create_product"):
            prod_name = st.text_input("Nome do Produto", key="admin_prod_name_c")
            prod_description = st.text_area("Descrição", key="admin_prod_description_c")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                prod_price = st.number_input("Preço (R$)", min_value=0.01, format="%.2f", key="admin_prod_price_c")
            with col2:
                prod_stock = st.number_input("Estoque Inicial", min_value=0, step=1, key="admin_prod_stock_c")
            with col3:
                uploaded_file = st.file_uploader(
                    "Imagem do Produto (Opcional)",
                    type=["png", "jpg", "jpeg"],
                    key="admin_prod_image_uploader_c"
                )
                
            product_submitted = st.form_submit_button("Salvar Produto")
            
            if product_submitted:
                if not prod_name or not prod_price:
                    st.error("Preencha o Nome e o Preço do produto.")
                else:
                    image_path = save_uploaded_file(uploaded_file)
                    
                    if add_product(prod_name, prod_description, prod_price, prod_stock, image_path):
                        st.success(f"Produto '{prod_name}' cadastrado com sucesso! Recarregando lista...")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao cadastrar o produto no banco de dados. Verifique o terminal Streamlit.") 

    # --- TAB 2: Modificar Produto ---
    with tab_modificar:
        st.header("Modificar Produto Existente")
        
        if not product_ids:
            st.warning("Nenhum produto cadastrado para modificar.")
        else:
            product_to_edit_id = st.selectbox(
                "Selecione o ID do Produto para Modificar:",
                options=product_ids,
                key="mod_prod_id"
            )
            
            selected_product = get_product(product_to_edit_id)
            
            if selected_product:
                with st.form(f"form_modify_product_{product_to_edit_id}"):
                    
                    # Campos pré-preenchidos
                    mod_name = st.text_input("Nome do Produto", value=selected_product['name'], key="mod_prod_name")
                    mod_description = st.text_area("Descrição", value=selected_product['description'], key="mod_prod_description")
                    
                    colA, colB, colC = st.columns(3)
                    with colA:
                        mod_price = st.number_input("Preço (R$)", min_value=0.01, format="%.2f", value=selected_product['price'], key="mod_prod_price")
                    with colB:
                        mod_stock = st.number_input("Estoque", min_value=0, step=1, value=selected_product['stock'], key="mod_prod_stock")
                    with colC:
                        mod_uploaded_file = st.file_uploader(
                            "Nova Imagem do Produto (Opcional)",
                            type=["png", "jpg", "jpeg"],
                            key="mod_prod_image_uploader"
                        )
                        st.caption(f"Imagem atual: {selected_product['image_path'] or 'Nenhuma'}")
                    
                    # Exibe a imagem atual
                    if selected_product['image_path'] and Path(selected_product['image_path']).exists():
                         st.image(selected_product['image_path'], width=100, caption="Imagem Atual")

                    modify_submitted = st.form_submit_button("Salvar Modificações")

                    if modify_submitted:
                        new_image_path = None # Não atualizar o caminho no DB por padrão
                        
                        # Se uma nova imagem foi carregada, salva e usa o novo caminho
                        if mod_uploaded_file:
                            new_image_path = save_uploaded_file(mod_uploaded_file)
                        
                        # Executa o update. Passamos None para new_image_path se nenhuma nova imagem foi enviada.
                        if update_product(product_to_edit_id, mod_name, mod_description, mod_price, mod_stock, new_image_path):
                            st.success(f"Produto ID {product_to_edit_id} modificado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao modificar produto. Verifique o terminal Streamlit.")
            else:
                st.error("Produto não encontrado.")

    # --- TAB 3: Deletar Produto ---
    with tab_deletar:
        st.header("Deletar Produto")
        
        if not product_ids:
            st.warning("Nenhum produto cadastrado para deletar.")
        else:
            product_to_delete_id = st.selectbox(
                "Selecione o ID do Produto para Deletar:",
                options=product_ids,
                key="del_prod_id"
            )
            
            if st.button(f"🗑️ Confirmar Deleção do Produto ID {product_to_delete_id}", key="btn_delete_product"):
                
                prod_data = get_product(product_to_delete_id)
                
                # 1. Tenta deletar o arquivo de imagem (opcional)
                if prod_data and prod_data['image_path']:
                    img_path = Path(prod_data['image_path'])
                    try:
                        if img_path.exists():
                            img_path.unlink() # Deleta o arquivo
                    except Exception as e:
                        print(f"Aviso: Não foi possível deletar o arquivo {img_path}: {e}")
                
                # 2. Deleta do banco
                if delete_product(product_to_delete_id):
                    st.success(f"Produto ID {product_to_delete_id} deletado permanentemente.")
                    st.rerun()
                else:
                    st.error("❌ Erro ao deletar produto. Verifique o terminal Streamlit.")

    # --- TAB 4: Listar Todos ---
    with tab_listar:
        st.header("Produtos Cadastrados")
        products_data = get_all_products()
        display_product_table(products_data)

pagina_admin_produtos()
