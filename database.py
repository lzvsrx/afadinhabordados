# database.py

import sqlite3
from typing import Optional, Dict, List
from pathlib import Path 

DATABASE_NAME = "fadinha_db.db"
# Definindo a pasta de imagens aqui para que utils.py possa importar
IMAGE_FOLDER = Path("product_images") 

IMAGE_FOLDER.mkdir(exist_ok=True)

def get_db_connection():
    """Cria e retorna a conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Cria as tabelas de usuários, produtos e pedidos se elas não existirem."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Tabela de Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            cpf TEXT,
            address TEXT,
            role TEXT DEFAULT 'client' CHECK(role IN ('client', 'admin'))
        )
    """)
    
    # 2. Tabela de Produtos (com image_path)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            image_path TEXT 
        )
    """)
    
    # 3. Tabela de Pedidos (com reference_image_path)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            details TEXT,
            reference_image_path TEXT, 
            status TEXT DEFAULT 'Pendente',
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    """)

    # Adicionar Admin inicial (se não existir)
    admin_email = "admin@fadinha.com"
    cursor.execute("SELECT email FROM users WHERE email = ?", (admin_email,))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (email, name, password, cpf, address, role) VALUES (?, ?, ?, ?, ?, ?)",
            (admin_email, "Admin Master", "456", "999.999.999-99", "Rua do Poder, 100", "admin")
        )
        
    conn.commit()
    conn.close()

# --- Funções de CRUD ---

def get_user(email: str) -> Optional[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user_data = cursor.fetchone()
    conn.close()
    return dict(user_data) if user_data else None

def add_user(data: Dict) -> bool:
    if get_user(data['email']): return False 
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, name, password, cpf, address, role) VALUES (?, ?, ?, ?, ?, ?)",
            (data['email'], data['name'], data['password'], data['cpf'], data['address'], data['role'])
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"ERRO SQL ao adicionar usuário '{data['email']}': {e}")
        return False
    finally:
        conn.close()

def get_all_users() -> Dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users_list = cursor.fetchall()
    conn.close()
    return {user['email']: dict(user) for user in users_list}

def get_all_users_list() -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, role, cpf FROM users ORDER BY role DESC, name ASC")
    users_list = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return users_list

def add_product(name: str, description: str, price: float, stock: int, image_path: str = None) -> bool:
    """Adiciona um novo produto com o caminho da imagem, registrando erros SQL."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO products (name, description, price, stock, image_path) VALUES (?, ?, ?, ?, ?)",
            (name, description, price, stock, image_path)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"ERRO SQL ao adicionar produto '{name}': {e}")
        return False
    finally:
        conn.close()

def get_all_products() -> List[Dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY name ASC")
    products_list = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return products_list

def add_order(user_email: str, product_name: str, quantity: int, details: str, reference_image_path: str = None) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO orders (user_email, product_name, quantity, details, reference_image_path) VALUES (?, ?, ?, ?, ?)",
            (user_email, product_name, quantity, details, reference_image_path)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"ERRO SQL ao adicionar pedido: {e}")
        return False
    finally:
        conn.close()