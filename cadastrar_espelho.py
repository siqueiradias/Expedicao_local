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

        #BOTÕES
        self.btn_adicionar.clicked.connect(self.adicionar)
        self.btn_salvar.clicked.connect(self.salvar)
        self.btn_remover.clicked.connect(self.remover_tabela)
        #self.btn_cadastrar.clicked.connect()

    def _buscar_dados(self):
        cadastrar_espelho_db().buscar(self.txt_cod.text())

    def _salvar_dados(self):
        pass

    def alterar_label(self):
        dados = cadastrar_espelho_db().buscar(self.txt_cod.text())
        try:
            self.lbl_descricao.setText(dados[1])            
        except Exception as e:
            print("Erro ao alterar label descrição: ", e)
            self.lbl_descricao.setText('')

        try:
            self.lbl_peso.setText(f"{float(dados[2]*int(self.txt_volumes.text())):.3f} KG")
        except Exception as e:
            print("Erro ao alterar label peso: ", e)
            self.lbl_peso.setText("0.000 KG")
    
    def pegar_valor(self):
        volume_geral = 0
        peso_geral = float(0.0)
        cont = 0
        lista_espelho = []
        while cont < self.tbl_resumo.rowCount():
            volume_geral += int(self.tbl_resumo.item(cont, 2).text())
            peso_geral += float(self.tbl_resumo.item(cont, 3).text())
            lista_espelho.append((self.lbl_espelho.text(),\
                int(self.tbl_resumo.item(cont, 0).text()),\
                     int(self.tbl_resumo.item(cont, 2).text()),\
                         float(self.tbl_resumo.item(cont, 3).text()),\
                             0,\
                                 float(0.0)))
            cont += 1
        return lista_espelho

    def salvar(self):
        dados = self.pegar_valor()
        for item in dados:
            print(item)
        try:
            salvar_dados = cadastrar_espelho_db()
            salvar_dados.inserir_espelho(dados)
        except Exception as e:
            print('Erro ao SALVAR os dados dos espelho: ', e)

    def adicionar(self):
        if self.verificar_tabela():
            print("Produto já adicionado!!!")
        else:
            self.inserir_tabela()
            self.atualizar_label_geral()
            self.txt_cod.setText('')
            self.txt_volumes.setText('')

    def verificar_tabela(self):
        cont = 0
        while cont < self.tbl_resumo.rowCount():
            if self.tbl_resumo.item(cont, 0).text() == self.txt_cod.text():
                return(True)
            cont += 1
        return False

    def inserir_tabela(self):
        rowCount = self.tbl_resumo.rowCount()
        self.tbl_resumo.insertRow(rowCount)
        # add more if there is more columns in the database.
        self.tbl_resumo.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(str(int(self.txt_cod.text()))))
        self.tbl_resumo.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(self.lbl_descricao.text()))
        self.tbl_resumo.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(str(int(self.txt_volumes.text()))))
        self.tbl_resumo.setItem(rowCount, 3, QtWidgets.QTableWidgetItem(self.lbl_peso.text().replace(' KG','')))
        self.pegar_valor()
    
    def atualizar_label_geral(self):
        dados = self.pegar_valor()
        volume_geral = 0
        peso_geral = 0.0
        for item in dados:
            volume_geral += item[2]
            peso_geral += item[3]
        
        self.lbl_geral_volume.setText(str(volume_geral) + ' CX')
        self.lbl_geral_peso.setText(str(peso_geral) + ' KG')

    def remover_tabela(self):
        if self.tbl_resumo.rowCount() > 0:
            self.tbl_resumo.removeRow(self.tbl_resumo.currentRow())
            self.atualizar_label_geral()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    janela = Window()
    janela.show()
    sys.exit(app.exec_())