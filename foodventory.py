# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtWidgets, QtCore, QtSql, QtGui
from datetime import datetime
import cv2
from pyzbar import pyzbar
from ui_MainWindow import Ui_MainWindow

class CameraThread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    sendUPC = QtCore.pyqtSignal(str)

    captureVid = True

    def run(self):
#        cap = VideoStream(src=0).start()
        cap = cv2.VideoCapture(0)

        while self.captureVid:
            ret, frame = cap.read()

            if ret:
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




class MainWindow(QtWidgets.QMainWindow):

    # Tab indexes for stacked widget
    tabs = {'Home':0, 'Inventory':1, 'List':2, 'Settings':3, 'Scanner':4, 'ManualEnter':5}

    # Column indexes
    columns = {'Name':0, 'Brand':1, 'Location':2, 'Quantity':3, 'Date':4, 'UPC':5}

    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setup_database()

        self.setup_table()

        self.setup_clock()

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

        self.ui.stackedWidget.currentChanged.connect(self.stack_index_changed)

        # Barcode scanner connections
        self.thread = CameraThread(self)
        self.thread.changePixmap.connect(self.set_image)

        self.thread.sendUPC.connect(self.receive_barcode)

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

    # Open/close camera when tabs changed
    def stack_index_changed(self, index):
        if index == self.tabs['Scanner']:
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
    window.show()
    sys.exit(app.exec_())
