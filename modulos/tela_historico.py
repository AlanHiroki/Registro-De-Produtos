# Importações necessárias
from modulos.conexao import conexao  # Função personalizada para conectar ao banco de dados
from modulos.globais import produto_inicial  # Variável global para armazenar informações do produto
from modulos import tela_principal  # Módulo para funções da tela principal
from datetime import datetime  # Para manipulação de datas e horas
from PyQt6 import QtWidgets, QtCore  # Componentes da interface gráfica
import json  # Para manipulação de dados no formato JSON

# Função para trocar o campo de pesquisa entre texto e data
def trocarInputDataHistorico(historico):
    def pesquisa_data_historico():
        try:
            # Obtém a data selecionada no campo de pesquisa
            pesquisa = historico.dateEditPesquisarHistorico.date().toString('yyyy-MM-dd')

            if pesquisa:
                # Busca os registros de histórico com base na data selecionada
                cursor.execute("SELECT funcionario, acao, nome, data_atual FROM historico WHERE DATE({}) = %s ORDER BY id DESC".format(onde), (pesquisa))
                tabela = cursor.fetchall()
            else:
                # Caso não haja data selecionada, busca todos os registros de histórico
                cursor.execute("SELECT funcionario, acao, nome, data_atual FROM historico ORDER BY id DESC")
                tabela = cursor.fetchall()

            if tabela:
                # Exibe os resultados na tabela
                mostrarTabelaHistorico(historico, tabela)
            else:
                # Limpa a tabela caso não haja resultados
                historico.tableWidget.setRowCount(0)
                historico.tableWidget.setColumnCount(0)

        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            historico.tableWidget.setRowCount(0)
            historico.tableWidget.setColumnCount(0)

    # Obtém o critério de pesquisa selecionado (ex: "Data", "Ação", etc.)
    onde = historico.cbxPesquisarHistorico.currentText()
    conectar = conexao()
    cursor = conectar.cursor()

    if onde == 'Data':  # Se o critério for "Data"
        onde = 'data_atual'

        if not hasattr(historico, 'dateEditPesquisarHistorico'):  # Se o campo de data ainda não foi criado
            # Cria um campo de seleção de data
            historico.dateEditPesquisarHistorico = QtWidgets.QDateEdit(historico)
            historico.dateEditPesquisarHistorico.setCalendarPopup(True)  # Exibe um calendário ao clicar
            historico.dateEditPesquisarHistorico.setDisplayFormat('dd/MM/yyyy')  # Formato da data
            historico.dateEditPesquisarHistorico.setDate(datetime.today())  # Define a data atual

            # Substitui o campo de texto pelo campo de data
            layout = historico.txtPesquisarHistorico.parentWidget().layout()
            layout.replaceWidget(historico.txtPesquisarHistorico, historico.dateEditPesquisarHistorico)

            historico.txtPesquisarHistorico.hide()  # Oculta o campo de texto
            historico.dateEditPesquisarHistorico.dateChanged.connect(pesquisa_data_historico)  # Conecta a função de pesquisa

    else:  # Se o critério não for "Data"
        if hasattr(historico, 'dateEditPesquisarHistorico'):  # Se o campo de data existir
            # Substitui o campo de data pelo campo de texto
            layout = historico.dateEditPesquisarHistorico.parentWidget().layout()
            layout.replaceWidget(historico.dateEditPesquisarHistorico, historico.txtPesquisarHistorico)
            historico.dateEditPesquisarHistorico.hide()  # Oculta o campo de data
            historico.txtPesquisarHistorico.show()  # Exibe o campo de texto

