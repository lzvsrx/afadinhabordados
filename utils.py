# utils.py

from pathlib import Path
from database import IMAGE_FOLDER 

COR_PRINCIPAL = "#FFC0CB" # Rosa
LOGO_PATH = "logo.png"
NUMERO_CONTATO = "+5535992645905"

def save_uploaded_file(uploaded_file):
    """
    Salva o arquivo enviado para a pasta product_images. 
    Aviso: Em ambientes de hospedagem como Streamlit Cloud, esta pasta é VOLÁTIL.
    """
    if uploaded_file is None:
        return None

    file_path = IMAGE_FOLDER / uploaded_file.name
    
    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return str(file_path)
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return None
