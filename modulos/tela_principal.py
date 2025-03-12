# Importações necessárias
from PyQt6.QtCore import QTimer  # Para manipulação de temporizadores
from datetime import date, datetime  # Para manipulação de datas
from modulos.conexao import conexao  # Função personalizada para conectar ao banco de dados
from pymysql.err import IntegrityError  # Para capturar erros de integridade do MySQL
from modulos import tela_produtos  # Módulo para manipulação da tela de produtos
from modulos.globais import produto_inicial  # Variável global para armazenar informações do produto
import json  # Para manipulação de dados no formato JSON

# Função para salvar um novo produto no banco de dados
def btnSalvar(main, sucesso, falha, produtos):
    # Obtém os dados do formulário
    nome_produto = main.txtNome.text().title().strip()  # Nome do produto (formatado)
    categoria_produto = main.cbxCategoria.currentText()  # Categoria selecionada
    preco_produto = main.dsbPreco.value()  # Preço do produto
    quantidade_produto = main.sbQuantidade.value()  # Quantidade do produto
    data_produto = main.deData.date()  # Data de registro
    data_str = data_produto.toString('yyyy-MM-dd')  # Formata a data como string

    conectar = conexao()  # Conecta ao banco de dados
    cursor = conectar.cursor()  # Cria um cursor para executar comandos SQL

    # Valida se o nome do produto foi preenchido
    if nome_produto == '':
        falha.lblFalha.setText('POR FAVOR DIGITE UM NOME')  # Exibe mensagem de erro
        falha.adjustSize()  # Ajusta o tamanho da janela de falha
        largura_lbl = falha.lblFalha.sizeHint().width() + 30
        falha.resize(largura_lbl, 100)  # Redimensiona a janela de falha
        falha.show()  # Exibe a janela de falha
    else:
        try:
            # Insere o novo produto no banco de dados
            sql_produtos = "INSERT INTO produtos (nome, categoria, preco, quantidade, data_registro) VALUES (%s, %s, %s, %s, %s)"
            data_produtos = (str(nome_produto), str(categoria_produto), str(preco_produto), str(quantidade_produto), str(data_str))
            cursor.execute(sql_produtos, data_produtos)
            conectar.commit()  # Confirma a transação

            # Limpa os campos do formulário após o registro
            main.txtNome.setText('')
            main.cbxCategoria.setCurrentIndex(0)
            main.dsbPreco.setValue(0)
            main.sbQuantidade.setValue(0)
            main.deData.setDate(date.today())  # Define a data atual

            # Formata o preço para exibição
            preco_formatado = f"{preco_produto:.2f}"

            # Obtém o ID do produto recém-registrado
            cursor.execute('SELECT id FROM produtos WHERE nome = %s', (nome_produto))
            id_produto = cursor.fetchall()

            # Prepara os dados para o histórico
            sql_historico = "INSERT INTO historico (funcionario, acao, nome, produto) VALUES(%s, %s, %s, %s)"
            dados_json = {
                "id": id_produto[0][0],
                "nome": nome_produto,
                "categoria": categoria_produto,
                "preco": preco_formatado,
                "quantidade": quantidade_produto,
                "data": data_str
            }
            data_historico = (str(produto_inicial.funcionario), 'CRIOU', str(nome_produto), json.dumps(dados_json, ensure_ascii=False))

            # Insere os dados no histórico
            cursor.execute(sql_historico, data_historico)
            conectar.commit()

            # Exibe uma mensagem de sucesso
            exibir_sucesso(sucesso, 'Produto registrado com SUCESSO')

            # Fecha a janela de sucesso após 2 segundos
            QTimer.singleShot(2000, sucesso.close)

        except IntegrityError as e:  # Captura erros de integridade (ex: produto duplicado)
            if e.args[0] == 1062:  # Código de erro para registro duplicado
                exibir_falha(falha, 'PRODUTO JÁ REGISTRADO')
        
        # Atualiza a tabela de produtos após o registro
        btnAtualizar(produtos)

# Função para limpar os campos do formulário
def btnLimpar(main):
    main.txtNome.setText('')  # Limpa o campo de nome
    main.cbxCategoria.setCurrentIndex(0)  # Reseta a categoria
    main.dsbPreco.setValue(0)  # Reseta o preço
    main.sbQuantidade.setValue(0)  # Reseta a quantidade
    main.deData.setDate(date.today())  # Define a data atual

# Função para fechar uma janela
def btnFechar(btnContinuar):
    btnContinuar.close()  # Fecha a janela

# Função para abrir a tela de produtos
def btnProduto(produtos):
    btnAtualizar(produtos)  # Atualiza a tabela de produtos
    produtos.show()  # Exibe a tela de produtos

# Função para atualizar a tabela de produtos
def btnAtualizar(produtos):
    # Ajusta o tamanho das colunas e linhas da tabela
    produtos.tableWidget.resizeColumnsToContents()
    produtos.tableWidget.resizeRowsToContents()

    conectar = conexao()  # Conecta ao banco de dados
    cursor = conectar.cursor()  # Cria um cursor para executar comandos SQL

    # Busca todos os produtos no banco de dados
    sql = 'SELECT * FROM produtos'
    cursor.execute(sql)
    tabela = cursor.fetchall()  # Obtém os resultados da consulta

    # Exibe os produtos na tabela
    tela_produtos.mostrarTabela(produtos, tabela)

# Função para exibir uma mensagem de sucesso
def exibir_sucesso(sucesso, txt):
    sucesso.lblSucesso.setText(txt)  # Define o texto da mensagem
    sucesso.adjustSize()  # Ajusta o tamanho da janela
    largura_lbl = sucesso.lblSucesso.sizeHint().width() + 30
    sucesso.resize(largura_lbl, 100)  # Redimensiona a janela
    sucesso.show()  # Exibe a janela

# Função para exibir uma mensagem de falha
def exibir_falha(falha, txt):
    falha.lblFalha.setText(txt)  # Define o texto da mensagem
    falha.adjustSize()  # Ajusta o tamanho da janela
    largura_lbl = falha.lblFalha.sizeHint().width() + 30
    falha.resize(largura_lbl, 100)  # Redimensiona a janela
    falha.show()  # Exibe a janela