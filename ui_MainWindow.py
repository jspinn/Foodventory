# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("QWidget\n"
"    {\n"
"        color: #b1b1b1;\n"
"        background-color: #323232;\n"
"    }\n"
"\n"
"\n"
"    QWidget:item:selected\n"
"    {\n"
"        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #00eaff);\n"
"    }\n"
"\n"
"    QWidget:disabled\n"
"    {\n"
"        color: #404040;\n"
"        background-color: #323232;\n"
"    }\n"
"\n"
"    QAbstractItemView\n"
"    {\n"
"        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);\n"
"    }\n"
"\n"
"    QWidget:focus\n"
"    {\n"
"        /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #00eaff);*/\n"
"    }\n"
"\n"
"    QLineEdit\n"
"    {\n"
"        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
"        padding: 1px;\n"
"        border-style: solid;\n"
"        border: 1px solid #1e1e1e;\n"
"        border-radius: 5;\n"
"    }\n"
"\n"
"    QPushButton\n"
"    {\n"
"        color: #b1b1b1;\n"
"        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"        border-width: 1px;\n"
"        border-color: #1e1e1e;\n"
"        border-style: solid;\n"
"        border-radius: 6;\n"
"        padding: 3px;\n"
"        font-size: 12px;\n"
"        padding-left: 5px;\n"
"        padding-right: 5px;\n"
"    }\n"
"\n"
"    QPushButton:pressed\n"
"    {\n"
"        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"    }\n"
"\n"
"    QPushButton:checked\n"
"    {\n"
"        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"    }\n"
"\n"
"    QComboBox\n"
"    {\n"
"        selection-background-color: #ffaa00;\n"
"        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"        border-style: solid;\n"
"        border: 1px solid #1e1e1e;\n"
"        border-radius: 5;\n"
"    }\n"
"\n"
"    QComboBox:hover,QPushButton:hover\n"
"    {\n"
"        border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #00eaff);\n"
"    }\n"
"\n"
"\n"
"    QComboBox:on\n"
"    {\n"
"        padding-top: 3px;\n"
"        padding-left: 4px;\n"
"        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"        selection-background-color: #ffaa00;\n"
"    }\n"
"\n"
"    QComboBox QAbstractItemView\n"
"    {\n"
"        border: 2px solid darkgray;\n"
"        selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #00eaff);\n"
"    }\n"
"\n"
"    QComboBox::drop-down\n"
"    {\n"
"         subcontrol-origin: padding;\n"
"         subcontrol-position: top right;\n"
"         width: 15px;\n"
"\n"
"         border-left-width: 0px;\n"
"         border-left-color: darkgray;\n"
"         border-left-style: solid; /* just a single line */\n"
"         border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"         border-bottom-right-radius: 3px;\n"
"     }\n"
"\n"
"     QTextEdit:focus\n"
"     {\n"
"         border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #00eaff);\n"
"     }\n"
"\n"
"     QScrollBar:horizontal {\n"
"          border: 1px solid #222222;\n"
"          background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"          height: 7px;\n"
"          margin: 0px 16px 0 16px;\n"
"     }\n"
"\n"
"     QScrollBar::handle:horizontal\n"
"     {\n"
"           background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #00eaff, stop: 1 #ffa02f);\n"
"           min-height: 20px;\n"
"           border-radius: 2px;\n"
"     }\n"
"\n"
"     QScrollBar::add-line:horizontal {\n"
"           border: 1px solid #1b1b19;\n"
"           border-radius: 2px;\n"
"           background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #00eaff);\n"
"           width: 14px;\n"
"           subcontrol-position: right;\n"
"           subcontrol-origin: margin;\n"
"     }\n"
"\n"
"     QScrollBar::sub-line:horizontal {\n"
"           border: 1px solid #1b1b19;\n"
"           border-radius: 2px;\n"
"           background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #00eaff);\n"
"           width: 14px;\n"
"          subcontrol-position: left;\n"
"          subcontrol-origin: margin;\n"
"     }\n"
"\n"
"     QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal\n"
"     {\n"
"           border: 1px solid black;\n"
"           width: 1px;\n"
"           height: 1px;\n"
"           background: white;\n"
"     }\n"
"\n"
"     QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"     {\n"
"           background: none;\n"
"     }\n"
"\n"
"     QScrollBar:vertical\n"
"     {\n"
"           background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"           width: 7px;\n"
"           margin: 16px 0 16px 0;\n"
"           border: 1px solid #222222;\n"
"     }\n"
"\n"
"     QScrollBar::handle:vertical\n"
"     {\n"
"           background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #00eaff, stop: 1 #ffa02f);\n"
"           min-height: 20px;\n"
"           border-radius: 2px;\n"
"     }\n"
"\n"
"     QScrollBar::add-line:vertical\n"
"     {\n"
"           border: 1px solid #1b1b19;\n"
"           border-radius: 2px;\n"
"           background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #00eaff);\n"
"           height: 14px;\n"
"           subcontrol-position: bottom;\n"
"           subcontrol-origin: margin;\n"
"     }\n"
"\n"
"     QScrollBar::sub-line:vertical\n"
"     {\n"
"           border: 1px solid #1b1b19;\n"
"           border-radius: 2px;\n"
"           background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #00eaff, stop: 1 #ffa02f);\n"
"           height: 14px;\n"
"           subcontrol-position: top;\n"
"           subcontrol-origin: margin;\n"
"     }\n"
"\n"
"     QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"     {\n"
"           border: 1px solid black;\n"
"           width: 1px;\n"
"           height: 1px;\n"
"           background: white;\n"
"     }\n"
"\n"
"\n"
"     QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"     {\n"
"           background: none;\n"
"     }\n"
"\n"
"     QTextEdit\n"
"     {\n"
"         background-color: #242424;\n"
"     }\n"
"\n"
"     QHeaderView::section\n"
"     {\n"
"         background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);\n"
"         color: white;\n"
"         padding-left: 4px;\n"
"         border: 1px solid #6c6c6c;\n"
"     }\n"
"\n"
"\n"
"     QTableView QTableCornerButton::section{\n"
"        background: #323232;\n"
"     }")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(68, 0, 732, 480))
        self.stackedWidget.setObjectName("stackedWidget")
        self.home = QtWidgets.QWidget()
        self.home.setObjectName("home")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.home)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 381, 251))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.timeLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(50)
        self.timeLabel.setFont(font)
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.verticalLayout.addWidget(self.timeLabel)
        self.dateLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(35)
        self.dateLabel.setFont(font)
        self.dateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dateLabel.setObjectName("dateLabel")
        self.verticalLayout.addWidget(self.dateLabel)
        self.dayLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.dayLabel.setFont(font)
        self.dayLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dayLabel.setObjectName("dayLabel")
        self.verticalLayout.addWidget(self.dayLabel)
        self.scanButton = QtWidgets.QPushButton(self.home)
        self.scanButton.setGeometry(QtCore.QRect(220, 310, 271, 131))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.scanButton.setFont(font)
        self.scanButton.setObjectName("scanButton")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.home)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(390, 60, 320, 221))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cityLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.cityLabel.setFont(font)
        self.cityLabel.setScaledContents(True)
        self.cityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.cityLabel.setWordWrap(True)
        self.cityLabel.setObjectName("cityLabel")
        self.verticalLayout_2.addWidget(self.cityLabel)
        self.tempLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.tempLabel.setFont(font)
        self.tempLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tempLabel.setObjectName("tempLabel")
        self.verticalLayout_2.addWidget(self.tempLabel)
        self.weatherPhraseLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.weatherPhraseLabel.setFont(font)
        self.weatherPhraseLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.weatherPhraseLabel.setWordWrap(True)
        self.weatherPhraseLabel.setObjectName("weatherPhraseLabel")
        self.verticalLayout_2.addWidget(self.weatherPhraseLabel)
        self.updateWeatherButton = QtWidgets.QPushButton(self.home)
        self.updateWeatherButton.setGeometry(QtCore.QRect(660, 20, 61, 51))
        self.updateWeatherButton.setObjectName("updateWeatherButton")
        self.stackedWidget.addWidget(self.home)
        self.inventory = QtWidgets.QWidget()
        self.inventory.setObjectName("inventory")
        self.tableView = QtWidgets.QTableView(self.inventory)
        self.tableView.setGeometry(QtCore.QRect(-1, 0, 667, 441))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tableView.setFont(font)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.invAddButton = QtWidgets.QPushButton(self.inventory)
        self.invAddButton.setGeometry(QtCore.QRect(664, -1, 71, 101))
        self.invAddButton.setObjectName("invAddButton")
        self.invDeleteButton = QtWidgets.QPushButton(self.inventory)
        self.invDeleteButton.setGeometry(QtCore.QRect(664, 97, 71, 101))
        self.invDeleteButton.setObjectName("invDeleteButton")
        self.invSearchLineEdit = QtWidgets.QLineEdit(self.inventory)
        self.invSearchLineEdit.setGeometry(QtCore.QRect(70, 440, 272, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.invSearchLineEdit.setFont(font)
        self.invSearchLineEdit.setObjectName("invSearchLineEdit")
        self.invFindButton = QtWidgets.QPushButton(self.inventory)
        self.invFindButton.setGeometry(QtCore.QRect(340, 439, 250, 43))
        self.invFindButton.setObjectName("invFindButton")
        self.invInstructionsButton = QtWidgets.QPushButton(self.inventory)
        self.invInstructionsButton.setGeometry(QtCore.QRect(664, 270, 71, 101))
        self.invInstructionsButton.setObjectName("invInstructionsButton")
        self.stackedWidget.addWidget(self.inventory)
        self.list = QtWidgets.QWidget()
        self.list.setObjectName("list")
        self.listEdit = QtWidgets.QLineEdit(self.list)
        self.listEdit.setGeometry(QtCore.QRect(50, 10, 421, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listEdit.setFont(font)
        self.listEdit.setObjectName("listEdit")
        self.addButton = QtWidgets.QPushButton(self.list)
        self.addButton.setGeometry(QtCore.QRect(520, 30, 121, 101))
        self.addButton.setObjectName("addButton")
        self.deleteButton = QtWidgets.QPushButton(self.list)
        self.deleteButton.setGeometry(QtCore.QRect(520, 160, 121, 101))
        self.deleteButton.setObjectName("deleteButton")
        self.clearButton = QtWidgets.QPushButton(self.list)
        self.clearButton.setGeometry(QtCore.QRect(520, 290, 121, 101))
        self.clearButton.setObjectName("clearButton")
        self.listTable = QtWidgets.QTableView(self.list)
        self.listTable.setGeometry(QtCore.QRect(50, 50, 421, 390))
        self.listTable.setObjectName("listTable")
        self.stackedWidget.addWidget(self.list)
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.exitButton = QtWidgets.QPushButton(self.settings)
        self.exitButton.setGeometry(QtCore.QRect(550, 370, 141, 81))
        self.exitButton.setObjectName("exitButton")
        self.zipEdit = QtWidgets.QLineEdit(self.settings)
        self.zipEdit.setGeometry(QtCore.QRect(170, 120, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.zipEdit.setFont(font)
        self.zipEdit.setObjectName("zipEdit")
        self.settingsLabel = QtWidgets.QLabel(self.settings)
        self.settingsLabel.setGeometry(QtCore.QRect(220, 10, 261, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.settingsLabel.setFont(font)
        self.settingsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.settingsLabel.setObjectName("settingsLabel")
        self.weatherLabel = QtWidgets.QLabel(self.settings)
        self.weatherLabel.setGeometry(QtCore.QRect(120, 80, 101, 21))
        self.weatherLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.weatherLabel.setObjectName("weatherLabel")
        self.zipLabel = QtWidgets.QLabel(self.settings)
        self.zipLabel.setGeometry(QtCore.QRect(40, 128, 91, 21))
        self.zipLabel.setObjectName("zipLabel")
        self.fullscreenOnButton = QtWidgets.QPushButton(self.settings)
        self.fullscreenOnButton.setGeometry(QtCore.QRect(170, 190, 61, 41))
        self.fullscreenOnButton.setCheckable(True)
        self.fullscreenOnButton.setChecked(True)
        self.fullscreenOnButton.setAutoExclusive(False)
        self.fullscreenOnButton.setObjectName("fullscreenOnButton")
        self.fullscreenButtonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.fullscreenButtonGroup.setObjectName("fullscreenButtonGroup")
        self.fullscreenButtonGroup.addButton(self.fullscreenOnButton)
        self.fullscreenLabel = QtWidgets.QLabel(self.settings)
        self.fullscreenLabel.setGeometry(QtCore.QRect(40, 199, 91, 21))
        self.fullscreenLabel.setObjectName("fullscreenLabel")
        self.fullscreenOffButton = QtWidgets.QPushButton(self.settings)
        self.fullscreenOffButton.setGeometry(QtCore.QRect(228, 190, 61, 41))
        self.fullscreenOffButton.setCheckable(True)
        self.fullscreenOffButton.setObjectName("fullscreenOffButton")
        self.fullscreenButtonGroup.addButton(self.fullscreenOffButton)
        self.saveZipButton = QtWidgets.QPushButton(self.settings)
        self.saveZipButton.setGeometry(QtCore.QRect(270, 120, 51, 41))
        self.saveZipButton.setObjectName("saveZipButton")
        self.rotateCameraOnButton = QtWidgets.QPushButton(self.settings)
        self.rotateCameraOnButton.setGeometry(QtCore.QRect(170, 250, 61, 41))
        self.rotateCameraOnButton.setCheckable(True)
        self.rotateCameraOnButton.setChecked(False)
        self.rotateCameraOnButton.setAutoExclusive(False)
        self.rotateCameraOnButton.setObjectName("rotateCameraOnButton")
        self.rotateCameraButtonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.rotateCameraButtonGroup.setObjectName("rotateCameraButtonGroup")
        self.rotateCameraButtonGroup.addButton(self.rotateCameraOnButton)
        self.rotateCameraOffButton = QtWidgets.QPushButton(self.settings)
        self.rotateCameraOffButton.setGeometry(QtCore.QRect(228, 250, 61, 41))
        self.rotateCameraOffButton.setCheckable(True)
        self.rotateCameraOffButton.setChecked(True)
        self.rotateCameraOffButton.setObjectName("rotateCameraOffButton")
        self.rotateCameraButtonGroup.addButton(self.rotateCameraOffButton)
        self.rotateCameraLabel = QtWidgets.QLabel(self.settings)
        self.rotateCameraLabel.setGeometry(QtCore.QRect(40, 260, 121, 16))
        self.rotateCameraLabel.setObjectName("rotateCameraLabel")
        self.stackedWidget.addWidget(self.settings)
        self.scanner = QtWidgets.QWidget()
        self.scanner.setObjectName("scanner")
        self.manualButton = QtWidgets.QPushButton(self.scanner)
        self.manualButton.setGeometry(QtCore.QRect(230, 390, 221, 71))
        self.manualButton.setObjectName("manualButton")
        self.imageView = QtWidgets.QLabel(self.scanner)
        self.imageView.setGeometry(QtCore.QRect(30, 20, 640, 355))
        self.imageView.setAlignment(QtCore.Qt.AlignCenter)
        self.imageView.setObjectName("imageView")
        self.stackedWidget.addWidget(self.scanner)
        self.manualEnter = QtWidgets.QWidget()
        self.manualEnter.setObjectName("manualEnter")
        self.nameLineEdit = QtWidgets.QLineEdit(self.manualEnter)
        self.nameLineEdit.setGeometry(QtCore.QRect(70, 20, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.nameLineEdit.setFont(font)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.brandLineEdit = QtWidgets.QLineEdit(self.manualEnter)
        self.brandLineEdit.setGeometry(QtCore.QRect(70, 80, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.brandLineEdit.setFont(font)
        self.brandLineEdit.setObjectName("brandLineEdit")
        self.upcLineEdit = QtWidgets.QLineEdit(self.manualEnter)
        self.upcLineEdit.setGeometry(QtCore.QRect(70, 260, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.upcLineEdit.setFont(font)
        self.upcLineEdit.setClearButtonEnabled(False)
        self.upcLineEdit.setObjectName("upcLineEdit")
        self.manualAddButton = QtWidgets.QPushButton(self.manualEnter)
        self.manualAddButton.setGeometry(QtCore.QRect(540, 130, 131, 81))
        self.manualAddButton.setObjectName("manualAddButton")
        self.manualCancelButton = QtWidgets.QPushButton(self.manualEnter)
        self.manualCancelButton.setGeometry(QtCore.QRect(540, 250, 131, 81))
        self.manualCancelButton.setObjectName("manualCancelButton")
        self.label = QtWidgets.QLabel(self.manualEnter)
        self.label.setGeometry(QtCore.QRect(330, 60, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.barcodeScanButton = QtWidgets.QPushButton(self.manualEnter)
        self.barcodeScanButton.setGeometry(QtCore.QRect(300, 220, 131, 81))
        self.barcodeScanButton.setObjectName("barcodeScanButton")
        self.quantitySpinBox = QtWidgets.QDoubleSpinBox(self.manualEnter)
        self.quantitySpinBox.setGeometry(QtCore.QRect(280, 110, 181, 91))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.quantitySpinBox.setFont(font)
        self.quantitySpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.quantitySpinBox.setProperty("value", 1.0)
        self.quantitySpinBox.setObjectName("quantitySpinBox")
        self.instructionsEdit = QtWidgets.QTextEdit(self.manualEnter)
        self.instructionsEdit.setGeometry(QtCore.QRect(70, 320, 391, 151))
        self.instructionsEdit.setObjectName("instructionsEdit")
        self.categoryComboBox = QtWidgets.QComboBox(self.manualEnter)
        self.categoryComboBox.setGeometry(QtCore.QRect(70, 140, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.categoryComboBox.setFont(font)
        self.categoryComboBox.setObjectName("categoryComboBox")
        self.locationComboBox = QtWidgets.QComboBox(self.manualEnter)
        self.locationComboBox.setGeometry(QtCore.QRect(70, 200, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.locationComboBox.setFont(font)
        self.locationComboBox.setObjectName("locationComboBox")
        self.stackedWidget.addWidget(self.manualEnter)
        self.homeButton = QtWidgets.QPushButton(self.centralwidget)
        self.homeButton.setGeometry(QtCore.QRect(-1, 0, 70, 120))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.homeButton.setFont(font)
        self.homeButton.setObjectName("homeButton")
        self.invButton = QtWidgets.QPushButton(self.centralwidget)
        self.invButton.setGeometry(QtCore.QRect(-1, 120, 70, 120))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.invButton.setFont(font)
        self.invButton.setObjectName("invButton")
        self.listButton = QtWidgets.QPushButton(self.centralwidget)
        self.listButton.setGeometry(QtCore.QRect(-1, 240, 70, 120))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.listButton.setFont(font)
        self.listButton.setObjectName("listButton")
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setGeometry(QtCore.QRect(-1, 360, 70, 120))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.settingsButton.setFont(font)
        self.settingsButton.setObjectName("settingsButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Foodventory"))
        self.timeLabel.setText(_translate("MainWindow", "TIME"))
        self.dateLabel.setText(_translate("MainWindow", "DATE"))
        self.dayLabel.setText(_translate("MainWindow", "DAY"))
        self.scanButton.setText(_translate("MainWindow", "SCAN"))
        self.cityLabel.setText(_translate("MainWindow", "City"))
        self.tempLabel.setText(_translate("MainWindow", "Temp"))
        self.weatherPhraseLabel.setText(_translate("MainWindow", "Phrase"))
        self.updateWeatherButton.setText(_translate("MainWindow", "Update"))
        self.invAddButton.setText(_translate("MainWindow", "Add"))
        self.invDeleteButton.setText(_translate("MainWindow", "Delete"))
        self.invSearchLineEdit.setPlaceholderText(_translate("MainWindow", "Search..."))
        self.invFindButton.setText(_translate("MainWindow", "Find"))
        self.invInstructionsButton.setText(_translate("MainWindow", "Instruct"))
        self.listEdit.setPlaceholderText(_translate("MainWindow", "New item..."))
        self.addButton.setText(_translate("MainWindow", "Add"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))
        self.clearButton.setText(_translate("MainWindow", "Clear"))
        self.exitButton.setText(_translate("MainWindow", "EXIT"))
        self.zipEdit.setPlaceholderText(_translate("MainWindow", "ZIP Code"))
        self.settingsLabel.setText(_translate("MainWindow", "Settings"))
        self.weatherLabel.setText(_translate("MainWindow", "Weather"))
        self.zipLabel.setText(_translate("MainWindow", "ZIP Code:"))
        self.fullscreenOnButton.setText(_translate("MainWindow", "ON"))
        self.fullscreenLabel.setText(_translate("MainWindow", "Fullscreen:"))
        self.fullscreenOffButton.setText(_translate("MainWindow", "OFF"))
        self.saveZipButton.setText(_translate("MainWindow", "Save"))
        self.rotateCameraOnButton.setText(_translate("MainWindow", "ON"))
        self.rotateCameraOffButton.setText(_translate("MainWindow", "OFF"))
        self.rotateCameraLabel.setText(_translate("MainWindow", "Rotate Camera:"))
        self.manualButton.setText(_translate("MainWindow", "Enter Manually"))
        self.imageView.setText(_translate("MainWindow", "Loading Camera..."))
        self.nameLineEdit.setPlaceholderText(_translate("MainWindow", "Name"))
        self.brandLineEdit.setPlaceholderText(_translate("MainWindow", "Brand"))
        self.upcLineEdit.setPlaceholderText(_translate("MainWindow", "UPC"))
        self.manualAddButton.setText(_translate("MainWindow", "Add"))
        self.manualCancelButton.setText(_translate("MainWindow", "Cancel"))
        self.label.setText(_translate("MainWindow", "Quantity"))
        self.barcodeScanButton.setText(_translate("MainWindow", "Barcode Scan"))
        self.instructionsEdit.setPlaceholderText(_translate("MainWindow", "Instructions..."))
        self.homeButton.setText(_translate("MainWindow", "HOME"))
        self.invButton.setText(_translate("MainWindow", "INV"))
        self.listButton.setText(_translate("MainWindow", "LIST"))
        self.settingsButton.setText(_translate("MainWindow", "SETTINGS"))
