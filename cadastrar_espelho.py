from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMenuBar, QMenu, QAction
import sqlite3
import datetime
import os
import sys

from cadastrar_espelho_db import *

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("gui/view/tela_cadastro.ui", self)
        
        #MENU
        self.txt_cod.textChanged.connect(self.alterar_label)
        self.txt_volumes.textChanged.connect(self.alterar_label)

        #FILTROS


        #BOTÕES
        self.btn_adicionar.clicked.connect(self.btn_adicionar)
        self.btn_remover.clicked.connect(self.remover_tabela)
        #self.btn_cadastrar.clicked.connect()

    def _buscar_dados(self):
        cadastrar_espelho_db().buscar(self.txt_cod.text())

    def _salvar_dados(self):
        pass

    def alterar_label(self):
        dados = cadastrar_espelho_db().buscar(self.txt_cod.text())
        print(dados)
        try:
            self.lbl_descricao.setText(dados[1])
            print(dados[2])
            self.lbl_peso.setText(f"{float(dados[2]*int(self.txt_volumes.text())):.3f} KG")
        except Exception as identifier:
            pass
    
    def pegar_valor(self):
        lista = self.tbl_resumo.itemAt(1, 1).text()
        print(lista)

    def inserir_tabela(self):
        rowCount = self.tbl_resumo.rowCount()
        self.tbl_resumo.insertRow(rowCount)
        # add more if there is more columns in the database.
        self.tbl_resumo.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(str(int(self.txt_cod.text()))))
        self.tbl_resumo.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(self.lbl_descricao.text()))
        self.tbl_resumo.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(self.txt_volumes.text()))
        self.tbl_resumo.setItem(rowCount, 3, QtWidgets.QTableWidgetItem(self.lbl_peso.text().replace(' KG','')))
        self.pegar_valor()
    
    def btn_adicionar(self):
        self.inserir_tabela()

        volume_geral = int(self.lbl_geral_volume.text().replace(' CX',''))
        volume_geral += int(self.txt_volumes.text())
        self.lbl_geral_volume.setText(str(volume_geral) + ' CX')
        
        peso_geral = float(self.lbl_geral_peso.text().replace(' KG',''))
        peso_geral += float(self.lbl_peso.text().replace(' KG',''))
        self.lbl_geral_peso.setText(str(peso_geral) + ' KG')

    def remover_tabela(self):
        if self.tbl_resumo.rowCount() > 0:
            self.tbl_resumo.removeRow(self.tbl_resumo.currentRow())

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    janela = Window()
    janela.show()
    sys.exit(app.exec_())