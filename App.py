from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox
#from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMenuBar, QMenu, QAction
#from PyKDE4.kdeui import KDateComboBox
import sqlite3
import datetime
import os
import sys


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self._lista_etiquetas = list()
        self._DB = 'BD_EXPEDICAO.db'
        #self._banco = factory_db(self.get_banco_dados())
        uic.loadUi("tela_inicio.ui", self)
        
        #MENU

        #FILTROS

        #BOTÕES
        self.btn_sair.clicked.connect(exit)
        self.btn_cadastrar.clicked.connect(self.cadastrar_espelho)
    
    def cadastrar_espelho(self):
        formSec = uic.loadUi("tela_cadastro.ui", self)
        formSec.resize(640, 500)
        formSec.resize()
        formSec.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    janela = Window()
    janela.show()
    sys.exit(app.exec_())