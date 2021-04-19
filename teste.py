import sys
from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QMenuBar, QMenu, QAction

from App import *
from leitura_espelho import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Main_Window()
    w.show()
    sys.exit(app.exec_())