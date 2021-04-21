import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import pyqtSlot

	
def showDialog():
    msgBox = QMessageBox()
    msgBox.setStyleSheet("QLabel {color: rgb(170, 0, 0); font: 800 36pt Cantarell;} \
            QPushButton {font: 500 28pt Cantarell; color: green}")
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText("O Volume 00000000000 é invalido")
    msgBox.setWindowTitle("Atenção")
    msgBox.setStandardButtons(QMessageBox.Close)
    #msgBox.buttonClicked.connect(QMessageBox.Ok)
    
    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Close:
        print('OK clicked')
   
def msgButtonClick(i):
   print("Button clicked is:",i.text())

	
if __name__ == '__main__': 
    app = QApplication(sys.argv)

    win = QWidget()
    button1 = QPushButton(win)
    button1.setText("Show dialog!")
    button1.move(50,50)
    button1.clicked.connect(showDialog)
    win.setWindowTitle("Click button")
    win.show()
    sys.exit(app.exec_())
