from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMenuBar, QMenu, QAction
import os
import sys

import App
from factory_db import *
from leitura_espelho_db import *

class Leitura(QtWidgets.QMainWindow):
    def __init__(self):
        super(Leitura, self).__init__()
        uic.loadUi("gui/view/tela_leitura.ui", self)
        self._espelho = '000001'
        self.lbl_espelho.setText(f"Espelho: {self._espelho}")
        self._banco = factory_db()
        
        #self.main = App.Main_Window()

        #BOTÕES
        self.txt_entrada.returnPressed.connect(self.adicionar)
        self.btn_adicionar.clicked.connect(self.adicionar)
        self.btn_sair.clicked.connect(self.sair)

    def abrir_espelho(self, espelho):
        self._espelho = espelho
        self.lbl_espelho.setText(f"Espelho: {self._espelho}")
        self.inserir_tabela(leitura_espelho_db.buscar(self._banco.get_cursor(), self._espelho))
        self.atualizar_label_geral()
    
    def sair(self):
        self.tela = App.Main_Window()
        self.tela.show()
        self.hide()

    def closeEvent(self, event):
        self.tela = App.Main_Window()
        self.tela.show()
        event.accept()

    def adicionar(self):
        try:
            etiqueta = self.txt_entrada.text()
            if len(etiqueta) == 18 and etiqueta.isnumeric():
                if etiqueta[0] == '0':
                    print('produto: ', etiqueta[4:8])
                    produto = int(etiqueta[4:8])
                else:
                    print('produto: ', etiqueta[6:9])
                    produto = int(etiqueta[6:9])
            elif len(etiqueta) == 20 and etiqueta.isnumeric():
                print('produto: ', etiqueta[4:10])
                produto = int(etiqueta[4:10])
            else:
                print('codigo invalido! ', etiqueta)
                self.txt_entrada.setText('')
                return False
            
            volume = (etiqueta, self._espelho, produto)
            self.txt_entrada.setText('')
            
            if leitura_espelho_db.inserir_volume(self._banco.get_cursor(),\
                self._banco.get_conexao(),\
                    etiqueta, self._espelho,\
                        produto):
                volume_real, peso_real = leitura_espelho_db.buscar_qtde_etqta_lida(self._banco.get_cursor(),\
                self._espelho, produto)
                leitura_espelho_db.atualizar_espelho_lido(self._banco.get_cursor(),\
                self._banco.get_conexao(), self._espelho, produto, volume_real, peso_real)
            else:
                print("Não permitido")

            self.atualizar_label_geral()
            self.atualizar_tabela()
        except Exception as e:
            self.txt_entrada.setText('')
            print("Erro ao adicionar a etiqueta: ", e)
    
    def atualizar_tabela(self):
        self.tbl_resumo.setRowCount(0)
        self.inserir_tabela(leitura_espelho_db.buscar(self._banco.get_cursor(), self._espelho))

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

"""if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    janela = Leitura()
    janela.show()
    sys.exit(app.exec_())"""