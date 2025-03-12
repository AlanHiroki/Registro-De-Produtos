# Importações necessárias
from modulos.conexao import conexao  # Função personalizada para conectar ao banco de dados
from modulos.globais import botoes_pesquisar  # Variável global para armazenar os botões de pesquisa
from modulos.tela_produtos import mostrarTabela  # Função para exibir os dados na tabela
from modulos.tela_principal import btnAtualizar  # Função para atualizar a tabela de produtos
from PyQt6.QtWidgets import QCheckBox  # Componente de checkbox da interface gráfica
from datetime import date  # Para manipulação de datas

# Função para marcar/desmarcar todos os checkboxes de pesquisa
def marcarTodos(marcado, itens):
    # Define os botões que devem ser habilitados/desabilitados ao marcar/desmarcar todos
    botoes_ate = {
        tuple(botoes_pesquisar.check_ate_todos),
        tuple(botoes_pesquisar.label_todos2),
        tuple(botoes_pesquisar.input_todos2),
        tuple(botoes_pesquisar.label_ate_todos)
    }

    if marcado:  # Se todos os checkboxes forem marcados
        for i in itens:
            if i in botoes_pesquisar.check_todos:
                i.setChecked(True)  # Marca o checkbox

            if not any(i in itens for itens in botoes_ate):
                i.setEnabled(True)  # Habilita o checkbox

        botoes_pesquisar.check_marcado_todos.setChecked(True)  # Marca o checkbox "Todos"

    else:  # Se todos os checkboxes forem desmarcados
        for i in itens:
            if i in botoes_pesquisar.check_todos:
                i.setChecked(False)  # Desmarca o checkbox
            else:
                i.setEnabled(False)  # Desabilita o checkbox

        botoes_pesquisar.check_marcado_todos.setChecked(False)  # Desmarca o checkbox "Todos"

# Função para habilitar/desabilitar os campos de "Até" na pesquisa
def marcadorEntre(marcado, ate, label, input):
    if marcado:  # Se o checkbox "Até" for marcado
        ate.setEnabled(True)  # Habilita o checkbox "Até"
        label.setEnabled(True)  # Habilita o label correspondente
        input.setEnabled(True)  # Habilita o campo de entrada correspondente
    else:  # Se o checkbox "Até" for desmarcado
        ate.setEnabled(False)  # Desabilita o checkbox "Até"
        label.setEnabled(False)  # Desabilita o label correspondente
        input.setEnabled(False)  # Desabilita o campo de entrada correspondente

# Função para habilitar/desabilitar os campos de pesquisa com intervalo
def marcadorHabilitarEntre(marcado, ate, label, input, ate_label, label2, input2, ate_check):
    if marcado:  # Se o checkbox for marcado
        if all(marcador.isChecked() for marcador in botoes_pesquisar.check_todos):
            botoes_pesquisar.check_marcado_todos.setChecked(True)  # Marca o checkbox "Todos"

        ate.setEnabled(True)  # Habilita o checkbox "Até"
        label.setEnabled(True)  # Habilita o label correspondente
        input.setEnabled(True)  # Habilita o campo de entrada correspondente
    else:  # Se o checkbox for desmarcado
        botoes_pesquisar.check_marcado_todos.setChecked(False)  # Desmarca o checkbox "Todos"

        ate.setEnabled(False)  # Desabilita o checkbox "Até"
        label.setEnabled(False)  # Desabilita o label correspondente
        input.setEnabled(False)  # Desabilita o campo de entrada correspondente
        ate_label.setEnabled(False)  # Desabilita o label "Até"
        label2.setEnabled(False)  # Desabilita o segundo label
        input2.setEnabled(False)  # Desabilita o segundo campo de entrada
        ate_check.setChecked(False)  # Desmarca o checkbox "Até"

# Função para habilitar/desabilitar os campos de pesquisa
def marcadorHabilitar(marcado, label, input):
    if marcado:  # Se o checkbox for marcado
        if all(marcador.isChecked() for marcador in botoes_pesquisar.check_todos):
            botoes_pesquisar.check_marcado_todos.setChecked(True)  # Marca o checkbox "Todos"

        label.setEnabled(True)  # Habilita o label correspondente
        input.setEnabled(True)  # Habilita o campo de entrada correspondente
    else:  # Se o checkbox for desmarcado
        botoes_pesquisar.check_marcado_todos.setChecked(False)  # Desmarca o checkbox "Todos"

        label.setEnabled(False)  # Desabilita o label correspondente
        input.setEnabled(False)  # Desabilita o campo de entrada correspondente

# Lista de checkboxes de pesquisa
marcadores = [
    botoes_pesquisar.check_nome,
    botoes_pesquisar.check_categoria,
    botoes_pesquisar.check_id,
    botoes_pesquisar.check_preco,
    botoes_pesquisar.check_quantidade,
    botoes_pesquisar.check_data
]

