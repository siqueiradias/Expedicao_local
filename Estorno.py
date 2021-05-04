from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QShortcut
from PyQt5.QtGui import QKeySequence, QColor
#from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMenuBar, QMenu, QAction
import os
import sys

import leitura_espelho
from factory_db import *
from leitura_espelho_db import *
from audio2 import WavePlayerLoop
from Alerta import CustomDialog
from time import sleep

class Estorno(QtWidgets.QMainWindow):
    def __init__(self, espelho):
        super(Estorno, self).__init__()
        uic.loadUi("gui/view/tela_estorno.ui", self)
        self._espelho = espelho
        #self.lbl_espelho.setText(f"Espelho: {self._espelho}")
        self._banco = factory_db()
        self.txt_estorno.setFocus()

        self._dados = leitura_espelho_db.buscar_estorno(self._banco.get_cursor(), self._espelho)
        self._lista_vol_estornado = list()

        self.inserir_tabela(self._dados)

        self.txt_estorno.returnPressed.connect(self.estorno)
        self.btn_estornar.clicked.connect(self.estorno)

        self.shortcut_adicionar = QShortcut(QKeySequence("ESC"), self)
        self.shortcut_adicionar.activated.connect(self.sair)

    
    def sair(self):
        self.tela = leitura_espelho.Leitura()
        self.tela.abrir_espelho(self._espelho)
        self.tela.showMaximized()
        self.hide()
    
    def closeEvent(self, event):
        self.tela = leitura_espelho.Leitura()
        self.tela.abrir_espelho(self._espelho)
        self.tela.showMaximized()
        event.accept()

    def inserir_tabela(self, dados):
        header = self.tbl_estorno.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        rowCount = self.tbl_estorno.rowCount()
        cont = len(dados)
        while cont > 0:
            cont -= 1
            self.tbl_estorno.insertRow(rowCount)
            for coluna in range(2):    
                self.tbl_estorno.setItem(rowCount, coluna, QtWidgets.QTableWidgetItem(str(dados[cont][coluna])))

    def estorno(self):
        """Realiza o estorno de volume do espelho
        """        
        achou = 0
        for volume in self._dados:
            if self.txt_estorno.text() == volume[0]:
                if volume in self._lista_vol_estornado:
                    achou = 2
                else:
                    self._lista_vol_estornado.append(volume)
                    self.colorir_tabela(self.txt_estorno.text())
                    achou = 1
        if achou == 1:
            try:
                leitura_espelho_db.remove_vol_espelho(\
                    self._banco.get_cursor(), self._banco.get_conexao(),\
                         self._espelho, self.txt_estorno.text())
                
                self.lbl_msg.setText("Volume estornado...")
                self.txt_estorno.setText('')
                audio = WavePlayerLoop("audio/sucesso.wav")
                audio.play()
            except Exception as e:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Erro")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText(f"Erro ao estornar volume!!!")
                msg_box.setDetailedText(str(e))
                msg_box.setEscapeButton('ESC')
                return_value = msg_box.exec()

        elif achou == 2:
            self.lbl_msg.setText("Volume já estornado...")
            self.txt_estorno.setText('')
            audio = WavePlayerLoop("audio/existe.wav")
            audio.play()
        else:
            self.lbl_msg.setText("Volume NÃO está no esplho...")
            self.txt_estorno.setText('')
            audio = WavePlayerLoop("audio/erro.wav")
            audio.play()
    
    def colorir_tabela(self, volume):
        """Colore a linha da tabela que corresponde ao volume

        Args:
            volume (str): codigo de barras do produto
        """        
        rowCount = self.tbl_estorno.rowCount()
        cont = rowCount
        while cont > 0:
            cont -= 1
            if self.tbl_estorno.item(cont, 0).text() == volume:
                for coluna in range(2):    
                    self.tbl_estorno.item(cont, coluna).setBackground(QColor(255,0,0)) #Vermelho
                   
    def lista_estorno(self):
        print(self._lista_vol_estornado)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    janela = Estorno()
    janela.show()
    sys.exit(app.exec_())