# Função para pesquisar registros de histórico
def pesquisarHistorico(historico):
    onde = historico.cbxPesquisarHistorico.currentText()  # Obtém o critério de pesquisa
    pesquisa = historico.txtPesquisarHistorico.text()  # Obtém o texto de pesquisa

    conectar = conexao()
    cursor = conectar.cursor()

    try:
        if onde in 'Ação':  # Se o critério for "Ação"
            onde = 'acao'

        if onde:
            # Busca os registros de histórico com base no critério selecionado
            cursor.execute("SELECT funcionario, acao, nome, data_atual FROM historico WHERE {} LIKE %s ORDER BY id DESC".format(onde), (f'%{pesquisa}%'))
            tabela = cursor.fetchall()
        else:
            # Caso não haja critério selecionado, busca todos os registros de histórico
            cursor.execute("SELECT funcionario, acao, nome, data_atual FROM historico ORDER BY id DESC")
            tabela = cursor.fetchall()

        if tabela:
            # Exibe os resultados na tabela
            mostrarTabelaHistorico(historico, tabela)
        else:
            # Limpa a tabela caso não haja resultados
            historico.tableWidget.setRowCount(0)
            historico.tableWidget.setColumnCount(0)

    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        historico.tableWidget.setRowCount(0)
        historico.tableWidget.setColumnCount(0)

# Função para abrir a tela de histórico
def btnHistorico(historico):
    historico.show()  # Exibe a tela de histórico

    # Ajusta o tamanho das colunas e linhas da tabela
    historico.tableWidget.resizeColumnsToContents()
    historico.tableWidget.resizeRowsToContents()

    conectar = conexao()
    cursor = conectar.cursor()

    # Busca todos os registros de histórico ordenados por ID (do mais recente para o mais antigo)
    sql = 'SELECT funcionario, acao, nome, data_atual FROM historico ORDER BY id DESC'
    cursor.execute(sql)
    tabela = cursor.fetchall()

    # Exibe os registros na tabela
    mostrarTabelaHistorico(historico, tabela)

# Função para exibir os dados na tabela de histórico
def mostrarTabelaHistorico(produtos, tabela):
    try:
        # Define o número de linhas e colunas da tabela com base nos dados recebidos
        produtos.tableWidget.setRowCount(len(tabela))
        produtos.tableWidget.setColumnCount(len(tabela[0]))

        # Preenche a tabela com os dados
        for r in range(0, len(tabela)):
            for c in range(0, len(tabela[0])):
                if c == 3:  # Coluna de data (formatação de data e hora)
                    dia = str(tabela[r][c])
                    try:
                        # Converte a data para o formato brasileiro (dd/MM/yyyy HH:mm:ss)
                        data = datetime.strptime(dia, '%Y-%m-%d %H:%M:%S')
                        data_formatada_str = data.strftime('%d/%m/%Y %H:%M:%S')
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
        table_largura = produtos.tableWidget.horizontalHeader().length()
        table_altura = produtos.tableWidget.verticalHeader().length()
        botoes_largura = produtos.widgetBotoes.sizeHint().width()
        nova_largura = table_largura + botoes_largura + 50

        # Redimensiona a janela para se adequar ao conteúdo
        produtos.resize(nova_largura, table_altura)
    except IndexError:  # Caso a tabela esteja vazia ou ocorra um erro de índice
        pass

# Função para atualizar a tabela de histórico
def btnAtualizarHistorico(historico):
    # Ajusta o tamanho das colunas e linhas da tabela
    historico.tableWidget.resizeColumnsToContents()
    historico.tableWidget.resizeRowsToContents()

    conectar = conexao()
    cursor = conectar.cursor()

    # Busca todos os registros de histórico ordenados por ID (do mais recente para o mais antigo)
    sql = 'SELECT funcionario, acao, nome, data_atual FROM historico ORDER BY id DESC'
    cursor.execute(sql)
    tabela = cursor.fetchall()

    # Exibe os registros na tabela
    mostrarTabelaHistorico(historico, tabela)

