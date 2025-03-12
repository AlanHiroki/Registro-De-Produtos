# Importações necessárias
import pymysql  # Biblioteca para conexão com o MySQL
from pymysql import Error  # Para capturar erros específicos do MySQL

# Função para estabelecer a conexão com o banco de dados
def conexao():
    try:
        # Tenta estabelecer a conexão com o banco de dados
        conexao = pymysql.connect(
            host='127.0.0.1',  # Endereço do servidor MySQL (localhost)
            user='root',  # Nome de usuário do banco de dados
            password='123456',  # Senha do banco de dados
            database='registro_produtos'  # Nome do banco de dados
        )
        return conexao  # Retorna a conexão estabelecida
    
    except Error as e:  # Captura erros específicos do MySQL
        print(f"Erro ao conectar ao MySQL: {e}")  # Exibe uma mensagem de erro
        return None  # Retorna None em caso de falha na conexão