import sys
import requests
import bs4
from PyQt5 import QtWidgets, QtCore, QtSql, QtGui
from datetime import datetime
from twilio.rest import Client, TwilioException

from ui_MainWindow import Ui_MainWindow
from weather import Weather
from instructionDialog import instructionDialog
from camera import CameraThread


class MainWindow(QtWidgets.QMainWindow):

    # Tab indexes for stacked widget
    tabs = {'Home':0, 'Inventory':1, 'List':2, 'Settings':3, 'Settings2':4, 'Scanner':5, 'ManualEnter':6}

    # Column indexes
    columns = {'Name':0, 'Brand':1, 'Category':2, 'Location':3, 'Quantity':4, 'Date':5, 'UPC':6, 'Instructions':7}

    DEFAULT_ZIP = '98101'

    MAX_CATEGORIES = 10

    MAX_LOCATIONS  = 10

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

            categories = ['Dry Goods', 'Meat', 'Veggies', 'Fruit', 'Dairy', 'Prepared', 'Other']
            self.settings.setValue('categories', categories)

            locations = ['Pantry', 'Fridge', 'Freezer']
            self.settings.setValue('locations', locations)

            self.settings.setValue('hideCursor', False)

        for category in self.settings.value('categories', type=list):
            self.ui.categoryComboBox.addItem(category)
            self.ui.categoriesListWidget.addItem(category)

        for location in self.settings.value('locations', type=list):
            self.ui.locationComboBox.addItem(location)
            self.ui.locationsListWidget.addItem(location)

        self.ui.sidLineEdit.setText(self.settings.value('sid', type=str))
        self.ui.authLineEdit.setText(self.settings.value('authToken', type=str))
        self.ui.fromNumberLineEdit.setText(self.settings.value('fromNumber', type=str))
        self.ui.toNumberLineEdit.setText(self.settings.value('toNumber', type=str))


        self.ui.fullscreenOffButton.setChecked(not self.settings.value('fullscreen', type=bool))
        self.ui.rotateCameraOnButton.setChecked(self.settings.value('rotateCamera', type=bool))
        self.ui.zipEdit.setText(self.settings.value('ZIP'))
        self.ui.hideCursorOnButton.setChecked(self.settings.value('hideCursor', type=bool))

        self.setup_database()

        self.setup_table()

        self.setup_clock()

        self.setup_weather()

        self.setup_connections()



    def setup_database(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('foodventory.db')
        db.open()

        self.query = QtSql.QSqlQuery()
        self.query.exec_("CREATE TABLE food(name TEXT, brand TEXT, category TEXT, location TEXT,"
                         "quantity REAL, date TEXT, UPC TEXT, instructions TEXT)")
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
        self.weather = Weather(self.settings.value('ZIP'))
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
        self.model.setHeaderData(self.columns['Category'], QtCore.Qt.Horizontal, "Category")
        self.model.setHeaderData(self.columns['Location'], QtCore.Qt.Horizontal, "Location")
        self.model.setHeaderData(self.columns['Quantity'], QtCore.Qt.Horizontal, "Qty")
        self.model.setHeaderData(self.columns['Date'], QtCore.Qt.Horizontal, "Date")
        self.model.setHeaderData(self.columns['UPC'], QtCore.Qt.Horizontal, "UPC")

        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setColumnHidden(self.columns['Instructions'], True)


        self.ui.tableView.setColumnWidth(self.columns['Name'], 200)
        self.ui.tableView.setColumnWidth(self.columns['Brand'], 150)
        self.ui.tableView.setColumnWidth(self.columns['Category'], 100)
        self.ui.tableView.setColumnWidth(self.columns['Location'], 80)
        self.ui.tableView.setColumnWidth(self.columns['Quantity'], 10)
        self.ui.tableView.setColumnWidth(self.columns['Date'], 80)
        self.ui.tableView.setColumnWidth(self.columns['UPC'], 140)


        # Setup list table
        self.ui.listTable.setModel(self.listModel)
        self.ui.listTable.horizontalHeader().hide()
        self.ui.listTable.horizontalHeader().setStretchLastSection(True)
        self.ui.listTable.setShowGrid(False)


    def update_table(self):
        self.model.select()


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
        self.ui.invInstructionsButton.clicked.connect(self.inv_instructions_button_pressed)
        self.ui.invFindButton.clicked.connect(self.inv_find_button_pressed)
        self.ui.invSearchLineEdit.returnPressed.connect(self.inv_find_button_pressed)

        # List connections
        self.ui.addButton.clicked.connect(self.add_button_pressed)
        self.ui.listEdit.returnPressed.connect(self.add_button_pressed)
        self.ui.deleteButton.clicked.connect(self.delete_button_pressed)
        self.ui.clearButton.clicked.connect(self.clear_button_pressed)
        self.ui.sendButton.clicked.connect(self.send_button_pressed)

        # Settings connections
        self.ui.exitButton.clicked.connect(self.exit_button_pressed)
        self.ui.saveZipButton.clicked.connect(self.save_zip_button_pressed)

        self.ui.fullscreenOnButton.pressed.connect(self.fullscreen_on_button_pressed)
        self.ui.fullscreenOffButton.pressed.connect(self.fullscreen_off_button_pressed)

        self.ui.rotateCameraOnButton.pressed.connect(self.rotate_camera_on_button_pressed)
        self.ui.rotateCameraOffButton.pressed.connect(self.rotate_camera_off_button_pressed)

        self.ui.hideCursorOnButton.pressed.connect(self.hide_cursor_on_button_pressed)
        self.ui.hideCursorOffButton.pressed.connect(self.hide_cursor_off_button_pressed)

        self.ui.categoriesAddButton.clicked.connect(self.categories_add_button_pressed)
        self.ui.categoriesDeleteButton.clicked.connect(self.categories_delete_button_pressed)
        self.ui.categoriesUpButton.clicked.connect(self.categories_up_button_pressed)
        self.ui.categoriesDownButton.clicked.connect(self.categories_down_button_pressed)
        self.ui.categoriesSaveButton.clicked.connect(self.categories_save_button_pressed)

        self.ui.locationsAddButton.clicked.connect(self.locations_add_button_pressed)
        self.ui.locationsDeleteButton.clicked.connect(self.locations_delete_button_pressed)
        self.ui.locationsUpButton.clicked.connect(self.locations_up_button_pressed)
        self.ui.locationsDownButton.clicked.connect(self.locations_down_button_pressed)
        self.ui.locationsSaveButton.clicked.connect(self.locations_save_button_pressed)

        self.ui.rightButton.clicked.connect(self.right_arrow_button_pressed)
        self.ui.leftButton2.clicked.connect(self.left2_button_pressed)

        self.ui.smsApplyButton.clicked.connect(self.sms_apply_button_pressed)

        self.ui.stackedWidget.currentChanged.connect(self.stack_index_changed)

        # Barcode scanner connections
        self.thread = CameraThread(self)
        self.thread.changePixmap.connect(self.set_image)

        self.thread.sendUPC.connect(self.receive_barcode)
        self.send_rotation.connect(self.thread.receive_rotation)

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
        category = self.ui.categoryComboBox.currentText()
        location = self.ui.locationComboBox.currentText()
        upc =  self.ui.upcLineEdit.text()
        date = self.now.strftime("%m/%d/%y")
        instructions = self.ui.instructionsEdit.toPlainText()

        # Insert into database
        self.query.prepare("INSERT INTO food (name, brand, category, location, quantity, date, upc, instructions) "
                           "VALUES(:name, :brand, :category, :location, :quantity, :date, :upc, :instructions)")

        self.query.bindValue(":quantity", quantity)
        self.query.bindValue(":name", name)
        self.query.bindValue(":brand", brand)
        self.query.bindValue(":category", category)
        self.query.bindValue(":location", location)
        self.query.bindValue(":date", date)
        self.query.bindValue(":upc", upc)
        self.query.bindValue(":instructions", instructions)

        self.query.exec_()

        # Update model view
        self.update_table()

        # Clear line edits
        self.ui.nameLineEdit.clear()
        self.ui.brandLineEdit.clear()
        self.ui.upcLineEdit.clear()
        self.ui.quantitySpinBox.setValue(1.0)

        # Return to home
        self.inv_button_pressed()

    def manual_cancel_button_pressed(self):
        self.ui.nameLineEdit.clear()
        self.ui.brandLineEdit.clear()
        self.ui.upcLineEdit.clear()
        self.ui.locationComboBox.setCurrentIndex(0)
        self.ui.categoryComboBox.setCurrentIndex(0)
        self.ui.stackedWidget.setCurrentIndex(self.tabs['Inventory'])

    def barcode_scan_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['Scanner'])

    # Inventory slots
    def inv_delete_button_pressed(self):
        self.model.removeRow(self.ui.tableView.currentIndex().row())
        self.update_table()

    def inv_add_button_pressed(self):
        self.manual_enter_button_pressed()

    def inv_instructions_button_pressed(self):
        record = self.model.record(self.ui.tableView.currentIndex().row())
        instruct = record.value('instructions')

        self.dialog = instructionDialog(instruct)
        self.dialog.sendInstruct.connect(self.receive_instruct)
        self.dialog.show()

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

    def send_button_pressed(self):

        listMessage = 'x\n\n'

        for row in range(self.listModel.rowCount()):
            listMessage += self.listModel.record(row).value('item') + '\n'

        try:
            client = Client(self.settings.value('sid',type=str), self.settings.value('authToken',type=str))

            client.messages.create(
                 body=listMessage,
                 from_=self.settings.value('fromNumber', type=str),
                 to=self.settings.value('toNumber', type=str)
                 )

            self.ui.listSentLabel.setText('List sent.')

        except TwilioException:
            self.ui.listSentLabel.setText('Error. Check settings.')

        except requests.ConnectionError:
            self.ui.listSentLabel.setText('Connection Error.')


    def receive_instruct(self, instructions):
        record = self.model.record(self.ui.tableView.currentIndex().row())
        record.setValue(self.columns['Instructions'], instructions)
        self.model.setRecord(self.ui.tableView.currentIndex().row(), record)
        self.model.submitAll()

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

    def hide_cursor_on_button_pressed(self):
        self.settings.setValue('hideCursor', True)

    def hide_cursor_off_button_pressed(self):
        self.settings.setValue('hideCursor', False)

    def categories_add_button_pressed(self):
        self.ui.categoriesInfoLabel.clear()

        if self.ui.categoriesListWidget.count() < self.MAX_CATEGORIES:
            self.ui.categoriesListWidget.addItem(self.ui.categoriesLineEdit.text())
        else:
            self.ui.categoriesInfoLabel.setText('Max categories reached.')

        self.ui.categoriesLineEdit.clear()

    def categories_delete_button_pressed(self):
        self.ui.categoriesInfoLabel.clear()
        self.ui.categoriesListWidget.takeItem(self.ui.categoriesListWidget.currentRow())

    def categories_up_button_pressed(self):
        self.ui.categoriesInfoLabel.clear()
        row = self.ui.categoriesListWidget.currentRow()
        item = self.ui.categoriesListWidget.takeItem(self.ui.categoriesListWidget.currentRow())
        self.ui.categoriesListWidget.insertItem(row - 1, item)
        self.ui.categoriesListWidget.setCurrentRow(row - 1)

    def categories_down_button_pressed(self):
        self.ui.categoriesInfoLabel.clear()
        row = self.ui.categoriesListWidget.currentRow()
        item = self.ui.categoriesListWidget.takeItem(self.ui.categoriesListWidget.currentRow())
        self.ui.categoriesListWidget.insertItem(row + 1, item)
        self.ui.categoriesListWidget.setCurrentRow(row + 1)

    def categories_save_button_pressed(self):
        categories = []
        self.ui.categoryComboBox.clear()

        for row in range(self.ui.categoriesListWidget.count()):
            categories.append(self.ui.categoriesListWidget.item(row).text())

        self.ui.categoryComboBox.addItems(categories)

        self.settings.setValue('categories', categories)

        self.ui.categoriesInfoLabel.setText('Categories saved.')


    def locations_add_button_pressed(self):
        self.ui.locationsInfoLabel.clear()

        if self.ui.locationsListWidget.count() < self.MAX_LOCATIONS:
            self.ui.locationsListWidget.addItem(self.ui.locationsLineEdit.text())
        else:
            self.ui.locationsInfoLabel.setText('Max categories reached.')

        self.ui.locationsLineEdit.clear()

    def locations_delete_button_pressed(self):
        self.ui.locationsInfoLabel.clear()
        self.ui.locationsListWidget.takeItem(self.ui.locationsListWidget.currentRow())

    def locations_up_button_pressed(self):
        self.ui.locationsInfoLabel.clear()
        row = self.ui.locationsListWidget.currentRow()
        item = self.ui.locationsListWidget.takeItem(self.ui.locationsListWidget.currentRow())
        self.ui.locationsListWidget.insertItem(row - 1, item)
        self.ui.locationsListWidget.setCurrentRow(row - 1)

    def locations_down_button_pressed(self):
        self.ui.locationsInfoLabel.clear()
        row = self.ui.locationsListWidget.currentRow()
        item = self.ui.locationsListWidget.takeItem(self.ui.locationsListWidget.currentRow())
        self.ui.locationsListWidget.insertItem(row + 1, item)
        self.ui.locationsListWidget.setCurrentRow(row + 1)

    def locations_save_button_pressed(self):
        locations = []
        self.ui.locationComboBox.clear()

        for row in range(self.ui.locationsListWidget.count()):
            locations.append(self.ui.locationsListWidget.item(row).text())

        self.ui.locationComboBox.addItems(locations)

        self.settings.setValue('locations', locations)

        self.ui.locationsInfoLabel.setText('Locations saved.')

    def right_arrow_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['Settings2'])


    # Settings2 Slots

    def left2_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['Settings'])

    def sms_apply_button_pressed(self):
        self.settings.setValue('sid', self.ui.sidLineEdit.text())
        self.settings.setValue('authToken', self.ui.authLineEdit.text())
        self.settings.setValue('fromNumber', self.ui.fromNumberLineEdit.text())
        self.settings.setValue('toNumber', self.ui.toNumberLineEdit.text())




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
            page = 'https://www.barcodelookup.com/{}'.format(upc)


            try:
                req = requests.get(page)
                req.raise_for_status

                barcodePage = bs4.BeautifulSoup(req.text, "html.parser")

                name = barcodePage.find('h4')
                self.ui.nameLineEdit.setText(name.text)

                brand = barcodePage.findAll('span', class_="product-text")
                self.ui.brandLineEdit.setText(brand[2].text)

            except requests.HTTPError:
                print("HTTP Error")

            except requests.ConnectionError:
                print("Connection Error")

            except IndexError:
                self.ui.nameLineEdit.clear()



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    app.setStyleSheet(
    """QWidget
    {
        color: #b1b1b1;
        background-color: #323232;
    }


    QWidget:item:selected
    {
        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #0095ff, stop: 1 #006bff);
    }

    QWidget:disabled
    {
        color: #404040;
        background-color: #323232;
    }

    QAbstractItemView
    {
        color: #d7d7d7;
        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);

        border-width: 1px;
        border-color: #1e1e1e;
        border-style: solid;
        border-radius: 1;
    }

    QLineEdit
    {
        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);
        padding: 1px;
        border-style: solid;
        border: 1px solid #1e1e1e;
        border-radius: 1;
    }

    QPushButton
    {
        color: #d7d7d7;
        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
        border-width: 1px;
        border-color: #1e1e1e;
        border-style: solid;
        border-radius: 1;
        padding: 3px;
        font-size: 12px;
        padding-left: 5px;
        padding-right: 5px;
    }

    QPushButton:pressed
    {
        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
    }

    QPushButton:checked
    {
        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
        border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #0095ff, stop: 1 #006bff);
    }

    QPushButton:default
    {
    }

    QComboBox
    {
        selection-background-color: #ffaa00;
        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
        border-style: solid;
        border: 1px solid #1e1e1e;
        border-radius: 5;
    }

    QComboBox:hover,QPushButton:hover
    {
        border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #0095ff, stop: 1 #006bff);
    }


    QComboBox:on
    {
        padding-top: 3px;
        padding-left: 4px;
        background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
        selection-background-color: #ffaa00;
    }

    QComboBox QAbstractItemView
    {
        border: 2px solid darkgray;
        selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #0095ff, stop: 1 #006bff);
    }

    QComboBox::drop-down
    {
         subcontrol-origin: padding;
         subcontrol-position: top right;
         width: 15px;

         border-left-width: 0px;
         border-left-color: darkgray;
         border-left-style: solid; /* just a single line */
         border-top-right-radius: 3px; /* same radius as the QComboBox */
         border-bottom-right-radius: 3px;
     }

     QDoubleSpinBox::up-button
     {
         color: #d7d7d7;
         background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
         border-width: 1px;
         border-color: #1e1e1e;
         border-style: solid;
         border-radius: 1;
         padding: 3px;
         font-size: 12px;
         padding-left: 5px;
         padding-right: 5px;
     }

     QDoubleSpinBox::down-button
     {
         color: #d7d7d7;
         background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
         border-width: 1px;
         border-color: #1e1e1e;
         border-style: solid;
         border-radius: 1;
         padding: 3px;
         font-size: 12px;
         padding-left: 5px;
         padding-right: 5px;
     }

     QTextEdit:focus
     {
         border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #0095ff, stop: 1 #006bff);
     }

     QScrollBar:horizontal {
          border: 1px solid #222222;
          background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);
          height: 30px;
          margin: 0px 32px 0 32px;
     }

     QScrollBar::handle:horizontal
     {
           background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #0095ff, stop: 0.5 #006bff, stop: 1 #0095ff);
           min-height: 20px;
           border-radius: 2px;
     }

     QScrollBar::add-line:horizontal {
           border: 1px solid #1b1b19;
           border-radius: 2px;
           background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #0095ff, stop: 1 #006bff);
           width: 30px;
           subcontrol-position: right;
           subcontrol-origin: margin;
     }


     QScrollBar::sub-line:horizontal {
           border: 1px solid #1b1b19;
           border-radius: 2px;
           background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #0095ff, stop: 1 #006bff);
           width: 30px;
          subcontrol-position: left;
          subcontrol-origin: margin;
     }

     QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal
     {
           border: 1px solid black;
           width: 2px;
           height: 2px;
           background: white;
     }

     QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
     {
           background: none;
     }

     QScrollBar:vertical
     {
           background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);
           width: 30px;
           margin: 32px 0 32px 0;
           border: 1px solid #222222;
     }

     QScrollBar::handle:vertical
     {
           background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #0095ff, stop: 0.5 #006bff, stop: 1 #0095ff);
           min-height: 20px;
           border-radius: 2px;
     }

     QScrollBar::add-line:vertical
     {
           border: 1px solid #1b1b19;
           border-radius: 2px;
           background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #0095ff, stop: 1 #006bff);
           height: 30px;
           subcontrol-position: bottom;
           subcontrol-origin: margin;
     }

     QScrollBar::sub-line:vertical
     {
           border: 1px solid #1b1b19;
           border-radius: 2px;
           background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #006bff, stop: 1 #0095ff);
           height: 30px;
           subcontrol-position: top;
           subcontrol-origin: margin;
     }

     QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
     {
           border: 1px solid black;
           width: 2px;
           height: 2px;
           background: white;
     }


     QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
     {
           background: none;
     }

     QTextEdit
     {
         background-color: #242424;
     }

     QHeaderView::section
     {
         background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);
         color: white;
         padding-left: 4px;
         border: 1px solid #6c6c6c;
     }


     QTableView QTableCornerButton::section
     {
        background: #323232;
     }
    """)

    window = MainWindow()

    if window.settings.value('hideCursor', type=bool):
        app.setOverrideCursor(QtCore.Qt.BlankCursor)

    if window.settings.value('fullscreen', type=bool):
        window.showFullScreen()
    else:
        window.show()
    sys.exit(app.exec_())
