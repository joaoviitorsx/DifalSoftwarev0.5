from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QCheckBox, QSpacerItem, QSizePolicy, QFrame
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QPixmap
from database.db_conexao import conectar_banco, cadastrar_empresa

class TelaCadastro(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.conexao = conectar_banco()
        
        # **Layout Principal**
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # **Logo**
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
        self.label_titulo = QLabel("Cadastro de Empresa")
        self.label_titulo.setObjectName("titulo")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_titulo)

        # **Descrição**
        self.label_descricao = QLabel("Preencha os campos abaixo para cadastrar uma nova empresa")
        self.label_descricao.setObjectName("descricao")
        self.label_descricao.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_descricao)

        # **Espaçamento**
        self.container_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # **Campo CNPJ**
        self.label_cnpj = QLabel("CNPJ")
        self.label_cnpj.setObjectName("campoLabel")
        self.container_layout.addWidget(self.label_cnpj)

        self.input_cnpj = QLineEdit()
        self.input_cnpj.setPlaceholderText("00.000.000/0000-00")
        self.input_cnpj.setObjectName("campoInput")
        self.input_cnpj.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.input_cnpj)

        # **Validação do CNPJ**
        cnpj_regex = QRegularExpression("[0-9]{2}\\.[0-9]{3}\\.[0-9]{3}/[0-9]{4}-[0-9]{2}")
        self.input_cnpj.setValidator(QRegularExpressionValidator(cnpj_regex))

        # **Campo Razão Social**
        self.label_razao_social = QLabel("Razão Social")
        self.label_razao_social.setObjectName("campoLabel")
        self.container_layout.addWidget(self.label_razao_social)

        self.input_razao_social = QLineEdit()
        self.input_razao_social.setPlaceholderText("Nome da Empresa")
        self.input_razao_social.setObjectName("campoInput")
        self.input_razao_social.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.input_razao_social)

        # **Checkbox para empresa de telecomunicações**
        self.checkbox_telecom = QCheckBox("Empresa de Telecom")
        self.checkbox_telecom.setObjectName("checkboxTelecom")
        self.checkbox_telecom.setCursor(Qt.PointingHandCursor)
        self.container_layout.addWidget(self.checkbox_telecom)

        # **Espaçamento**
        self.container_layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # **Botões**
        self.botoes_container = QFrame()
        self.botoes_layout = QVBoxLayout(self.botoes_container)

        self.botao_salvar = QPushButton("Salvar")
        self.botao_salvar.setObjectName("botaoPrincipal")
        self.botao_salvar.setCursor(Qt.PointingHandCursor)
        self.botao_salvar.clicked.connect(self.confirmar_salvar)
        self.botoes_layout.addWidget(self.botao_salvar)

        self.botao_voltar = QPushButton("Voltar")
        self.botao_voltar.setObjectName("botaoSecundario")
        self.botao_voltar.setCursor(Qt.PointingHandCursor)
        self.botao_voltar.clicked.connect(self.voltar_para_tela_inicial)
        self.botoes_layout.addWidget(self.botao_voltar)

        self.container_layout.addWidget(self.botoes_container)

        # **Adiciona o container ao layout principal**
        self.layout.addWidget(self.container)

    def confirmar_salvar(self):
        """Exibe um pop-up de confirmação antes de salvar a empresa."""
        cnpj = self.input_cnpj.text().strip()
        razao_social = self.input_razao_social.text().strip()
        setor_telecom = "Sim" if self.checkbox_telecom.isChecked() else "Não"

        if not cnpj or not razao_social:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos corretamente.")
            return

        resposta = QMessageBox.question(
            self, "Confirmação",
            f"Tem certeza que deseja salvar esta empresa?\n\nCNPJ: {cnpj}\nRazão Social: {razao_social}\nSetor de Telecom: {setor_telecom}",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            self.salvar_empresa()
    
    def salvar_empresa(self):
        """Cadastra a empresa no banco de dados."""
        cnpj = self.input_cnpj.text().strip()
        razao_social = self.input_razao_social.text().strip()
        setor_telecom = "Sim" if self.checkbox_telecom.isChecked() else "Não"
        
        cadastrar_empresa(self.conexao, cnpj, razao_social, setor_telecom)
        QMessageBox.information(self, "Sucesso", "Empresa cadastrada com sucesso!")
        self.voltar_para_tela_inicial()
    
    def voltar_para_tela_inicial(self):
        """Retorna para a tela inicial após o cadastro."""
        self.main_window.mostrar_tela_inicial()
