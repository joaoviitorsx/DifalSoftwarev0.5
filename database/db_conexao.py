import mysql.connector
from mysql.connector import Error
from utils.mensagem import mensagem_error

# Configurações do Banco de Dados
HOST = "localhost"
USER = "root"
PASSWORD = "1234"
DATABASE = "empresas_db"

def conectar_banco():
    """Conecta ao banco de dados e cria a estrutura se necessário."""
    conexao = None
    try:
        conexao = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            port="3306"
        )
        criar_banco(conexao)  # Criar o banco se não existir
        conexao.close()

        conexao = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            port="3306",
            database=DATABASE
        )
        criar_tabela_empresa(conexao)  # Criar a tabela de empresas se necessário
        return conexao

    except mysql.connector.Error as err:
        mensagem_error(f"Erro ao conectar ao banco de dados: {err}")

def criar_banco(conexao):
    """Cria o banco de dados se ele não existir."""
    cursor = conexao.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        conexao.commit()
    except mysql.connector.Error as err:
        mensagem_error(f"Erro ao criar o banco de dados: {err}")
        conexao.rollback()
    finally:
        cursor.close()

def criar_tabela_empresa(conexao):
    """Cria a tabela de empresas se ela não existir."""
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cnpj VARCHAR(20) UNIQUE NOT NULL,
            razao_social VARCHAR(255) NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conexao.commit()
    cursor.close()

def cadastrar_empresa(conexao, cnpj, razao_social):
    """Cadastra uma nova empresa no banco de dados."""
    cursor = conexao.cursor()
    try:
        cursor.execute("INSERT INTO empresas (cnpj, razao_social) VALUES (%s, %s)", (cnpj, razao_social))
        conexao.commit()
    except mysql.connector.IntegrityError:
        mensagem_error("CNPJ já cadastrado!")
    except mysql.connector.Error as err:
        mensagem_error(f"Erro ao cadastrar empresa: {err}")
    finally:
        cursor.close()

def listar_empresas(conexao):
    """Retorna uma lista de empresas cadastradas."""
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id, cnpj, razao_social FROM empresas ORDER BY razao_social")
    empresas = cursor.fetchall()
    cursor.close()
    return empresas

def fechar_banco(conexao):
    """Fecha a conexão com o banco de dados."""
    if conexao and conexao.is_connected():
        conexao.close()
