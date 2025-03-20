from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from database.db_conexao import conectar_banco, listar_empresas


class TelaInicial(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.conexao = conectar_banco()

        # **Layout Principal**
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Adiciona a logo da empresa
        self.logo = QLabel(self)
        pixmap = QPixmap("images/logo.png")
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap.scaled(250, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo)

        # **Container Principal**
        self.container = QFrame()
        self.container.setObjectName("cardContainer")
        self.container.setFixedWidth(450)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignCenter)

        # **Título**
        self.label_titulo = QLabel("Selecione uma empresa")
        self.label_titulo.setObjectName("titulo")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_titulo)

        # **Descrição**
        self.label_descricao = QLabel("Escolha uma empresa cadastrada ou cadastre uma nova")
        self.label_descricao.setObjectName("descricao")
        self.label_descricao.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_descricao)

        # **Dropdown para seleção de empresa**
        self.combo_empresas = QComboBox()
        self.combo_empresas.setObjectName("comboEmpresas")
        self.combo_empresas.setMinimumHeight(40)
        self.container_layout.addWidget(self.combo_empresas)

        # **Linha Separadora**
        self.linha = QFrame()
        self.linha.setFrameShape(QFrame.HLine)
        self.linha.setFrameShadow(QFrame.Sunken)
        self.container_layout.addWidget(self.linha)

        # **Botão para prosseguir**
        self.botao_prosseguir = QPushButton("Prosseguir")
        self.botao_prosseguir.setObjectName("botaoPrincipal")
        self.botao_prosseguir.setEnabled(False)  # Desativado até selecionar uma empresa
        self.botao_prosseguir.setCursor(Qt.PointingHandCursor)
        self.botao_prosseguir.clicked.connect(self.prosseguir_para_tela_aliquota)
        self.container_layout.addWidget(self.botao_prosseguir)

        # **Espaçamento**
        self.container_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # **Botão para cadastrar nova empresa**
        self.botao_cadastrar = QPushButton("➕ Cadastrar nova empresa")
        self.botao_cadastrar.setObjectName("botaoPrimario")
        self.botao_cadastrar.setCursor(Qt.PointingHandCursor)
        self.botao_cadastrar.clicked.connect(self.abrir_tela_cadastro)
        self.container_layout.addWidget(self.botao_cadastrar)

        # **Adiciona o container ao layout principal**
        self.layout.addWidget(self.container)

        # **Carrega as empresas do banco**
        self.carregar_empresas()

    def carregar_empresas(self):
        """Carrega as empresas do banco de dados no combo box."""
        empresas = listar_empresas(self.conexao)
        self.combo_empresas.clear()
        self.combo_empresas.addItem("Selecionar empresa...", None)

        for empresa in empresas:
            self.combo_empresas.addItem(f"{empresa['razao_social']} - {empresa['cnpj']}", empresa)

        # Conectar evento de mudança de seleção
        self.combo_empresas.currentIndexChanged.connect(self.habilitar_botao_prosseguir)

    def habilitar_botao_prosseguir(self, index):
        """Habilita o botão 'Prosseguir' apenas quando uma empresa é selecionada."""
        if index > 0:
            self.botao_prosseguir.setEnabled(True)
        else:
            self.botao_prosseguir.setEnabled(False)

    def prosseguir_para_tela_aliquota(self):
        """Obtém a empresa selecionada e avança para a tela de alíquota."""
        index = self.combo_empresas.currentIndex()
        if index > 0:
            empresa = self.combo_empresas.itemData(index)
            self.main_window.mostrar_tela_aliquota(empresa)

    def abrir_tela_cadastro(self):
        """Abre a tela de cadastro de empresas."""
        self.main_window.mostrar_tela_cadastro()

    def showEvent(self, event):
        """Recarrega a lista de empresas sempre que a tela for exibida."""
        self.carregar_empresas()
        super().showEvent(event)
