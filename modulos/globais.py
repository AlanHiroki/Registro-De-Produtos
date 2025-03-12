# Importações necessárias
from PyQt6.QtCore import QDate  # Para manipulação de datas
from datetime import date  # Para manipulação de datas

# Classe para armazenar as variáveis globais relacionadas ao produto
class produto_inicial:
    def __call__(self):
        # Variáveis para armazenar os dados iniciais do produto
        self.id_inicial = 0  # ID inicial do produto
        self.nome_inicial = ""  # Nome inicial do produto
        self.categorioa_inicial = ""  # Categoria inicial do produto
        self.preco_inicial = 0.0  # Preço inicial do produto
        self.quantidade_inicial = 0  # Quantidade inicial do produto
        self.data_inicial = QDate()  # Data inicial do produto (formato QDate)
        self.num_id_geral = 0  # ID geral do produto
        self.id_ativo = 0  # ID do produto atualmente selecionado

        # Variáveis para armazenar os dados históricos do produto
        self.id_historico = 0  # ID histórico do produto
        self.nome_historico = ''  # Nome histórico do produto
        self.categoria_historico = ''  # Categoria histórica do produto
        self.preco_historico = 0  # Preço histórico do produto
        self.quantidade_historico = 0  # Quantidade histórica do produto
        self.data_historico = QDate()  # Data histórica do produto (formato QDate)

        self.funcionario = ""  # Nome do funcionário responsável pela ação

# Classe para armazenar as variáveis globais relacionadas à interface de pesquisa
class interface_pesquisar:
    def __call__(self, pesquisar):
        # Checkboxes da interface de pesquisa
        self.check_nome = pesquisar.checkNome  # Checkbox para pesquisa por nome
        self.check_categoria = pesquisar.checkCategoria  # Checkbox para pesquisa por categoria
        self.check_id = pesquisar.checkId  # Checkbox para pesquisa por ID
        self.check_preco = pesquisar.checkPreco  # Checkbox para pesquisa por preço
        self.check_quantidade = pesquisar.checkQuantidade  # Checkbox para pesquisa por quantidade
        self.check_data = pesquisar.checkData  # Checkbox para pesquisa por data
        self.check_marcado_todos = pesquisar.checkTodos  # Checkbox para marcar/desmarcar todos
        self.check_todos = [self.check_nome, self.check_categoria, self.check_id, self.check_preco, self.check_quantidade, self.check_data]  # Lista de todos os checkboxes

        # Labels da interface de pesquisa
        self.label_nome = pesquisar.lblNome  # Label para o campo de nome
        self.label_categoria = pesquisar.lblCategoria  # Label para o campo de categoria
        self.label_id = pesquisar.lblId  # Label para o campo de ID
        self.label_preco = pesquisar.lblPreco  # Label para o campo de preço
        self.label_quantidade = pesquisar.lblQuantidade  # Label para o campo de quantidade
        self.label_data = pesquisar.lblData  # Label para o campo de data
        self.label_todos = [self.label_nome, self.label_categoria, self.label_id, self.label_preco, self.label_quantidade, self.label_data]  # Lista de todos os labels

        # Campos de entrada da interface de pesquisa
        self.input_nome = pesquisar.txtNome  # Campo de entrada para o nome
        self.input_categoria = pesquisar.cbxCategoria  # Campo de entrada para a categoria
        self.input_id = pesquisar.sbId  # Campo de entrada para o ID
        self.input_preco = pesquisar.dsbPreco  # Campo de entrada para o preço
        self.input_quantidade = pesquisar.sbQuantidade  # Campo de entrada para a quantidade
        self.input_data = pesquisar.deData  # Campo de entrada para a data
        self.input_todos = [self.input_nome, self.input_categoria, self.input_id, self.input_preco, self.input_quantidade, self.input_data]  # Lista de todos os campos de entrada

        # Checkboxes para pesquisa com intervalo
        self.check_ate_id = pesquisar.checkAteId  # Checkbox para pesquisa por ID com intervalo
        self.check_ate_preco = pesquisar.checkAtePreco  # Checkbox para pesquisa por preço com intervalo
        self.check_ate_quantidade = pesquisar.checkAteQuantidade  # Checkbox para pesquisa por quantidade com intervalo
        self.check_ate_data = pesquisar.checkAteData  # Checkbox para pesquisa por data com intervalo
        self.check_ate_todos = [self.check_ate_id, self.check_ate_preco, self.check_ate_quantidade, self.check_ate_data]  # Lista de todos os checkboxes de intervalo

        # Labels para pesquisa com intervalo
        self.label_ate_id = pesquisar.lblAteId  # Label para o campo "Até" do ID
        self.label_ate_preco = pesquisar.lblAtePreco  # Label para o campo "Até" do preço
        self.label_ate_quantidade = pesquisar.lblAteQuantidade  # Label para o campo "Até" da quantidade
        self.label_ate_data = pesquisar.lblAteData  # Label para o campo "Até" da data
        self.label_ate_todos = [self.label_ate_id, self.label_ate_preco, self.label_ate_quantidade, self.label_ate_data]  # Lista de todos os labels de intervalo

        # Labels para os segundos campos de intervalo
        self.label_id2 = pesquisar.lblId2  # Label para o segundo campo de ID
        self.label_preco2 = pesquisar.lblPreco2  # Label para o segundo campo de preço
        self.label_quantidade2 = pesquisar.lblQuantidade2  # Label para o segundo campo de quantidade
        self.label_data2 = pesquisar.lblData2  # Label para o segundo campo de data
        self.label_todos2 = [self.label_id2, self.label_preco2, self.label_quantidade2, self.label_data2]  # Lista de todos os segundos labels

        # Campos de entrada para os segundos campos de intervalo
        self.input_id2 = pesquisar.sbId2  # Campo de entrada para o segundo ID
        self.input_preco2 = pesquisar.dsbPreco2  # Campo de entrada para o segundo preço
        self.input_quantidade2 = pesquisar.sbQuantidade2  # Campo de entrada para a segunda quantidade
        self.input_data2 = pesquisar.deData2  # Campo de entrada para a segunda data
        self.input_todos2 = [self.input_id2, self.input_preco2, self.input_quantidade2, self.input_data2]  # Lista de todos os segundos campos de entrada

        # Lista de todos os elementos da interface de pesquisa
        self.todos = self.check_todos + self.label_todos + self.input_todos + self.check_ate_todos + self.label_todos2 + self.label_ate_todos + self.label_todos2 + self.input_todos2

        # Define a data atual nos campos de data
        self.input_data.setDate(date.today())
        self.input_data2.setDate(date.today())

# Instância da classe interface_pesquisar para ser usada globalmente
botoes_pesquisar = interface_pesquisar()