import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from ui.tela_inicial import TelaInicial
from ui.tela_cadastro import TelaCadastro
from ui.tela_aliquota import TelaAliquota
from ui.tela_principal import TelaPrincipal

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Software para Cálculo de DIFAL")
        self.setWindowIcon(QIcon("images/icone.ico"))
        self.setMinimumSize(QSize(800, 600))
        
        # Criando o QStackedWidget para navegação entre telas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Inicializando as telas
        self.tela_inicial = TelaInicial(self)
        self.tela_cadastro = TelaCadastro(self)
        self.tela_aliquota = TelaAliquota(self)
        self.tela_principal = TelaPrincipal(self)
        
        # Adicionando as telas ao QStackedWidget
        self.stacked_widget.addWidget(self.tela_inicial)
        self.stacked_widget.addWidget(self.tela_cadastro)
        self.stacked_widget.addWidget(self.tela_aliquota)
        self.stacked_widget.addWidget(self.tela_principal)
        
        # Iniciar na tela inicial
        self.mostrar_tela_inicial()
        
        # Aplicar o tema de estilização
        self.aplicar_estilos()
    
    def mostrar_tela_inicial(self):
        self.stacked_widget.setCurrentWidget(self.tela_inicial)
    
    def mostrar_tela_cadastro(self):
        self.stacked_widget.setCurrentWidget(self.tela_cadastro)
    
    def mostrar_tela_aliquota(self, empresa=None):
        self.tela_aliquota.definir_empresa(empresa)
        self.stacked_widget.setCurrentWidget(self.tela_aliquota)
    
    def mostrar_tela_principal(self, empresa=None, aliquota=None):
        self.tela_principal.definir_dados(empresa, aliquota)
        self.stacked_widget.setCurrentWidget(self.tela_principal)
    
    def aplicar_estilos(self):
        try:
            with open("styles/main.qss", "r", encoding="utf-8") as f:
                stylesheet = f.read()
                self.setStyleSheet(stylesheet)
        except FileNotFoundError:
            print("Arquivo de estilos não encontrado.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
