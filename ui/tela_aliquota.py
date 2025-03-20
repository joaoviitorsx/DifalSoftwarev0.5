import re
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QSpacerItem, QSizePolicy, QMessageBox
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QPixmap


class TelaAliquota(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.empresa = None
        
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

        # **Container Central**
        self.container = QFrame()
        self.container.setObjectName("cardContainer")
        self.container.setFixedWidth(400)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignCenter)

        # **Título**
        self.label_titulo = QLabel("Configuração da Alíquota")
        self.label_titulo.setObjectName("titulo")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_titulo)

        # **Espaçamento**
        self.container_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        #Container de empresa e cnpj
        self.info_empresa_container = QFrame()
        self.info_empresa_container.setObjectName("infoEmpresaContainer")
        self.info_empresa_container.setFrameShape(QFrame.StyledPanel)
        self.info_empresa_layout = QVBoxLayout(self.info_empresa_container)

        self.label_empresa = QLabel("empresa")
        self.label_empresa.setObjectName("empresaNome")
        self.label_empresa.setAlignment(Qt.AlignLeft)
        self.info_empresa_layout.addWidget(self.label_empresa)

        self.label_cnpj = QLabel("CNPJ: --.--")
        self.label_cnpj.setObjectName("empresaCNPJ")
        self.label_cnpj.setAlignment(Qt.AlignLeft)
        self.info_empresa_layout.addWidget(self.label_cnpj)

        self.container_layout.addWidget(self.info_empresa_container)

        # **Descrição**
        self.label_descricao = QLabel("Defina a alíquota interna para o cálculo do DIFAL")
        self.label_descricao.setAlignment(Qt.AlignLeft)
        self.container_layout.addWidget(self.label_descricao)

        # **Campo da Alíquota**
        self.label_aliquota = QLabel("Alíquota Interna (%)")
        self.label_aliquota.setObjectName("campoLabel")
        self.container_layout.addWidget(self.label_aliquota)

        self.input_aliquota = QLineEdit()
        self.input_aliquota.setPlaceholderText("0.00")
        self.input_aliquota.setObjectName("campoInput")
        self.input_aliquota.setAlignment(Qt.AlignCenter)

        # Validação: apenas números com até duas casas decimais
        aliquota_regex = QRegularExpression("^[0-9]+(\\.[0-9]{1,2})?$")
        self.input_aliquota.setValidator(QRegularExpressionValidator(aliquota_regex))

        self.container_layout.addWidget(self.input_aliquota)

        # **Descrição do Campo**
        self.label_descricao_aliquota = QLabel("Valor percentual da alíquota interna do estado")
        self.label_descricao_aliquota.setObjectName("campoDescricao")
        self.label_descricao_aliquota.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_descricao_aliquota)

        # **Espaçamento**
        self.container_layout.addSpacerItem(QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # **Botões**
        self.botoes_container = QFrame()
        self.botoes_layout = QVBoxLayout(self.botoes_container)

        self.botao_continuar = QPushButton("Prosseguir")
        self.botao_continuar.setObjectName("botaoPrincipal")
        self.botao_continuar.setCursor(Qt.PointingHandCursor)
        self.botao_continuar.clicked.connect(self.continuar)
        self.botoes_layout.addWidget(self.botao_continuar)

        self.botao_voltar = QPushButton("Voltar")
        self.botao_voltar.setObjectName("botaoSecundario")
        self.botao_voltar.setCursor(Qt.PointingHandCursor)
        self.botao_voltar.clicked.connect(self.voltar_para_tela_inicial)
        self.botoes_layout.addWidget(self.botao_voltar)

        self.container_layout.addWidget(self.botoes_container)

        # **Adiciona o container ao layout principal**
        self.layout.addWidget(self.container)

    def formatar_cnpj(self, cnpj):
        """Formata um CNPJ de 'XXXXXXXXXXXXXX' para 'XX.XXX.XXX/XXXX-XX'"""
        cnpj_limpo = re.sub(r'\D', '', cnpj)
        if len(cnpj_limpo) == 14:
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj

    def definir_empresa(self, empresa):
        """Define os dados da empresa selecionada"""
        self.empresa = empresa
        self.label_empresa.setText(empresa["razao_social"])
        self.label_cnpj.setText(f"CNPJ: {self.formatar_cnpj(empresa['cnpj'])}")

    def continuar(self):
        """Valida e prossegue para a próxima tela."""
        aliquota_texto = self.input_aliquota.text().strip()

        if not aliquota_texto:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos corretamente.")
            return 
        
        try:
            aliquota = float(aliquota_texto)
            if aliquota <= 0 or aliquota > 100:
                raise ValueError

            self.main_window.mostrar_tela_principal(self.empresa, aliquota)
        except ValueError:
            QMessageBox.warning(self, "Erro", "Valor inválido")
            pass 

    def voltar_para_tela_inicial(self):
        """Retorna para a tela inicial"""
        self.main_window.mostrar_tela_inicial()
