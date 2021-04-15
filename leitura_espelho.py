from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMenuBar, QMenu, QAction
import os
import sys

from factory_db import *
from leitura_espelho_db import *

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("gui/view/tela_leitura.ui", self)
        self._espelho = '000001'
        self.lbl_espelho.setText(f"Espelho: {self._espelho}")
        self._banco = factory_db()
        self.inserir_tabela(leitura_espelho_db.buscar(self._banco.get_cursor(), self._espelho))
        self.atualizar_label_geral()

        #MENU
        #self.txt_cod.textChanged.connect(self.alterar_label)
        #self.txt_volumes.textChanged.connect(self.alterar_label)

        #BOTÕES
        self.btn_adicionar.clicked.connect(self.adicionar)
        #self.btn_salvar.clicked.connect(self.salvar)
        #self.btn_remover.clicked.connect(self.remover_tabela)
        #self.btn_cadastrar.clicked.connect()
    
    def adicionar(self):
        etiqueta = self.txt_entrada.text()
        produto = int(etiqueta[4:8])
        volume = (etiqueta, self._espelho, produto)
        self.txt_entrada.setText('')
        print(volume)
        leitura_espelho_db.inserir_volume(self._banco.get_cursor(),\
             self._banco.get_conexao(),\
                  etiqueta, self._espelho,\
                       produto)

    def inserir_tabela(self, dados):
        rowCount = self.tbl_resumo.rowCount()
        cont = len(dados)
        while cont > 0:
            cont -= 1
            self.tbl_resumo.insertRow(rowCount)
            self.tbl_resumo.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(str(dados[cont][0])))
            self.tbl_resumo.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(str(dados[cont][1])))
            self.tbl_resumo.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(str(dados[cont][2])))
            self.tbl_resumo.setItem(rowCount, 3, QtWidgets.QTableWidgetItem(str(dados[cont][3])))
            self.tbl_resumo.setItem(rowCount, 4, QtWidgets.QTableWidgetItem(str(dados[cont][4])))
            self.tbl_resumo.setItem(rowCount, 5, QtWidgets.QTableWidgetItem(str(dados[cont][5])))
            self.tbl_resumo.setItem(rowCount, 6, QtWidgets.QTableWidgetItem(str(dados[cont][6])))
            self.tbl_resumo.setItem(rowCount, 7, QtWidgets.QTableWidgetItem(str(dados[cont][7])))
          
    def atualizar_label_geral(self):
        dados = leitura_espelho_db.buscar_valor_geral(self._banco.get_cursor(), self._espelho)
        vol_prev_geral = dados[0]
        peso_prev_geral = dados[1]
        vol_prev_real = dados[2]
        peso_prev_real = dados[3]
                
        self.lbl_vol_prev_geral.setText(str(vol_prev_geral) + ' CX')
        self.lbl_peso_prev_geral.setText(str(peso_prev_geral) + ' KG')
        self.lbl_vol_real_geral.setText(str(vol_prev_real) + ' CX')
        self.lbl_peso_real_geral.setText(str(peso_prev_real) + ' KG')

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    janela = Window()
    janela.show()
    sys.exit(app.exec_())