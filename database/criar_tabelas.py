
def criar_tabelas(cursor):
    """Cria apenas a tabela de empresas."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cnpj VARCHAR(20) UNIQUE NOT NULL,
            razao_social VARCHAR(255) NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
