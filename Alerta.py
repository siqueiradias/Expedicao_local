from PyQt5.QtWidgets import (
    QApplication, 
    QMessageBox, 
    QShortcut, 
    QWidget, 
    QPushButton,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout)
import os
import sys

import App
from audio2 import WavePlayerLoop
from time import sleep

class CustomQMessageBox():
    def __init__(self, titulo, texto, detalhe="None"):
        self._titulo = titulo
        self._texto = texto
        self._detalhe = detalhe

    def erro_leitura(self):
        msgBox = QMessageBox()
        """msgBox.setStyleSheet("QLabel {color: rgb(170, 0, 0); font: 800 36pt Cantarell;} \
                QPushButton {font: 500 28pt Cantarell; color: green}")"""
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(self._texto)
        msgBox.setInformativeText("F12 - Fechar")
        msgBox.setWindowTitle(self._titulo)
        #msgBox.setStandardButtons(QMessageBox.Close)
        #msgBox.buttonClicked.connect(QMessageBox.Ok)
        
        returnValue = msgBox.exec()
        #if returnValue == QMessageBox.Close:
        #    print('Fechado')
    
        
    def resultado(self, clicado):
        if clicado == "&Close":
            print("Mensagem de erro finalizada")

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("HELLO!")

        self.layout = QVBoxLayout()
        message = QLabel("Volume 00000000000000 é invalido")
        atalho = QLabel("ESC - SAIR")
        message.setStyleSheet("QLabel {color: rgb(170, 0, 0); font: 800 36pt Cantarell;}")
        atalho.setStyleSheet("QLabel {font: 500 28pt Cantarell; color: green}")
        self.layout.addWidget(message)
        
        self.layout.addWidget(atalho)
        #self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QWidget()
    button1 = QPushButton(win)
    button1.setText("Show dialog!")
    button1.move(50,50)
    ui_msg = CustomQMessageBox("Atenção", "Volume 01020222002354 invalido")

    ui_dialog = CustomDialog()


    #button1.clicked.connect(ui_msg.erro_leitura)
    button1.clicked.connect(ui_dialog.exec_)
    win.setWindowTitle("Click button")
    win.show()
    sys.exit(app.exec_())
"""
    app = QtWidgets.QApplication([])
    janela = Leitura()
    janela.show()
    sys.exit(app.exec_())"""
    