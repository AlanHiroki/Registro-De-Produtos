# Importações necessárias
from PyQt6 import uic, QtWidgets  # Bibliotecas para criar a interface gráfica
from datetime import date  # Para trabalhar com datas
from modulos.globais import interface_pesquisar, botoes_pesquisar  # Funções personalizadas para a interface de pesquisa

# Inicialização da aplicação PyQt
app = QtWidgets.QApplication([])

# Carregamento da interface de pesquisa
pesquisar = uic.loadUi('interface/rdp_pesquisar.ui')  # Carrega a interface de pesquisa
botoes = interface_pesquisar()  # Inicializa os botões da interface de pesquisa
botoes(pesquisar)  # Configura os botões na interface
botoes_pesquisar(pesquisar)  # Configura ações dos botões de pesquisa

# Importação dos módulos que controlam as telas e suas funcionalidades
from modulos import tela_editar, tela_principal, tela_produtos, tela_pesquisar, tela_historico, telas_login

# Configuração da tela principal de login
main = uic.loadUi('interface/rdp_login.ui')  # Carrega a interface de login
main.btnRegistrar.clicked.connect(lambda: tela_produtos.fechar_abrir(main, registrar))  # Abre a tela de registro
main.btnLogin.clicked.connect(lambda: telas_login.login(main, registro, sucesso, falha))  # Valida o login
main.btnMostrarSenha.clicked.connect(lambda: telas_login.mostrar_senha(main))  # Mostra/esconde a senha

# Configuração da tela de registro de usuário
registrar = uic.loadUi('interface/rdp_registrar.ui')  # Carrega a interface de registro
registrar.btnRegistrarRegistrar.clicked.connect(lambda: telas_login.registrar_usuario(registrar, sucesso, falha, main))  # Registra o usuário
registrar.btnVoltarRegistrar.clicked.connect(lambda: tela_produtos.fechar_abrir(registrar, main))  # Volta para a tela de login

# Configuração da tela de registro de produtos
registro = uic.loadUi('interface/rdp_registro.ui')  # Carrega a interface de registro de produtos
registro.deData.setDate(date.today())  # Define a data atual no campo de data
registro.btnSalvar.clicked.connect(lambda: tela_principal.btnSalvar(registro, sucesso, falha, produtos))  # Salva o registro
registro.btnLimpar.clicked.connect(lambda: tela_principal.btnLimpar(registro))  # Limpa os campos
registro.btnProdutos.clicked.connect(lambda: tela_principal.btnProduto(produtos))  # Abre a tela de produtos

# Configuração da tela de sucesso
sucesso = uic.loadUi('interface/rdp_sucesso.ui')  # Carrega a interface de sucesso
sucesso.btnContinuarS.clicked.connect(lambda: tela_principal.btnFechar(sucesso))  # Fecha a tela de sucesso

# Configuração da tela de falha
falha = uic.loadUi('interface/rdp_falha.ui')  # Carrega a interface de falha
falha.btnContinuarF.clicked.connect(lambda: tela_principal.btnFechar(falha))  # Fecha a tela de falha

# Configuração da tela de produtos
produtos = uic.loadUi('interface/rdp_produtos.ui')  # Carrega a interface de produtos
produtos.txtPesquisar.textChanged.connect(lambda: tela_produtos.pesquisar(produtos))  # Pesquisa produtos ao digitar
produtos.cbxPesquisar.currentIndexChanged.connect(lambda: tela_produtos.trocarInputData(produtos))  # Altera o campo de pesquisa

# Conexões dos botões da tela de produtos
produtos.btnEditar.clicked.connect(lambda: tela_editar.btnEditar(produtos, editar, falha))  # Abre a tela de edição
produtos.btnExcluir.clicked.connect(lambda: tela_produtos.btnExcluir(produtos, excluir, falha))  # Abre a tela de exclusão
produtos.btnPesquisar.clicked.connect(lambda: tela_produtos.abrir(pesquisar))  # Abre a tela de pesquisa
produtos.btnAtualizar.clicked.connect(lambda: tela_principal.btnAtualizar(produtos))  # Atualiza a lista de produtos
produtos.btnHistorico.clicked.connect(lambda: tela_historico.btnHistorico(historico))  # Abre a tela de histórico

# Configuração da tela de edição
editar = uic.loadUi('interface/rdp_editor.ui')  # Carrega a interface de edição
editar.btnRestaurar.clicked.connect(lambda: tela_editar.btnRestaurar(editar))  # Restaura os valores originais
editar.btnEditorSalvar.clicked.connect(lambda: tela_editar.btnEditorSalvar(editar, sucesso, falha, produtos))  # Salva as alterações