# Função para realizar a pesquisa com base nos critérios selecionados
def btnPesquisar(produtos):
    conectar = conexao()  # Conecta ao banco de dados
    cursor = conectar.cursor()  # Cria um cursor para executar comandos SQL

    # Lista de nomes dos campos de pesquisa no banco de dados
    nomes_marcadores = ['Nome', 'Categoria', 'Id', 'Preco', 'Quantidade', 'Data_registro']
    # Lista de valores dos campos de pesquisa
    pesquisar_valores = [
        botoes_pesquisar.input_nome.text(),
        botoes_pesquisar.input_categoria.currentText(),
        botoes_pesquisar.input_id.value(),
        botoes_pesquisar.input_preco.value(),
        botoes_pesquisar.input_quantidade.value(),
        botoes_pesquisar.input_data.date().toString('yyyy-MM-dd')
    ]

    # Filtra os nomes e valores dos campos marcados
    nomes_marcados = [nomes_marcadores[i] for i in range(len(marcadores)) if marcadores[i].isChecked()]
    informacoes_marcados = [pesquisar_valores[i] for i in range(len(marcadores)) if marcadores[i].isChecked()]

    if nomes_marcados:  # Se houver campos marcados para pesquisa
        sql = 'SELECT * FROM produtos WHERE '  # Inicia a consulta SQL
        condicoes = []  # Lista para armazenar as condições da consulta
        parametros = []  # Lista para armazenar os parâmetros da consulta

        # Constrói as condições da consulta com base nos campos marcados
        for nome, valor in zip(nomes_marcados, informacoes_marcados):
            if nome in ['Nome', 'Categoria']:  # Para campos de texto (busca parcial)
                condicoes.append(f'{nome} LIKE %s')
                parametros.append(f'%{valor}%')
            else:  # Para campos numéricos ou de data (busca exata ou intervalo)
                if nome == 'Id' and botoes_pesquisar.check_ate_id.isChecked():
                    condicoes.append(f'{nome} BETWEEN %s AND %s')
                    parametros.append(valor)
                    parametros.append(botoes_pesquisar.input_id2.value())

                elif nome == 'Preço' and botoes_pesquisar.check_ate_preco.isChecked():
                    condicoes.append(f'{nome} BETWEEN %s AND %s')
                    parametros.append(valor)
                    parametros.append(botoes_pesquisar.input_preco2.value())

                elif nome == 'Quantidade' and botoes_pesquisar.check_ate_quantidade.isChecked():
                    condicoes.append(f'{nome} BETWEEN %s AND %s')
                    parametros.append(valor)
                    parametros.append(botoes_pesquisar.input_quantidade2.value())

                elif nome == 'Data_registro' and botoes_pesquisar.check_ate_data.isChecked():
                    condicoes.append(f'{nome} BETWEEN %s AND %s')
                    parametros.append(valor)
                    parametros.append(botoes_pesquisar.input_data2.date().toString('yyyy-MM-dd'))

                else:  # Para busca exata
                    condicoes.append(f'{nome} = %s')
                    parametros.append(valor)

        # Junta as condições com "AND" e executa a consulta
        sql += ' AND '.join(condicoes)
        cursor.execute(sql, tuple(parametros))
        tabela = cursor.fetchall()  # Obtém os resultados da consulta
        conectar.commit()  # Confirma a transação

        if tabela:  # Se houver resultados
            mostrarTabela(produtos, tabela)  # Exibe os resultados na tabela
        else:  # Se não houver resultados
            produtos.tableWidget.setRowCount(0)  # Limpa a tabela
            produtos.tableWidget.setColumnCount(0)

# Função para limpar os campos de pesquisa
def btnLimparPesquisa(itens, produtos):
    for i in itens:  # Percorre todos os itens de pesquisa
        if isinstance(i, QCheckBox):  # Se for um checkbox
            i.setChecked(False)  # Desmarca o checkbox

            if i in botoes_pesquisar.check_ate_todos:
                i.setEnabled(False)  # Desabilita o checkbox "Até"
        else:  # Se for outro tipo de item
            i.setEnabled(False)  # Desabilita o item

    # Limpa os campos de entrada
    botoes_pesquisar.input_nome.setText('')
    botoes_pesquisar.input_categoria.setCurrentIndex(0)

    # Função auxiliar para definir valores padrão nos campos numéricos
    def set_input_values(input1, input2, value):
        input1.setValue(value)
        input2.setValue(value)

    # Define valores padrão nos campos de ID, quantidade, preço e data
    set_input_values(botoes_pesquisar.input_id, botoes_pesquisar.input_id2, 0)
    set_input_values(botoes_pesquisar.input_quantidade, botoes_pesquisar.input_quantidade2, 0)
    set_input_values(botoes_pesquisar.input_preco, botoes_pesquisar.input_preco2, 0)
    botoes_pesquisar.input_data.setDate(date.today())
    botoes_pesquisar.input_data2.setDate(date.today())

    # Atualiza a tabela de produtos
    btnAtualizar(produtos)