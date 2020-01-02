# This Python file uses the following encoding: utf-8
import sys
import requests
from PyQt5 import QtWidgets, QtCore, QtSql, QtGui
from datetime import datetime
import cv2
from pyzbar import pyzbar
from ui_MainWindow import Ui_MainWindow
from weather import Weather

class CameraThread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    sendUPC = QtCore.pyqtSignal(str)

    captureVid = True

    def run(self):
        cap = cv2.VideoCapture(0)

        while self.captureVid:
            captured, frame = cap.read()

            if captured:
                if self.rotation:
                   frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                cv2.waitKey(30)


                barcodes = pyzbar.decode(frame)

                for barcode in barcodes:
                    barcodeData = barcode.data.decode('utf-8')

                    self.sendUPC.emit(barcodeData)

        cap.release()
        cv2.destroyAllWindows()

    @QtCore.pyqtSlot(bool)
    def receive_rotation(self, rotation):
        self.rotation = rotation




class MainWindow(QtWidgets.QMainWindow):

    # Tab indexes for stacked widget
    tabs = {'Home':0, 'Inventory':1, 'List':2, 'Settings':3, 'Scanner':4, 'ManualEnter':5}

    # Column indexes
    columns = {'Name':0, 'Brand':1, 'Location':2, 'Quantity':3, 'Date':4, 'UPC':5}

    DEFAULT_ZIP = '98101'

    settings = QtCore.QSettings("jspinn", "Foodventory")

    send_rotation = QtCore.pyqtSignal(bool)

    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set default settings if first launch
        if self.settings.value('firstLaunch', True, type=bool):
            self.settings.setValue('ZIP', self.DEFAULT_ZIP)
            self.settings.setValue('fullscreen', True)
            self.settings.setValue('rotateCamera', False)
            self.settings.setValue('firstLaunch', False)


        self.ui.fullscreenOffButton.setChecked(not self.settings.value('fullscreen', type=bool))
        self.ui.rotateCameraOnButton.setChecked(self.settings.value('rotateCamera', type=bool))
        self.ui.zipEdit.setText(self.settings.value('ZIP'))

        self.setup_database()

        self.setup_table()

        self.setup_clock()

        self.setup_weather()

        self.setup_connections()




    def setup_connections(self):
        # Side bar connections
        self.ui.homeButton.clicked.connect(self.home_button_pressed)
        self.ui.invButton.clicked.connect(self.inv_button_pressed)
        self.ui.listButton.clicked.connect(self.list_button_pressed)
        self.ui.settingsButton.clicked.connect(self.settings_button_pressed)

        # Home connections
        self.ui.manualButton.clicked.connect(self.manual_enter_button_pressed)
        self.ui.manualAddButton.clicked.connect(self.manual_add_button_pressed)
        self.ui.manualCancelButton.clicked.connect(self.manual_cancel_button_pressed)
        self.ui.barcodeScanButton.clicked.connect(self.barcode_scan_button_pressed)
        self.ui.updateWeatherButton.clicked.connect(self.update_weather)

        self.ui.scanButton.clicked.connect(self.scan_button_pressed)

        # Inventory connections
        self.ui.invDeleteButton.clicked.connect(self.inv_delete_button_pressed)
        self.ui.invAddButton.clicked.connect(self.inv_add_button_pressed)
        self.ui.invFindButton.clicked.connect(self.inv_find_button_pressed)
        self.ui.invSearchLineEdit.returnPressed.connect(self.inv_find_button_pressed)

        # List connections
        self.ui.addButton.clicked.connect(self.add_button_pressed)
        self.ui.listEdit.returnPressed.connect(self.add_button_pressed)
        self.ui.deleteButton.clicked.connect(self.delete_button_pressed)
        self.ui.clearButton.clicked.connect(self.clear_button_pressed)

        # Settings connections
        self.ui.exitButton.clicked.connect(self.exit_button_pressed)
        self.ui.saveZipButton.clicked.connect(self.save_zip_button_pressed)
        self.ui.fullscreenOnButton.pressed.connect(self.fullscreen_on_button_pressed)
        self.ui.fullscreenOffButton.pressed.connect(self.fullscreen_off_button_pressed)
        self.ui.rotateCameraOnButton.pressed.connect(self.rotate_camera_on_button_pressed)
        self.ui.rotateCameraOffButton.pressed.connect(self.rotate_camera_off_button_pressed)

        self.ui.stackedWidget.currentChanged.connect(self.stack_index_changed)

        # Barcode scanner connections
        self.thread = CameraThread(self)
        self.thread.changePixmap.connect(self.set_image)

        self.thread.sendUPC.connect(self.receive_barcode)
        self.send_rotation.connect(self.thread.receive_rotation)

    def setup_database(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('foodventory.db')
        db.open()

        self.query = QtSql.QSqlQuery()
        self.query.exec_("CREATE TABLE food(name TEXT, brand TEXT, location TEXT, quantity REAL, date TEXT, UPC TEXT)")
        self.query.exec_("CREATE TABLE list(item TEXT)")

        self.model = QtSql.QSqlTableModel()
        self.listModel = QtSql.QSqlTableModel()

        self.model.setTable('food')
        self.listModel.setTable('list')

        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.listModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)

        self.model.select()
        self.listModel.select()

    def setup_clock(self):
        # Set initial clock
        self.date_time()

        # Set timer for clock
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.date_time)
        self.timer.start(1000)

    def setup_weather(self):
        self.weather = Weather(self.settings.value('ZIP')) # zip code - REPLACE WITH SETTINGS
        self.update_weather()

        self.weatherTimer = QtCore.QTimer(self)
        self.weatherTimer.timeout.connect(self.update_weather)
        self.weatherTimer.start(3600000) # 1 hour in ms - REPLACE WITH SETTINGS

    def update_weather(self):
        try:
            self.weather.set_weather_page()

            self.ui.cityLabel.setText(self.weather.get_city())
            self.ui.tempLabel.setText(self.weather.get_temp())
            self.ui.weatherPhraseLabel.setText(self.weather.get_phrase())

        except requests.HTTPError:
            self.ui.cityLabel.clear()
            self.ui.tempLabel.setText("Invalid ZIP")
            self.ui.weatherPhraseLabel.setText("Set ZIP code in settings")

        except requests.ConnectionError:
            self.ui.cityLabel.clear()
            self.ui.tempLabel.clear()
            self.ui.weatherPhraseLabel.setText("Connection Error")

        except:
            self.ui.cityLabel.clear()
            self.ui.tempLabel.clear()
            self.ui.weatherPhraseLabel.setText("Error")



    def setup_table(self):
        # Setup inventory table
        self.model.setHeaderData(self.columns['Name'], QtCore.Qt.Horizontal, "Food Item")
        self.model.setHeaderData(self.columns['Brand'], QtCore.Qt.Horizontal, "Brand")
        self.model.setHeaderData(self.columns['Location'], QtCore.Qt.Horizontal, "Location")
        self.model.setHeaderData(self.columns['Quantity'], QtCore.Qt.Horizontal, "Qty")
        self.model.setHeaderData(self.columns['Date'], QtCore.Qt.Horizontal, "Date")
        self.model.setHeaderData(self.columns['UPC'], QtCore.Qt.Horizontal, "UPC")

        self.ui.tableView.setModel(self.model)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)

        # Setup list table
        self.ui.listTable.setModel(self.listModel)
        self.ui.listTable.horizontalHeader().hide()
        self.ui.listTable.horizontalHeader().setStretchLastSection(True)
        self.ui.listTable.setShowGrid(False)


    def update_table(self):
        self.model.select()
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)

    def date_time(self):
        self.now = datetime.now()
        self.ui.timeLabel.setText(self.now.strftime("%I"+":%M:%S"))
        self.ui.dayLabel.setText(self.now.strftime("%A"))
        self.ui.dateLabel.setText(self.now.strftime("%m/%d/%y"))

    def find(self, searchText, column=0, match=QtCore.Qt.MatchContains):
        start = self.model.index(0, column)
        return self.model.match(
            start, QtCore.Qt.DisplayRole,
            searchText, -1, match)

    # SLOTS

    # Side menu slots

    def home_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['Home'])

    def inv_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['Inventory'])

    def list_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['List'])

    def settings_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['Settings'])

    # Home slots
    def scan_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['Scanner'])

    def manual_enter_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['ManualEnter'])

    def manual_add_button_pressed(self):
        quantity = self.ui.quantitySpinBox.value()
        name = self.ui.nameLineEdit.text()
        brand = self.ui.brandLineEdit.text()
        location = self.ui.locationLineEdit.text()
        upc =  self.ui.upcLineEdit.text()
        date = self.now.strftime("%m/%d/%y")

        # Insert into database
        self.query.prepare("INSERT INTO food (name, brand, location, quantity, date, upc) VALUES(:name, :brand, :location, :quantity, :date, :upc)")

        self.query.bindValue(":quantity", quantity)
        self.query.bindValue(":name", name)
        self.query.bindValue(":brand", brand)
        self.query.bindValue(":location", location)
        self.query.bindValue(":date", date)
        self.query.bindValue(":upc", upc)

        self.query.exec_()

        # Update model view
        self.update_table()

        # Clear line edits
        self.ui.nameLineEdit.clear()
        self.ui.brandLineEdit.clear()
        self.ui.locationLineEdit.clear()
        self.ui.upcLineEdit.clear()
        self.ui.quantitySpinBox.setValue(1.0)

        # Return to home
        self.inv_button_pressed()

    def manual_cancel_button_pressed(self):
        self.ui.nameLineEdit.clear()
        self.ui.brandLineEdit.clear()
        self.ui.upcLineEdit.clear()
        self.ui.locationLineEdit.clear()
        self.ui.stackedWidget.setCurrentIndex(self.tabs['Home'])

    def barcode_scan_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['Scanner'])

    # Inventory slots
    def inv_delete_button_pressed(self):
        self.model.removeRow(self.ui.tableView.currentIndex().row())
        self.model.select()

    def inv_add_button_pressed(self):
        self.manual_enter_button_pressed()

    def inv_find_button_pressed(self):
        searchItems = self.find(self.ui.invSearchLineEdit.text())

        if not searchItems:
            searchItems = self.find(self.ui.invSearchLineEdit.text(), 1)

        if searchItems:
            index = searchItems[0]

            self.ui.tableView.selectRow(index.row())


    # List slots
    def add_button_pressed(self):
        listItem = self.ui.listEdit.text()
        self.query.prepare("INSERT INTO list (item) VALUES(:item)")

        self.query.bindValue(":item", listItem)

        self.query.exec_()

        self.listModel.select()

        self.ui.listEdit.clear()
        self.ui.listEdit.setFocus()

    def delete_button_pressed(self):
        self.listModel.removeRow(self.ui.listTable.currentIndex().row())
        self.listModel.select()

    def clear_button_pressed(self):

        for row in range(self.listModel.rowCount()):
            self.listModel.removeRow(row)

        self.listModel.select()


    # Settings slots
    def exit_button_pressed(self):
        self.close()

    def save_zip_button_pressed(self):
        self.settings.setValue('ZIP', self.ui.zipEdit.text())
        self.weather.zip = self.ui.zipEdit.text()
        self.update_weather()

    def fullscreen_on_button_pressed(self):
        self.settings.setValue('fullscreen', True)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.ui.fullscreenOnButton.setChecked(True)

    def fullscreen_off_button_pressed(self):
        self.settings.setValue('fullscreen', False)
        self.showNormal()
        self.ui.fullscreenOffButton.setChecked(True)

    def rotate_camera_on_button_pressed(self):
        self.settings.setValue('rotateCamera', True)

    def rotate_camera_off_button_pressed(self):
        self.settings.setValue('rotateCamera', False)

    # Open/close camera when tabs changed
    def stack_index_changed(self, index):
        if index == self.tabs['Scanner']:
            self.send_rotation.emit(self.settings.value('rotateCamera', type=bool))
            self.thread.captureVid = True
            self.thread.start()
        elif self.thread.isRunning():
            self.thread.captureVid = False
            self.thread.quit()
            self.ui.imageView.setText('Loading Camera...')


    # Video image slot
    @QtCore.pyqtSlot(QtGui.QImage)
    def set_image(self, image):
        self.ui.imageView.setPixmap(QtGui.QPixmap.fromImage(image))

    @QtCore.pyqtSlot(str)
    def receive_barcode(self, upc):

        searchItems = self.find(upc, self.columns['UPC'], QtCore.Qt.MatchContains)

        if searchItems:
            self.ui.stackedWidget.setCurrentIndex(self.tabs['Inventory'])
            index = searchItems[0]

            self.ui.tableView.selectRow(index.row())

        else:
            self.ui.stackedWidget.setCurrentIndex(self.tabs['ManualEnter'])
            self.ui.upcLineEdit.setText(upc)

            # ADD ONLINE NAME SEARCH HERE




if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    if window.settings.value('fullscreen', type=bool):
        window.showFullScreen()
    else:
        window.show()
    sys.exit(app.exec_())
