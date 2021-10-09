# imports
import sys
from time import sleep
from threading import Thread
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QObject


# load ui file
baseUIClass, baseUIWidget = uic.loadUiType("main.ui")

class timerThread(Thread):
    def __init__(self, readDelegate):
        Thread.__init__(self)
        self.daemon = True
        self.timerValue = readDelegate
        self.start()
        print("RUNNING")
        
    def run(self):
        self.timerStatus = False
        self.i = 0
        while True:
            if self.timerStatus:
                self.i = self.i + 1;
            self.timerValue(str(self.i))
            sleep(0.1)

    def stopTimer(self):
        self.i = 0
        self.timerStatus = False
        print("STOPPED")

    def startTimer(self):
        self.timerStatus = True


class AppSignals(QObject):
    timerUpdateSignal = pyqtSignal(str)

# use loaded ui file in the logic class
class mainWindow(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setupUi(self)
        
        #Inital Sates
        self.status.setText("STOPPED")

        #Signals
        #Call Signals
        self.app_signals = AppSignals()
        #Connect Signals to functions

        self.timerLoop = timerThread(self.timerUpdateDelegate)
        self.app_signals.timerUpdateSignal.connect(self.timerUpdate)

        #Connect buttons by its names
        self.start_but.clicked.connect(lambda:self.startCount())
        self.stop_but.clicked.connect(lambda:self.stopCount())


    #Start Count
    def startCount(self):
        self.status.setText("STARTED")
        self.timerLoop.startTimer()
        
    def stopCount(self):
        self.status.setText("STOPPED")
        self.timerLoop.stopTimer()

    def timerUpdateDelegate(self, time_update):
        self.app_signals.timerUpdateSignal.emit(time_update)
    
    def timerUpdate(self, time_update):
        self.count.setText(time_update)
        self.batteryBar.setValue(int(time_update))


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWindow(None)
    #timerLoop = timerThread(ui.timerUpdateDelegate) THIS IS ONE WAY TO START THE THEAD THO
    ui.show()
    sys.exit(app.exec_())