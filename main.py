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
    def __init__(self, readDelegate, valUp, func):
        Thread.__init__(self)
        self.daemon = True
        self.timerValue = readDelegate
        self.valUpd = valUp
        self.start()
        self.callBoo = func
        print("RUNNING")
        
    def run(self):
        self.timerStatus = False
        self.i = 0
        while True:
            if self.timerStatus:
                self.i = self.i + 1;
            self.timerValue(str(self.i))

            if self.i < 50:
                self.valUpd("Below 50")
            
            else:
                self.valUpd("Above 50")
                self.callBoo("CALLBACK TEST")

            sleep(0.1)

    def stopTimer(self):
        self.i = 0
        self.timerStatus = False
        print("STOPPED")

    def startTimer(self):
        self.timerStatus = True


class AppSignals(QObject):
    timerUpdateSignal = pyqtSignal(str)
    val_update = pyqtSignal(str)

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
        #Start a Thread; Pass on functions that contain pyqtsignal to return value
        self.timerLoop = timerThread(self.timerUpdateDelegate, self.valUpdate, self.updateCB)

        #connect app signals to functions
        self.app_signals.timerUpdateSignal.connect(self.timerUpdate)
        self.app_signals.val_update.connect(self.updateText)

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

    #Signal Definitions

    def timerUpdateDelegate(self, time_update):
        self.app_signals.timerUpdateSignal.emit(time_update)

    def valUpdate(self, val_update):
        self.app_signals.val_update.emit(val_update)

    #UI Updates

    def updateText(self, text):
        self.text_val.setText(text)
    
    def timerUpdate(self, time_update):
        self.count.setText(time_update)
        self.batteryBar.setValue(int(time_update))

    def updateCB(self, text):
        self.testboo.setText(text)


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWindow(None)
    ui.show()
    sys.exit(app.exec_())