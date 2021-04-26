#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
 
class ColoredTable(QtWidgets.QTableWidget):
    def __init__(self, parent):
        super().__init__()
        item = QtWidgets.QTableWidgetItem()
        self.defaultBrush = (item.foreground(), item.background())
        self.itemChanged.connect(self._itemChanged)
        self._setup()
 
    def _setup(self):
        self.setRowCount(4)
        self.setColumnCount(2)
        txt = ("a", "b", "c", "d")
        for row in range(4):
            for col in range(2):
                item = QtWidgets.QTableWidgetItem()
                item.setText(txt[row])
                if col == 0:
                    item.setCheckState(False)
                self.setItem(row, col, item)
 
    def _itemChanged(self, item):
        if bool(item.checkState()):
            fg = QtGui.QColor("#004000")
            bg = QtGui.QColor("#C6EFCE")
        else:
            fg, bg = self.defaultBrush
 
        row = item.row()
        self.itemChanged.disconnect()
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                item.setForeground(fg)
                item.setBackground(bg)
        self.itemChanged.connect(self._itemChanged)
 
 
class Main(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.ui = QtWidgets.QWidget(self)
        self.setCentralWidget(self.ui)
        self.ui.table = ColoredTable(self)
        self.ui.layout = QtWidgets.QVBoxLayout()
        self.ui.layout.addWidget(self.ui.table)
        self.ui.setLayout(self.ui.layout)
        self.show()
 
 
if __name__== '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = Main(app)
    sys.exit(app.exec_())