# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtWidgets, QtCore, uic
from datetime import datetime
from ui_MainWindow import Ui_MainWindow

class FoodItem():
    def __init__(self, name, location, barcode):
        self.name = name
        self.location = location
        self.barcode = barcode



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.date_time()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.date_time)
        self.timer.start(1000)

    def date_time(self):
        now = datetime.now()
        self.ui.timeLabel.setText(now.strftime("%I"+":%M:%S"))
        self.ui.dayLabel.setText(now.strftime("%A"))
        self.ui.dateLabel.setText(now.strftime("%d/%m/%Y"))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
