# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, QtCore
from ui_instructionDialog import Ui_Dialog

class instructionDialog(QtWidgets.QDialog):
    sendInstruct = QtCore.pyqtSignal(str)

    def __init__(self, instruction):
        super(QtWidgets.QDialog,self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.instructionEdit.setText(instruction)

        # Flag if text was edited
        self.edited = False

        self.ui.okButton.clicked.connect(self.ok_button_pressed)
        self.ui.editButton.clicked.connect(self.edit_button_pressed)

    def edit_button_pressed(self):
        self.edited = True
        self.ui.instructionEdit.setReadOnly(False)

    def ok_button_pressed(self):
        if self.edited:
            self.sendInstruct.emit(self.ui.instructionEdit.toPlainText())
        self.close()
