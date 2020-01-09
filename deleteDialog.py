from PyQt5 import QtWidgets, QtCore
from ui_deleteDialog import Ui_Dialog

class deleteDialog(QtWidgets.QDialog):

    def __init__(self, item):
        super(QtWidgets.QDialog,self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)



        self.ui.label.setText("Are you sure you want to delete '" + item + "'?")

        self.ui.yesButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)
