from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMenuBar, QMenu, QAction
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
        uic.loadUi("tela_cadastro.ui", self)
        
        #MENU
        self.txt_cod.textChanged.connect(self.alterar_label)
        self.txt_volumes.textChanged.connect(self.alterar_label)

        #FILTROS


        #BOTÕES
        self.btn_adicionar.clicked.connect(self.preencher_tabela)
        #self.btn_cadastrar.clicked.connect()

    def alterar_label(self):
        self.lbl_descricao.setText(self.txt_cod.text())
        self.lbl_peso.setText(self.txt_volumes.text())

    def preencher_tabela(self):
        #self.tbl_resumo = QTableWidget()
        lista = []
        lista.append((self.txt_cod.text(), self.txt_volumes.text(), self.lbl_descricao.text(), self.lbl_peso.text()))
        #print(help(self.tbl_resumo))
        # add more if there is more columns in the database.
        print("oi")
        print(lista)
        self.tbl_resumo.setItem(0, 0, QtWidgets.QTableWidgetItem(self.txt_cod.text()))
        self.tbl_resumo.setItem(0, 1, QtWidgets.QTableWidgetItem(self.txt_volumes.text()))
        self.tbl_resumo.setItem(0, 2, QtWidgets.QTableWidgetItem(self.lbl_descricao.text()))
        self.tbl_resumo.setItem(0, 3, QtWidgets.QTableWidgetItem(self.lbl_peso.text()))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    janela = Window()
    janela.show()
    sys.exit(app.exec_())