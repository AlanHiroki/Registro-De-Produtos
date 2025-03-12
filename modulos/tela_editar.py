# Importações necessárias
from modulos import tela_principal  # Módulo para funções da tela principal
from modulos.conexao import conexao  # Função personalizada para conectar ao banco de dados
from modulos.globais import produto_inicial  # Variável global para armazenar informações do produto
from PyQt6.QtCore import QTimer  # Para manipulação de temporizadores
from pymysql.err import IntegrityError  # Para capturar erros de integridade do MySQL
from PyQt6.QtCore import QDate  # Para manipulação de datas
import json  # Para manipulação de dados no formato JSON

# Função para carregar os dados do produto selecionado na tela de edição
def btnEditar(produtos, editar, falha):
    dados = produtos.tableWidget.currentRow()  # Obtém a linha selecionada na tabela
    id_item = produtos.tableWidget.item(dados, 0)  # Obtém o ID do produto selecionado
    try:
        if id_item:
            produto_inicial.id_ativo = int(id_item.text())  # Armazena o ID do produto selecionado na variável global

        conectar = conexao()  # Conecta ao banco de dados
        cursor = conectar.cursor()  # Cria um cursor para executar comandos SQL

        # Obtém os dados do produto selecionado
        cursor.execute('SELECT * FROM produtos WHERE id = %s', (produto_inicial.id_ativo))
        tabela = cursor.fetchall()

        editar.show()  # Exibe a tela de edição

        # Armazena os dados iniciais do produto na variável global
        produto_inicial.num_id_geral = produto_inicial.id_ativo
        produto_inicial.id_inicial = produto_inicial.id_historico = int(tabela[0][0])
        editar.sbAlterarId.setValue(int(tabela[0][0]))  # Define o ID na tela de edição

        produto_inicial.nome_inicial = produto_inicial.nome_historico = str(tabela[0][1])
        editar.txtAlterarNome.setText(str(tabela[0][1]))  # Define o nome na tela de edição

        produto_inicial.categorioa_inicial = produto_inicial.categoria_historico = str(tabela[0][2])
        editar.cbxAlterarCategoria.setCurrentText(str(tabela[0][2]))  # Define a categoria na tela de edição

        produto_inicial.preco_inicial = produto_inicial.preco_historico = float(tabela[0][3])
        editar.dsbAlterarPreco.setValue(float(tabela[0][3]))  # Define o preço na tela de edição

        produto_inicial.quantidade_inicial = produto_inicial.quantidade_historico = int(tabela[0][4])
        editar.sbAlterarQuantidade.setValue(int(tabela[0][4]))  # Define a quantidade na tela de edição

        data_str = str(tabela[0][5])  # Obtém a data do produto
        data_formatada = QDate.fromString(data_str, 'yyyy-MM-dd')  # Converte a data para o formato QDate
        produto_inicial.data_inicial = produto_inicial.data_historico = data_formatada  # Armazena a data na variável global
        editar.deAlterarData.setDate(data_formatada)  # Define a data na tela de edição

    except AttributeError:  # Caso nenhuma linha seja selecionada
        tela_principal.exibir_falha(falha, 'POR FAVOR SELECIONE UM LINHA DA TABELA')  # Exibe uma mensagem de falha

# Função para restaurar os valores iniciais do produto na tela de edição
def btnRestaurar(editar):
    editar.sbAlterarId.setValue(produto_inicial.id_inicial)  # Restaura o ID
    editar.txtAlterarNome.setText(produto_inicial.nome_inicial)  # Restaura o nome
    editar.cbxAlterarCategoria.setCurrentText(produto_inicial.categorioa_inicial)  # Restaura a categoria
    editar.dsbAlterarPreco.setValue(produto_inicial.preco_inicial)  # Restaura o preço
    editar.sbAlterarQuantidade.setValue(produto_inicial.quantidade_inicial)  # Restaura a quantidade
    editar.deAlterarData.setDate(produto_inicial.data_inicial)  # Restaura a data

# Função para salvar as alterações feitas no produto
def btnEditorSalvar(editar, sucesso, falha, produtos):
    # Obtém os dados alterados da tela de edição
    id = editar.sbAlterarId.value()
    nome = editar.txtAlterarNome.text().title().strip()
    categoria = editar.cbxAlterarCategoria.currentText()
    preco = editar.dsbAlterarPreco.value()
    quantidade = editar.sbAlterarQuantidade.value()
    data = editar.deAlterarData.date()
    data_str = data.toString('yyyy-MM-dd')  # Formata a data como string

    conectar = conexao()  # Conecta ao banco de dados
    cursor = conectar.cursor()  # Cria um cursor para executar comandos SQL

    try:
        # Atualiza os dados do produto no banco de dados
        cursor.execute('UPDATE produtos SET id=%s, nome=%s, categoria=%s, preco=%s, quantidade=%s, data_registro=%s WHERE id = %s',
                       (id, nome, categoria, preco, quantidade, data_str, produto_inicial.id_inicial))
        conectar.commit()  # Confirma a transação

        # Prepara os dados para o histórico
        sql = "INSERT INTO historico (funcionario, acao, nome, produto, produto_editado) VALUES(%s, %s, %s, %s, %s)"

        # Dados do produto antes da edição
        produtos_antes = {
            'id': produto_inicial.id_historico,
            'nome': produto_inicial.nome_historico,
            'categoria': produto_inicial.categoria_historico,
            'preco': produto_inicial.preco_historico,
            'quantidade': produto_inicial.quantidade_historico,
            'data': produto_inicial.data_historico.toString('yyyy-MM-dd')
        }

        # Dados do produto após a edição
        produtos_depois = {
            'id': id,
            'nome': nome,
            'categoria': categoria,
            'preco': preco,
            'quantidade': quantidade,
            'data': data_str
        }

        # Insere os dados no histórico
        tudo = (produto_inicial.funcionario, 'EDITOU', produto_inicial.nome_historico, json.dumps(produtos_antes, ensure_ascii=False), json.dumps(produtos_depois, ensure_ascii=False))
        cursor.execute(sql, tudo)
        conectar.commit()

        # Exibe uma mensagem de sucesso
        tela_principal.exibir_sucesso(sucesso, 'PRODUTO editado com SUCESSO')

        # Atualiza a tabela de produtos e fecha a tela de edição
        tela_principal.btnAtualizar(produtos)
        editar.close()
        QTimer.singleShot(2000, sucesso.close)  # Fecha a janela de sucesso após 2 segundos

    except IntegrityError as e:  # Captura erros de integridade (ex: ID ou nome duplicado)
        if e.args[0] == 1062:  # Código de erro para registro duplicado
            tela_principal.exibir_falha(falha, 'ID ou NOME JÁ REGISTRADO')  # Exibe uma mensagem de falha