# Configuração da tela de exclusão
excluir = uic.loadUi('interface/rdp_excluir.ui')  # Carrega a interface de exclusão
excluir.btnNaoExcluir.clicked.connect(lambda: tela_principal.btnFechar(excluir))  # Cancela a exclusão
excluir.btnSimExcluir.clicked.connect(lambda: tela_produtos.btnExcluirSim(excluir, produtos))  # Confirma a exclusão

# Configuração da tela de pesquisa
pesquisar.checkTodos.clicked.connect(lambda marcado: tela_pesquisar.marcarTodos(marcado, botoes.todos))  # Marca/desmarca todos os filtros

# Conexões dos checkboxes da tela de pesquisa
pesquisar.checkNome.toggled.connect(lambda marcado: tela_pesquisar.marcadorHabilitar(marcado, botoes.label_nome, botoes.input_nome))
pesquisar.checkCategoria.toggled.connect(lambda marcado: tela_pesquisar.marcadorHabilitar(marcado, botoes.label_categoria, botoes.input_categoria))
pesquisar.checkId.toggled.connect(lambda marcado: tela_pesquisar.marcadorHabilitarEntre(marcado, botoes.check_ate_id, botoes.label_id, botoes.input_id, botoes.label_ate_id, botoes.label_id2, botoes.input_id2, botoes.check_ate_id))
pesquisar.checkAteId.toggled.connect(lambda marcado: tela_pesquisar.marcadorEntre(marcado, botoes.label_ate_id, botoes.label_id2, botoes.input_id2))
pesquisar.checkPreco.toggled.connect(lambda marcado: tela_pesquisar.marcadorHabilitarEntre(marcado, botoes.check_ate_preco, botoes.label_preco, botoes.input_preco, botoes.label_ate_preco, botoes.label_preco2, botoes.input_preco2, botoes.check_ate_preco))
pesquisar.checkAtePreco.toggled.connect(lambda marcado: tela_pesquisar.marcadorEntre(marcado, botoes.label_ate_preco, botoes.label_preco2, botoes.input_preco2))
pesquisar.checkQuantidade.toggled.connect(lambda marcado: tela_pesquisar.marcadorHabilitarEntre(marcado, botoes.check_ate_quantidade, botoes.label_quantidade, botoes.input_quantidade, botoes.label_ate_quantidade, botoes.label_quantidade2, botoes.input_quantidade2, botoes.check_ate_quantidade))
pesquisar.checkAteQuantidade.toggled.connect(lambda marcado: tela_pesquisar.marcadorEntre(marcado, botoes.label_ate_quantidade, botoes.label_quantidade2, botoes.input_quantidade2))
pesquisar.checkData.toggled.connect(lambda marcado: tela_pesquisar.marcadorHabilitarEntre(marcado, botoes.check_ate_data, botoes.label_data, botoes.input_data, botoes.label_ate_data, botoes.label_data2, botoes.input_data2, botoes.check_ate_data))
pesquisar.checkAteData.toggled.connect(lambda marcado: tela_pesquisar.marcadorEntre(marcado, botoes.label_ate_data, botoes.label_data2, botoes.input_data2))

# Botões da tela de pesquisa
pesquisar.btnLimparPesquisa.clicked.connect(lambda: tela_pesquisar.btnLimparPesquisa(botoes_pesquisar.todos, produtos))  # Limpa a pesquisa
pesquisar.btnPesquisar.clicked.connect(lambda: tela_pesquisar.btnPesquisar(produtos))  # Executa a pesquisa

# Configuração da tela de histórico
historico = uic.loadUi('interface/rdp_historico.ui')  # Carrega a interface de histórico
historico.txtPesquisarHistorico.textChanged.connect(lambda: tela_historico.pesquisarHistorico(historico))  # Pesquisa no histórico
historico.cbxPesquisarHistorico.currentIndexChanged.connect(lambda: tela_historico.trocarInputDataHistorico(historico))  # Altera o campo de pesquisa
historico.btnAtualizarHistorico.clicked.connect(lambda: tela_historico.btnAtualizarHistorico(historico))  # Atualiza o histórico
historico.btnDetalhes.clicked.connect(lambda: tela_historico.btnDetalhes(historico, detalhes, falha))  # Abre os detalhes
historico.tableWidget.cellDoubleClicked.connect(lambda: tela_historico.btnDetalhes(historico, detalhes, falha))  # Abre detalhes ao clicar na tabela

# Configuração da tela de detalhes
detalhes = uic.loadUi('interface/rdp_detalhes.ui')  # Carrega a interface de detalhes
detalhes.btnFechar.clicked.connect(lambda: tela_principal.btnFechar(detalhes))  # Fecha a tela de detalhes

# Exibe a tela principal e inicia a aplicação
main.show()
app.exec()