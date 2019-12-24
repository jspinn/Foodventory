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

    # CONNECTIONS

        # Side bar connections
        self.ui.homeButton.clicked.connect(self.home_button_pressed)
        self.ui.invButton.clicked.connect(self.inv_button_pressed)
        self.ui.listButton.clicked.connect(self.list_button_pressed)
        self.ui.settingsButton.clicked.connect(self.settings_button_pressed)

        # Home connections

        # Inventory connections
        self.ui.addButton.clicked.connect(self.add_button_pressed)
        self.ui.deleteButton.clicked.connect(self.delete_button_pressed)
        self.ui.clearButton.clicked.connect(self.clear_button_pressed)

        # List connections

        # Settings connections



    def date_time(self):
        now = datetime.now()
        self.ui.timeLabel.setText(now.strftime("%I"+":%M:%S"))
        self.ui.dayLabel.setText(now.strftime("%A"))
        self.ui.dateLabel.setText(now.strftime("%m/%d/%Y"))

    # SLOTS

    # Side menu slots

    def home_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def inv_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def list_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def settings_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    # Home slots

    # Inventory slots

    # List slots
    def add_button_pressed(self):
        self.ui.listWidget.addItem(u"\u2022 " + self.ui.listEdit.text())
        self.ui.listEdit.clear()

    def delete_button_pressed(self):
        self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())

    def clear_button_pressed(self):
        self.ui.listWidget.clear()

    # Settings slots



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
