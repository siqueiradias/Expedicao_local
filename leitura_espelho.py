from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QShortcut
from PyQt5.QtGui import QKeySequence, QColor
#from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMenuBar, QMenu, QAction
import os
import sys

import App
import Estorno
from factory_db import *
from leitura_espelho_db import *
from audio2 import WavePlayerLoop
from Alerta import CustomDialog
from time import sleep

class Leitura(QtWidgets.QMainWindow):
    def __init__(self):
        super(Leitura, self).__init__()
        uic.loadUi("gui/view/tela_leitura.ui", self)
        self._espelho = '000001'
        self.lbl_espelho.setText(f"Espelho: {self._espelho}")
        self._banco = factory_db()
        self.txt_entrada.setFocus()
        
        #TECLAS DE ATALHOS
        self.shortcut_adicionar = QShortcut(QKeySequence("Alt+A"), self)
        self.shortcut_adicionar.activated.connect(self.adicionar)

        self.shortcut_estornar = QShortcut(QKeySequence("Alt+R"), self)
        self.shortcut_estornar.activated.connect(self.estornar)

        self.shortcut_exportar = QShortcut(QKeySequence("Alt+E"), self)
        self.shortcut_exportar.activated.connect(self.exportar)

        self.shortcut_sair = QShortcut(QKeySequence("Alt+S"), self)
        self.shortcut_sair.activated.connect(exit)

        #BOTÕES
        self.txt_entrada.returnPressed.connect(self.adicionar)
        self.btn_adicionar.clicked.connect(self.adicionar)
        self.btn_estornar.clicked.connect(self.estornar)
        self.btn_sair.clicked.connect(self.sair)

    def abrir_espelho(self, espelho):
        self._espelho = espelho
        self.lbl_espelho.setText(f"Espelho: {self._espelho}")
        self.inserir_tabela(leitura_espelho_db.buscar(self._banco.get_cursor(), self._espelho))
        self.atualizar_label_geral()
    
    def estornar(self):
        self.tela_estorno =  Estorno.Estorno(self._espelho)
        self.tela_estorno.show()
        self.hide()


    
    def exportar(self):
        print("Exportar!")

    def sair(self):
        self.tela = App.Main_Window()
        self.tela.show()
        self.hide()

    def closeEvent(self, event):
        self.tela = App.Main_Window()
        self.tela.show()
        event.accept()

    def adicionar(self):
        self.txt_entrada.setFocus()
        try:
            etiqueta = self.txt_entrada.text()
            if len(etiqueta) == 18 and etiqueta.isnumeric():
                if etiqueta[0] == '0':
                    #print('produto: ', etiqueta[4:8])
                    produto = int(etiqueta[4:8])
                else:
                    #print('produto: ', etiqueta[6:9])
                    produto = int(etiqueta[6:9])
            elif len(etiqueta) == 20 and etiqueta.isnumeric():
                #print('produto: ', etiqueta[4:10])
                produto = int(etiqueta[4:10])
            else:
                self.lbl_aviso.setText(f"Volume {etiqueta} é invalido!")
                msg_erro = CustomDialog("Atenção", f"Volume {etiqueta} é invalido!")
                msg_erro.ui_dialog()
                self.txt_entrada.setText('')
                return False
            if not(leitura_espelho_db.buscar_produto(self._banco.get_cursor(), self._espelho, produto)):
                self.lbl_aviso.setText(f"Volume {etiqueta} não pertence a nenhum produto do espelho!")
                msg_erro = CustomDialog("Atenção", f"""Volume {etiqueta} não pertence
                a nenhum produto do espelho {self._espelho}!""")
                msg_erro.ui_dialog()
                self.txt_entrada.setText('')
                return False
            
            self.txt_entrada.setText('')
            
            if self.verificar_item_restante(produto):
                inclusao = self.verificar_volume(etiqueta)
                if inclusao == 1:              
                    inclusao = leitura_espelho_db.inserir_volume(self._banco.get_cursor(),\
                        self._banco.get_conexao(),\
                            etiqueta, self._espelho,\
                                produto)
            else:
                inclusao = 3

            if inclusao == 1:
                volume_real, peso_real = leitura_espelho_db.buscar_qtde_etqta_lida(self._banco.get_cursor(),\
                self._espelho, produto)
                leitura_espelho_db.atualizar_espelho_lido(self._banco.get_cursor(),\
                self._banco.get_conexao(), self._espelho, produto, volume_real, peso_real)
                tocar = WavePlayerLoop("audio/sucesso.wav")
                tocar.play()
                self.lbl_aviso.setText(f'Volume {etiqueta} incluído')
            elif inclusao == 2:
                tocar = WavePlayerLoop("audio/existe.wav") 
                tocar.play()
                self.lbl_aviso.setText(f"Volume {etiqueta} já incluido!")
            elif inclusao == 3:
                self.lbl_aviso.setText(f"Produto {produto} já atingiu o peso!")
                msg_erro = CustomDialog("Atenção", f"""Produto {produto} já atingiu o peso!""")
                msg_erro.ui_dialog()    
            elif inclusao == 4:
                self.lbl_aviso.setText(f"Volume {etiqueta} pertence a outro espelho!")
                msg_erro = CustomDialog("Atenção", f"""Volume {etiqueta} pertence a outro espelho!""")
                msg_erro.ui_dialog()  
            else:
                print("Não permitido")
                self.lbl_aviso.setText(f"Volume {etiqueta} é invalido!")
                msg_erro = CustomDialog("Atenção", f"Volume {etiqueta} é invalido!")
                msg_erro.ui_dialog()

            self.atualizar_label_geral()
            self.atualizar_tabela()
            self.txt_entrada.setFocus()
        except Exception as e:
            self.txt_entrada.setText('')
            self.txt_entrada.setFocus()
            print("Erro ao adicionar a etiqueta: ", e)

    def verificar_item_restante(self, produto):
        """Verifica se volume que será incluso no espelho aberto
        já teve o número de volume atingido, se caso, NÃO retornar True
        se SIM, retornar False

        Args:
            produto (str): codigo do produto referente ao volume que pretende ser incluso no espelho

        Returns:
            boolean: True ou False
        """        
        volume_restante, peso_restante = leitura_espelho_db.buscar_espelho_produto_restante(self._banco.get_cursor(), self._espelho, int(produto))
        if volume_restante < 0:
            return True
        else:
            return False

    def verificar_volume(self, etiqueta):
        espelho = leitura_espelho_db.buscar_etiqueta(self._banco.get_cursor(), etiqueta)[0]
        if espelho == self._espelho:
            #print("Etiqueta já pertence ao espelho!")
            return 2
        elif espelho == None:
            #print("Etiqueta ainda não registrada")
            return 1
        else:
            #print("Etiqueta pertence a outro espelho!")
            return 4

    def atualizar_tabela(self):
        self.tbl_resumo.setRowCount(0)
        self.inserir_tabela(leitura_espelho_db.buscar(self._banco.get_cursor(), self._espelho))

    def inserir_tabela(self, dados):
        header = self.tbl_resumo.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)

        rowCount = self.tbl_resumo.rowCount()
        cont = len(dados)
        while cont > 0:
            cont -= 1
            self.tbl_resumo.insertRow(rowCount)
            for coluna in range(8):    
                self.tbl_resumo.setItem(rowCount, coluna, QtWidgets.QTableWidgetItem(str(dados[cont][coluna])))
            #self.tbl_resumo.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(str(dados[cont][0])))
            #self.tbl_resumo.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(str(dados[cont][1])))
            #self.tbl_resumo.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(str(dados[cont][2])))
            #self.tbl_resumo.setItem(rowCount, 3, QtWidgets.QTableWidgetItem(str(dados[cont][3])))
            #self.tbl_resumo.setItem(rowCount, 4, QtWidgets.QTableWidgetItem(str(dados[cont][4])))
            #self.tbl_resumo.setItem(rowCount, 5, QtWidgets.QTableWidgetItem(str(dados[cont][5])))
            #self.tbl_resumo.setItem(rowCount, 6, QtWidgets.QTableWidgetItem(str(dados[cont][6])))
            #self.tbl_resumo.setItem(rowCount, 7, QtWidgets.QTableWidgetItem(str(dados[cont][7])))
            #for coluna in range(8):    
                if dados[cont][4] == 0:
                    self.tbl_resumo.item(rowCount, coluna).setBackground(QColor(255,0,0)) #Vermelho
                elif dados[cont][6] == 0:
                    self.tbl_resumo.item(rowCount, coluna).setBackground(QColor(0, 170, 0)) #Verde
                else:
                    self.tbl_resumo.item(rowCount, coluna).setBackground(QColor(255, 255, 0)) #Amarelo

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