# Função para exibir os detalhes de um registro de histórico
def btnDetalhes(historico, detalhes, falha, linha=None):
    conectar = conexao()
    cursor = conectar.cursor()
    try:
        linha = historico.tableWidget.currentRow()  # Obtém a linha selecionada na tabela
        data_item = historico.tableWidget.item(linha, 3).text()  # Obtém a data do registro selecionado
        data_sql = QtCore.QDateTime.fromString(data_item, 'dd/MM/yyyy HH:mm:ss')  # Converte a data para o formato SQL
        data_str = data_sql.toString('yyyy-MM-dd HH:mm:ss')  # Formata a data como string

        if data_sql:
            # Obtém o ID do registro selecionado
            cursor.execute('SELECT id FROM historico WHERE data_atual = %s', (data_str))
            tabela = cursor.fetchall()
            produto_inicial.id_ativo = int(tabela[0][0])  # Armazena o ID na variável global

        # Obtém os dados do registro selecionado
        cursor.execute('SELECT produto FROM historico WHERE id = %s', (produto_inicial.id_ativo))
        tabela = cursor.fetchall()
        produto_json = tabela[0][0]  # Obtém os dados do produto no formato JSON

        # Converte os dados JSON para um dicionário
        dados_json = json.loads(produto_json)

        # Extrai os dados do dicionário
        id = dados_json.get('id', '')
        nome = dados_json.get('nome', '')
        categoria = dados_json.get('categoria', '')
        preco = dados_json.get('preco', '')
        quantidade = dados_json.get('quantidade', '')
        data = dados_json.get('data', '')
        data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')  # Formata a data

        # Obtém a ação realizada (ex: "CRIOU", "EDITOU", etc.)
        cursor.execute('SELECT acao FROM historico WHERE id = %s', (produto_inicial.id_ativo))
        tabela = cursor.fetchall()
        acao = tabela[0][0]

        tam_maximo = 800  # Define o tamanho máximo de cada linha de texto

        if acao == 'EDITOU':  # Se a ação for "EDITOU"
            # Obtém os dados do produto após a edição
            cursor.execute('SELECT produto_editado FROM historico WHERE id = %s', (produto_inicial.id_ativo))
            tabela = cursor.fetchall()
            produto_novo_json = tabela[0][0]
            dados_json_novo = json.loads(produto_novo_json)

            # Extrai os dados do produto após a edição
            id_novo = dados_json_novo.get('id', '')
            nome_novo = dados_json_novo.get('nome', '')
            categoria_novo = dados_json_novo.get('categoria', '')
            preco_novo = dados_json_novo.get('preco', '')
            quantidade_novo = dados_json_novo.get('quantidade', '')
            data_novo = dados_json_novo.get('data', '')
            data_formatada_novo = datetime.strptime(data_novo, '%Y-%m-%d').strftime('%d/%m/%Y')

            # Cria o texto com os dados antigos e novos
            texto = f'''<b>ANTIGO</b> <br>
            Id: {id} | Nome: {nome} | Categoria: {categoria} | Preço: {preco} | Quantidade: {quantidade} | Data: {data_formatada}<br><br> 
            <b>NOVO</b>
            <br> Id: {id_novo} | Nome: {nome_novo} | Categoria: {categoria_novo} | Preço: {preco_novo} | Quantidade: {quantidade_novo} | Data: {data_formatada_novo}'''
        else:  # Se a ação não for "EDITOU"
            # Cria o texto com os dados do produto
            texto = f'Id: {id} | Nome: {nome} | Categoria: {categoria} | Preço: {preco} | Quantidade: {quantidade} | Data: {data_formatada}'

        # Divide o texto em partes para evitar que ultrapasse o tamanho máximo
        partes = texto.split(" | ")
        linhas = []
        linha_atual = ""

        for parte in partes:
            if len(linha_atual) + len(parte) < tam_maximo:
                linha_atual += (parte + " | ")
            else:
                linhas.append(linha_atual.strip())
                linha_atual = parte + " | "

        if linha_atual:
            linhas.append(linha_atual.strip())

        # Junta as partes do texto com quebras de linha
        texto_formatado = "<br>".join(linhas)
        detalhes.lblProduto.setText(texto_formatado)  # Exibe o texto na tela de detalhes
        detalhes.adjustSize()

        # Ajusta o tamanho da janela de detalhes com base no conteúdo
        largura_lbl = detalhes.lblProduto.sizeHint().width() + 400
        altura_lbl = detalhes.lblProduto.sizeHint().height() + 20
        detalhes.resize(largura_lbl, altura_lbl)

        detalhes.show()  # Exibe a tela de detalhes
    except AttributeError:  # Caso nenhuma linha seja selecionada
        tela_principal.exibir_falha(falha, 'POR FAVOR SELECIONE UM LINHA DA TABELA')