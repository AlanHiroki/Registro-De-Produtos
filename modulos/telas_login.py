# Importações necessárias
import string  # Para manipulação de strings (ex: gerar senha)
import random  # Para gerar valores aleatórios (ex: senha)
import pymysql  # Para conexão com o banco de dados MySQL
from modulos.conexao import conexao  # Função personalizada para conectar ao banco de dados
from modulos.tela_principal import exibir_sucesso, exibir_falha  # Funções para exibir mensagens de sucesso/falha
from modulos.globais import produto_inicial  # Variável global para armazenar informações do funcionário
from PyQt6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout  # Componentes da interface gráfica
from PyQt6.QtGui import QIcon  # Para manipulação de ícones

# Função para gerar uma senha aleatória
def gerar_senha(tamanho=8):
    while True:
        conectar = conexao()  # Conecta ao banco de dados
        cursor = conectar.cursor()  # Cria um cursor para executar comandos SQL

        # Define os caracteres permitidos para a senha (letras maiúsculas e dígitos)
        caracteres = string.ascii_uppercase + string.digits
        # Gera uma senha aleatória com o tamanho especificado
        senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
        
        # Verifica se a senha já existe no banco de dados
        cursor.execute('SELECT senha FROM usuarios WHERE senha = %s', (senha,))
        tabela = cursor.fetchone()  # Obtém o resultado da consulta
        
        # Se a senha não existir no banco, retorna a senha gerada
        if tabela is None:
            conectar.close()  # Fecha a conexão com o banco de dados
            return senha

# Função para registrar um novo usuário
def registrar_usuario(registrar, sucesso, falha, main):
    try:
        conectar = conexao()  # Conecta ao banco de dados
        cursor = conectar.cursor()  # Cria um cursor para executar comandos SQL

        # Obtém o nome do usuário da interface e formata (primeira letra maiúscula)
        nome = registrar.txtNomeRegistrar.text().title().strip()
        # Gera uma senha aleatória
        senha = gerar_senha()

        # Insere o novo usuário no banco de dados
        cursor.execute('INSERT INTO usuarios (nome, senha) VALUES (%s, %s)', (nome, senha))
        conectar.commit()  # Confirma a transação

        conectar.close()  # Fecha a conexão com o banco de dados
        registrar.close()  # Fecha a tela de registro
        main.show()  # Exibe a tela principal de login

        # Exibe uma mensagem de sucesso com a senha gerada
        exibir_sucesso(sucesso, f'Registrado com sucesso, essa é sua senha: <strong>{senha}<strong> <br> (anote para não esquecer)')

    except pymysql.MySQLError:  # Captura erros do MySQL
        # Exibe uma mensagem de falha caso o nome já esteja registrado
        exibir_falha(falha, 'Nome já registrado <br> (tente colocar nome e sobrenome)')

# Função para validar o login do usuário
def login(main, registro, sucesso, falha):
    conectar = conexao()  # Conecta ao banco de dados
    cursor = conectar.cursor()  # Cria um cursor para executar comandos SQL

    try:
        # Obtém o nome e a senha da interface e formata
        nome = main.txtNomeLogin.text().title().split()
        senha = main.txtSenhaLogin.text().upper().split()

        # Verifica se o nome e a senha correspondem a um usuário no banco de dados
        cursor.execute('SELECT nome, senha FROM usuarios WHERE nome = %s AND senha = %s', (nome, senha))
        tabela = cursor.fetchall()  # Obtém o resultado da consulta

        if tabela:  # Se o usuário for encontrado
            main.close()  # Fecha a tela de login
            registro.show()  # Exibe a tela de registro de produtos
            # Exibe uma mensagem de sucesso com o nome do usuário
            exibir_sucesso(sucesso, f'BEM VINDO(a) {tabela[0][0]}')
            # Armazena o nome do funcionário na variável global
            produto_inicial.funcionario = tabela[0][0]
        else:  # Se o usuário não for encontrado
            # Exibe uma mensagem de falha
            exibir_falha(falha, 'errou no login <br> nome ou senha invalidos')
    except pymysql.MySQLError:  # Captura erros do MySQL
        # Exibe uma mensagem de falha caso ocorra um erro
        exibir_falha(falha, 'POR FAVOR INSIRA OS DADOS CORRETAMENTE')

# Função para mostrar/esconder a senha na interface de login
def mostrar_senha(main):
    if main.txtSenhaLogin.echoMode() == QLineEdit.EchoMode.Password:  # Se a senha estiver oculta
        main.txtSenhaLogin.setEchoMode(QLineEdit.EchoMode.Normal)  # Mostra a senha
        main.btnMostrarSenha.setIcon(QIcon('./interface/eye.png'))  # Altera o ícone para "olho aberto"
    else:  # Se a senha estiver visível
        main.txtSenhaLogin.setEchoMode(QLineEdit.EchoMode.Password)  # Oculta a senha
        main.btnMostrarSenha.setIcon(QIcon('./interface/hidden.png'))  # Altera o ícone para "olho fechado"