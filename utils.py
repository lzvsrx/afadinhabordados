# utils.py

import streamlit as st
from pathlib import Path
# Importamos IMAGE_FOLDER, assumindo que database.py já o definiu
from database import IMAGE_FOLDER 

COR_PRINCIPAL = "#FFC0CB" # Rosa
LOGO_PATH = "logo.png"
NUMERO_CONTATO = "+5535992645905"

def save_uploaded_file(uploaded_file):
    """Salva o arquivo enviado para a pasta product_images e retorna o caminho relativo."""
    if uploaded_file is None:
        return None

    # Monta o caminho completo no disco
    file_path = IMAGE_FOLDER / uploaded_file.name
    
    # Escreve o arquivo no disco
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    # Retorna o caminho relativo como string
    return str(file_path)