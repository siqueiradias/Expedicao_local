from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QShortcut, QFileDialog
from PyQt5.QtGui import QKeySequence
#from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMenuBar, QMenu, QAction
#from PyKDE4.kdeui import KDateComboBox
#import sqlite3
#import datetime
import os
import sys

import leitura_espelho
import cadastrar_espelho
from exportar import Exportar
from factory_db import factory_db


class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self._lista_etiquetas = list()
        #self._DB = 'dao/base/BD_EXPEDICAO.db'
        self._banco = factory_db()
        uic.loadUi("gui/view/tela_inicio.ui", self)
        self.txt_espelho.setFocus()

        self.leitura = leitura_espelho.Leitura()
        self.cadastrar = cadastrar_espelho.Cadastrar()

        #TECLAS DE ATALHOS
        self.shortcut_cadastar = QShortcut(QKeySequence("Alt+C"), self)
        self.shortcut_cadastar.activated.connect(self.cadastrar_espelho)

        self.shortcut_abrir = QShortcut(QKeySequence("Alt+A"), self)
        self.shortcut_abrir.activated.connect(self.abrir)

        self.shortcut_exportar = QShortcut(QKeySequence("Alt+E"), self)
        self.shortcut_exportar.activated.connect(self.abrir)

        self.shortcut_sair = QShortcut(QKeySequence("Alt+S"), self)
        self.shortcut_sair.activated.connect(exit)

        #BOTÕES
        self.btn_sair.clicked.connect(exit)
        self.btn_cadastrar.clicked.connect(self.cadastrar_espelho)
        self.btn_abrir.clicked.connect(self.abrir)
        self.btn_exportar.clicked.connect(self.exportar)

        #LINE EDIT - Ativação dos botões
        self.txt_espelho.textChanged.connect(self.ativar_botoes)
        self.btn_cadastrar.setEnabled(False)
        self.btn_abrir.setEnabled(False)
        self.btn_exportar.setEnabled(False)
        
        #ENTER
        #self.btn_sair.released.connect(exit)
        #self.btn_cadastrar.toggle.connect(self.cadastrar_espelho)
        #self.btn_abrir.released.connect(self.abrir)
        #self.btn_exportar.pressed.connect(self.exportar)

    def ativar_botoes(self):
        """Verificar se foi digitado o espelho
        se SIM, ativar ativa os botões
        """
        if self.txt_espelho.text() == "":
            self.btn_cadastrar.setEnabled(False)
            self.btn_abrir.setEnabled(False)
            self.btn_exportar.setEnabled(False)
        else:
            self.btn_cadastrar.setEnabled(True)
            self.btn_abrir.setEnabled(True)
            self.btn_exportar.setEnabled(True)

    def cadastrar_espelho(self):
        self.cadastrar.novo_espelho(str(self.txt_espelho.text()))
        self.cadastrar.show()
        self.hide()
        
    def abrir(self):
        if self.btn_abrir.isEnabled():
            self.leitura.abrir_espelho(str(self.txt_espelho.text()))
            self.leitura.showMaximized()
            self.hide()
    
    def exportar(self):
        print("Botão exportado!")
        formatos = {
            'csv': "Arq. separado por vírgula (*.csv)",
            'xlsx': "Arquivo excel (*.xlsx)",
            'txt': "Arquivo de texto (*.txt)"
        }
        try:
            arquivo = QFileDialog.getSaveFileName(self, "Onde salvar?", "",\
                (f"{formatos['csv']};;{formatos['xlsx']};;{formatos['txt']}"))

            if arquivo[1] == formatos['csv']:
                Exportar.exp_to_csv(self._banco.get_conexao(), self.txt_espelho.text(), arquivo[0])
            elif arquivo[1] == formatos['xlsx']:
                Exportar.exp_to_excel(self._banco.get_conexao(), self.txt_espelho.text(), arquivo[0])
            elif arquivo[1] == formatos['txt']:
                Exportar.exp_to_txt(self._banco.get_conexao(), self.txt_espelho.text(), arquivo[0])
            
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Notificação")
            msg_box.setText("Arquivo salvo com sucesso!")
            
            return_value = msg_box.exec()
            
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("ERRO")
            msg_box.setText("Erro ao salvar arquivo!")
            msg_box.setDetailedText(e)
            return_value = msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Main_Window()
    w.show()
    sys.exit(app.exec_())

"""if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    janela = Main_Window()
    janela.show()
    sys.exit(app.exec_())"""
