# imports
import sys
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets

# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("main.ui")

# use loaded ui file in the logic class
class mainWindow(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWindow(None)
    ui.showMaximized()
    sys.exit(app.exec_())