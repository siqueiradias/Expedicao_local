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
    QVBoxLayout
    )
from PyQt5.QtCore import Qt
import os
import sys

import App
from audio2 import WavePlayerLoop
from time import sleep

class CustomQMessageBox():
    def __init__(self, titulo, texto, detalhe=None):
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

class CustomDialog():
    """Tela de Dialogo para informar mensagem ao usuario
    com Layout predefinido e emissão de aviso sonoro
    """
    def __init__(self, titulo, texto):
        """Metodo Construtor do Dialogo

        Args:
            titulo (str): Titulo da janela
            texto (str): Informação/Mensagem para o usuario
        """
        self._titulo = titulo
        self._texto = texto

    def ui_dialog(self):
        """Criar a UI predefinida e gerencia as regras
        """
        dialog = QDialog()
        dialog.setWindowTitle(self._titulo)

        dialog.layout = QVBoxLayout()
        #Label 1
        mensagem = QLabel(self._texto)
        mensagem.setStyleSheet("QLabel {color: rgb(170, 0, 0); font: 800 36pt Cantarell;}")
        #Label 2
        atalho = QLabel("ESC - FECHAR")
        atalho.setStyleSheet("QLabel {font: 500 28pt Cantarell; color: green;}")
        atalho.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        dialog.layout.addWidget(mensagem)
        dialog.layout.addWidget(atalho)
        dialog.setLayout(dialog.layout)

        self.tocar = WavePlayerLoop("audio/erro.wav", True)
        self.play()

        return_value = dialog.exec()
        if dialog.isVisible:
            self.stop()
            
    def play(self):
        """Play no audio
        """
        self.tocar.start()
    
    def stop(self):
        """Stop no audio
        """
        self.tocar.stop()

    def closeEvent(self, event):
        self.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QWidget()
    button1 = QPushButton(win)
    button1.setText("Show dialog!")
    button1.move(50,50)
    ui_msg = CustomQMessageBox("Atenção", "Volume 01020222002354 invalido")

    ui_dialog = CustomDialog("Atenção", "Volume 01020222002354 invalido")


    button1.clicked.connect(ui_msg.erro_leitura)
    #button1.clicked.connect(ui_dialog.ui_dialog)
    win.setWindowTitle("Click button")
    win.show()
    sys.exit(app.exec_())
"""
    app = QtWidgets.QApplication([])
    janela = Leitura()
    janela.show()
    sys.exit(app.exec_())"""
    