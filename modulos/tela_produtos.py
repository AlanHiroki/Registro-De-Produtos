# Importações necessárias
from modulos.conexao import conexao  # Função personalizada para conectar ao banco de dados
from PyQt6.QtCore import QDate  # Para manipulação de datas
from modulos import globais, tela_principal  # Módulos globais e de tela principal
from PyQt6.QtCore import QTimer  # Para manipulação de temporizadores
from PyQt6 import QtWidgets, QtCore  # Componentes da interface gráfica
from datetime import datetime  # Para manipulação de datas e horas
from modulos.globais import produto_inicial  # Variável global para armazenar informações do produto
import json  # Para manipulação de dados no formato JSON

# Função para exibir os dados na tabela de produtos
def mostrarTabela(produtos, tabela):
    try:
        # Define o número de linhas e colunas da tabela com base nos dados recebidos
        produtos.tableWidget.setRowCount(len(tabela))
        produtos.tableWidget.setColumnCount(len(tabela[0]))

        # Preenche a tabela com os dados
        for r in range(0, len(tabela)):
            for c in range(0, len(tabela[0])):
                if c == 3:  # Coluna de preço (formatação monetária)
                    preco = float(tabela[r][c])
                    preco_formatado = (f'R${preco:,.2f}')  # Formata o preço como moeda
                    item = QtWidgets.QTableWidgetItem(preco_formatado)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Centraliza o texto
                    produtos.tableWidget.setItem(r, c, item)

                elif c == 5:  # Coluna de data (formatação de data)
                    dia = (str(tabela[r][c]))

                    try:
                        # Converte a data para o formato brasileiro (dd/MM/yyyy)
                        data = datetime.strptime(dia, '%Y-%m-%d')
                        data_formatada_str = data.strftime('%d/%m/%Y')
                        item = QtWidgets.QTableWidgetItem(data_formatada_str)
                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Centraliza o texto
                        produtos.tableWidget.setItem(r, c, item)
                        
                    except ValueError:  # Caso a data não esteja no formato esperado
                        data_formatada_str = dia
                        item = QtWidgets.QTableWidgetItem(data_formatada_str)
                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Centraliza o texto
                        produtos.tableWidget.setItem(r, c, item)

                else:  # Outras colunas (sem formatação especial)
                    item = QtWidgets.QTableWidgetItem(str(tabela[r][c]))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Centraliza o texto
                    produtos.tableWidget.setItem(r, c, item)

        # Ajusta o tamanho das colunas e linhas para se adequar ao conteúdo
        produtos.tableWidget.resizeColumnsToContents()
        produtos.tableWidget.resizeRowsToContents()
        
        # Define um limite máximo para a largura das colunas
        for c in range(produtos.tableWidget.columnCount()):
            produtos.tableWidget.setColumnWidth(c, min(produtos.tableWidget.columnWidth(c), 300))

        # Calcula a largura total da tabela, incluindo a barra de rolagem e os botões
        rolagem_largura = produtos.tableWidget.verticalScrollBar().sizeHint().width()
        table_largura = produtos.tableWidget.horizontalHeader().length()
        table_altura = produtos.tableWidget.verticalHeader().length()
        botoes_largura = produtos.widgetBotoes.sizeHint().width()
        nova_largura = table_largura + botoes_largura + rolagem_largura + 30

        # Redimensiona a janela para se adequar ao conteúdo
        produtos.resize(nova_largura, table_altura)
    except IndexError:  # Caso a tabela esteja vazia ou ocorra um erro de índice
        pass

# Função para trocar o campo de pesquisa entre texto e data
def trocarInputData(produtos):
    def pesquisa_data():
        try:
            # Obtém a data selecionada no campo de pesquisa
            pesquisa = produtos.dateEditPesquisar.date().toString('yyyy-MM-dd')

            if pesquisa:
                # Busca os produtos com base na data selecionada
                cursor.execute("SELECT * FROM produtos WHERE {} = %s".format(onde), (pesquisa))
                tabela = cursor.fetchall()
            else:
                # Caso não haja data selecionada, busca todos os produtos
                cursor.execute("SELECT * FROM produtos")
                tabela = cursor.fetchall()

            if tabela:
                # Exibe os resultados na tabela
                mostrarTabela(produtos, tabela)
            else:
                # Limpa a tabela caso não haja resultados
                produtos.tableWidget.setRowCount(0)
                produtos.tableWidget.setColumnCount(0)

        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            produtos.tableWidget.setRowCount(0)
            produtos.tableWidget.setColumnCount(0)

    # Obtém o critério de pesquisa selecionado (ex: "Data", "Nome", etc.)
    onde = produtos.cbxPesquisar.currentText()
    conectar = conexao()
    cursor = conectar.cursor()

    if onde == 'Data':  # Se o critério for "Data"
        onde = 'data_registro'

        if not hasattr(produtos, 'dateEditPesquisar'):  # Se o campo de data ainda não foi criado
            # Cria um campo de seleção de data
            produtos.dateEditPesquisar = QtWidgets.QDateEdit(produtos)
            produtos.dateEditPesquisar.setCalendarPopup(True)  # Exibe um calendário ao clicar
            produtos.dateEditPesquisar.setDisplayFormat('dd/MM/yyyy')  # Formato da data
            produtos.dateEditPesquisar.setDate(datetime.today())  # Define a data atual

            # Substitui o campo de texto pelo campo de data
            layout = produtos.txtPesquisar.parentWidget().layout()
            layout.replaceWidget(produtos.txtPesquisar, produtos.dateEditPesquisar)

            produtos.txtPesquisar.hide()  # Oculta o campo de texto
            produtos.dateEditPesquisar.dateChanged.connect(pesquisa_data)  # Conecta a função de pesquisa

    else:  # Se o critério não for "Data"
        if hasattr(produtos, 'dateEditPesquisar'):  # Se o campo de data existir
            # Substitui o campo de data pelo campo de texto
            layout = produtos.dateEditPesquisar.parentWidget().layout()
            layout.replaceWidget(produtos.dateEditPesquisar, produtos.txtPesquisar)
            produtos.dateEditPesquisar.hide()  # Oculta o campo de data
            produtos.txtPesquisar.show()  # Exibe o campo de texto

