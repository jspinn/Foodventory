# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'deleteDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(550, 150)
        Dialog.setModal(True)
        self.yesButton = QtWidgets.QPushButton(Dialog)
        self.yesButton.setGeometry(QtCore.QRect(173, 80, 93, 51))
        self.yesButton.setObjectName("yesButton")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        self.cancelButton.setGeometry(QtCore.QRect(283, 80, 93, 51))
        self.cancelButton.setObjectName("cancelButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(35, 20, 481, 41))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.yesButton.setText(_translate("Dialog", "Yes"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))
        self.label.setText(_translate("Dialog", "Are you sure you want to delete?"))
