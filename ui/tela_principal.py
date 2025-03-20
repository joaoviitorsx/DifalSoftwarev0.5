import re
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from utils.ler_arquivos import processar_nfes


class TelaPrincipal(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.empresa = None
        self.aliquota = None
        self.arquivo_xmls = None
        self.arquivo_ncm = None

        # **Layout Principal**
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Adicionando a logo da empresa
        self.logo = QLabel(self)
        pixmap = QPixmap("images/logo.png")
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap.scaled(250, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo)

        # **Container Principal**
        self.container = QFrame()
        self.container.setObjectName("cardContainer")
        self.container.setFixedWidth(550)  # Define largura fixa para centralizar
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignCenter)

        # **Título**
        self.label_titulo = QLabel("Arquivos para Processamento")
        self.label_titulo.setObjectName("titulo")
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_titulo)

        # **Descrição**
        self.label_descricao = QLabel("Envie os arquivos necessários para o cálculo do DIFAL")
        self.label_descricao.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.label_descricao)

        # **Espaçamento**
        self.container_layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # **Sub-container para informações da empresa**
        self.info_empresa_container = QFrame()
        self.info_empresa_container.setObjectName("infoEmpresaContainer")
        self.info_empresa_container.setFrameShape(QFrame.StyledPanel)
        self.info_empresa_text_layout = QVBoxLayout()
        self.info_empresa_layout = QHBoxLayout(self.info_empresa_container)

        # **Nome da Empresa**
        self.label_empresa = QLabel("empresa 1")
        self.label_empresa.setObjectName("empresaNome")
        self.label_empresa.setAlignment(Qt.AlignLeft)
        self.info_empresa_text_layout.addWidget(self.label_empresa)

        # **CNPJ**
        self.label_cnpj = QLabel("CNPJ: 12.345.675/0001-99")
        self.label_cnpj.setObjectName("empresaCNPJ")
        self.label_cnpj.setAlignment(Qt.AlignLeft)
        self.info_empresa_text_layout.addWidget(self.label_cnpj)

        self.info_empresa_layout.addLayout(self.info_empresa_text_layout)

        # **Alíquota (Destaque Azul)**
        self.label_aliquota = QLabel("Alíquota: 12%")
        self.label_aliquota.setObjectName("aliquotaDestaque")
        self.label_aliquota.setAlignment(Qt.AlignRight)
        self.info_empresa_layout.addWidget(self.label_aliquota)

        # Adiciona o sub-container ao container principal
        self.container_layout.addWidget(self.info_empresa_container)

        # **Seção de Upload (Arquivo XML)**
        self.upload_xml_container = self.criar_card_upload(
            "Arquivo de XMLs (NF-es)", "Clique para selecionar um arquivo (.xlsx) com os XMLs",
            self.selecionar_arquivo_xmls
        )
        self.container_layout.addWidget(self.upload_xml_container)

        # **Seção de Upload (Arquivo NCM)**
        self.upload_ncm_container = self.criar_card_upload(
            "Arquivo de NCM", "Clique para selecionar um arquivo (.xlsx) com os dados de NCM",
            self.selecionar_arquivo_ncm
        )
        self.container_layout.addWidget(self.upload_ncm_container)

        # **Progress Bar**
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(20)  # Ajusta a altura
        self.container_layout.addWidget(self.progress_bar)

        # **Botão de Processamento**
        self.botao_processar = QPushButton("Processar Arquivos")
        self.botao_processar.setObjectName("botaoProcessar")
        self.botao_processar.setCursor(Qt.PointingHandCursor)
        self.botao_processar.clicked.connect(self.processar_dados)
        self.container_layout.addWidget(self.botao_processar)

        # Botão de voltar
        self.botao_voltar = QPushButton("Voltar")
        self.botao_voltar.setObjectName("botaoVoltar")
        self.botao_voltar.setCursor(Qt.PointingHandCursor)
        self.botao_voltar.clicked.connect(self.voltar_para_tela_aliquota)
        self.container_layout.addWidget(self.botao_voltar)

        # **Adiciona o container principal ao layout principal**
        self.layout.addWidget(self.container)

    def criar_card_upload(self, titulo, descricao, funcao_click):
        """Cria um card de upload estilizado."""
        card = QFrame()
        card.setObjectName("uploadCard")
        card_layout = QVBoxLayout(card)

        label_titulo = QLabel(titulo)
        label_titulo.setObjectName("uploadTitulo")
        label_titulo.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(label_titulo)

        label_descricao = QLabel(descricao)
        label_descricao.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(label_descricao)

        botao_selecionar = QPushButton("📂 Selecionar arquivo")
        botao_selecionar.setCursor(Qt.PointingHandCursor)
        botao_selecionar.setObjectName("botaoUpload")
        botao_selecionar.clicked.connect(funcao_click)
        card_layout.addWidget(botao_selecionar)

        return card
    
    def formatar_cnpj(self, cnpj):
        """Formata um CNPJ de 'XXXXXXXXXXXXXX' para 'XX.XXX.XXX/XXXX-XX'"""
        cnpj_limpo = re.sub(r'\D', '', cnpj)
        if len(cnpj_limpo) == 14:
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj

    def definir_dados(self, empresa, aliquota):
        """Define os dados da empresa e alíquota selecionada."""
        self.empresa = empresa
        self.aliquota = aliquota
        self.label_empresa.setText(empresa["razao_social"])
        self.label_cnpj.setText(f"CNPJ: {self.formatar_cnpj(empresa['cnpj'])}")
        self.label_aliquota.setText(f"Alíquota: {aliquota}%")

    def selecionar_arquivo_xmls(self):
        """Abre o diálogo para selecionar a planilha de XMLs."""
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecionar Planilha de XMLs", "", "Planilhas Excel (*.xlsx)")
        if arquivo:
            self.arquivo_xmls = arquivo
            QMessageBox.information(self, "Arquivo Selecionado", f"Planilha de XMLs carregada: {arquivo}")

    def selecionar_arquivo_ncm(self):
        """Abre o diálogo para selecionar a planilha de NCMs."""
        arquivo, _ = QFileDialog.getOpenFileName(self, "Selecionar Planilha de NCMs", "", "Planilhas Excel (*.xlsx)")
        if arquivo:
            self.arquivo_ncm = arquivo
            QMessageBox.information(self, "Arquivo Selecionado", f"Planilha de NCMs carregada: {arquivo}")

    def processar_dados(self):
        """Valida os arquivos e inicia o processamento."""
        if not self.arquivo_xmls or not self.arquivo_ncm:
            QMessageBox.warning(self, "Erro", "Selecione ambos os arquivos antes de processar.")
            return
        
        processar_nfes(self.arquivo_xmls, self.arquivo_ncm, self.progress_bar, self)
        QMessageBox.information(self, "Sucesso", "Processamento iniciado!")
        self.progress_bar.setValue(0)

    def voltar_para_tela_aliquota(self):
        """Retorna para a tela de alíquota"""
        self.main_window.mostrar_tela_aliquota(self.empresa)