# Função para pesquisar produtos com base no critério selecionado
def pesquisar(produtos):
    onde = produtos.cbxPesquisar.currentText()  # Obtém o critério de pesquisa
    pesquisa = produtos.txtPesquisar.text()  # Obtém o texto de pesquisa

    conectar = conexao()
    cursor = conectar.cursor()

    try:
        if onde == 'Nome' or onde == 'Categoria':  # Se o critério for "Nome" ou "Categoria"
            # Busca os produtos que contenham o texto de pesquisa
            cursor.execute("SELECT * FROM produtos WHERE {} LIKE %s ORDER BY id ASC".format(onde), (f'%{pesquisa}%'))
            tabela = cursor.fetchall()
        else:  # Para outros critérios (ex: "ID", "Preço")
            if pesquisa:
                if onde in 'Preço':  # Se o critério for "Preço"
                    onde = 'preco'
                # Busca os produtos com base no valor exato
                cursor.execute("SELECT * FROM produtos WHERE {} = %s ORDER BY id ASC".format(onde), (pesquisa))
                tabela = cursor.fetchall()
            else:
                # Caso não haja texto de pesquisa, busca todos os produtos
                cursor.execute("SELECT * FROM produtos ORDER BY id ASC")
                tabela = cursor.fetchall()

        if tabela:
            # Exibe os resultados na tabela
            mostrarTabela(produtos, tabela)
        else:
            # Limpa a tabela caso não haja resultados
            produtos.tableWidget.setRowCount(0)
            produtos.tableWidget.setColumnCount(0)

    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        produtos.tableWidget.setRowCount(0)
        produtos.tableWidget.setColumnCount(0)

# Função para preparar a exclusão de um produto
def btnExcluir(produtos, tela_excluir, falha):
    excluir = produtos.tableWidget.currentRow()  # Obtém a linha selecionada na tabela
    id_item = produtos.tableWidget.item(excluir, 0)  # Obtém o ID do produto selecionado
    try:
        if id_item:
            # Armazena o ID do produto selecionado na variável global
            produto_inicial.id_ativo = int(id_item.text())
        conectar = conexao()
        cursor = conectar.cursor()

        # Busca o nome do produto selecionado
        cursor.execute('SELECT nome FROM produtos WHERE id = %s', (produto_inicial.id_ativo))
        nome = cursor.fetchone()

        # Exibe o nome do produto na tela de exclusão
        tela_excluir.lblItem.setText(f'{nome[0]}')

        # Busca os dados do produto para o histórico
        cursor.execute('SELECT * FROM produtos WHERE id = %s', (produto_inicial.id_ativo))
        historico = cursor.fetchall()

        # Armazena os dados do produto na variável global
        produto_inicial.id_historico = int(historico[0][0])
        produto_inicial.nome_historico = str(historico[0][1])
        produto_inicial.categoria_historico = str(historico[0][2])
        produto_inicial.preco_historico = float(historico[0][3])
        produto_inicial.quantidade_historico = int(historico[0][4])
        data_str = str(historico[0][5])
        data_formatada = QDate.fromString(data_str, 'yyyy-MM-dd')
        produto_inicial.data_historico = data_formatada
        
        # Ajusta o tamanho da tela de exclusão e a exibe
        nome_tamanho = tela_excluir.nomeLayout.sizeHint().width() + 20
        tela_excluir.resize(nome_tamanho, 120)
        tela_excluir.show()

    except AttributeError:  # Caso nenhuma linha seja selecionada
        tela_principal.exibir_falha(falha, 'POR FAVOR SELECIONE UM LINHA DA TABELA')

# Função para confirmar a exclusão de um produto
def btnExcluirSim(excluir, produtos):
    conectar = conexao()
    cursor = conectar.cursor()

    # Prepara os dados do produto excluído para o histórico
    produtos_excluidos = {
        'id': produto_inicial.id_historico,
        'nome': produto_inicial.nome_historico,
        'categoria': produto_inicial.categoria_historico,
        'preco': produto_inicial.preco_historico,
        'quantidade': produto_inicial.quantidade_historico,
        'data': produto_inicial.data_historico.toString('yyyy-MM-dd')
    }
    
    # Insere os dados do produto excluído no histórico
    cursor.execute('INSERT INTO historico (funcionario, acao, nome, produto) VALUES (%s, %s, %s, %s)',
                   (produto_inicial.funcionario, 'EXCLUIU', produto_inicial.nome_historico, json.dumps(produtos_excluidos, ensure_ascii=False)))
    conectar.commit()

    # Remove o produto da tabela de produtos
    cursor.execute('DELETE FROM produtos WHERE id = %s', (produto_inicial.id_ativo))
    conectar.commit()

    # Fecha a tela de exclusão e atualiza a tabela de produtos
    excluir.close()
    tela_principal.btnAtualizar(produtos)

# Função para abrir uma nova aba
def abrir(aba):
    aba.show()

# Função para fechar uma aba e abrir outra
def fechar_abrir(aba1, aba2):
    aba1.close()
    aba2.show()