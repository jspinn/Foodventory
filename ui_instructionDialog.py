# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'instructionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setModal(True)
        self.instructionEdit = QtWidgets.QTextEdit(Dialog)
        self.instructionEdit.setGeometry(QtCore.QRect(-1, -1, 314, 303))
        self.instructionEdit.setReadOnly(True)
        self.instructionEdit.setObjectName("instructionEdit")
        self.editButton = QtWidgets.QPushButton(Dialog)
        self.editButton.setGeometry(QtCore.QRect(310, -2, 93, 155))
        self.editButton.setAutoDefault(False)
        self.editButton.setObjectName("editButton")
        self.okButton = QtWidgets.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(310, 150, 93, 152))
        self.okButton.setAutoDefault(False)
        self.okButton.setObjectName("okButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Instructions"))
        self.editButton.setText(_translate("Dialog", "Edit"))
        self.okButton.setText(_translate("Dialog", "OK"))
