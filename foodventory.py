# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtWidgets, QtCore, QtSql, QtGui, uic
from datetime import datetime
from ui_MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Tab indexes for stacked widget
        self.tabs = {'Home':0, 'Inventory':1, 'List':2, 'Settings':3, 'PutAway':4, 'ManualEnter':5}

        # Set up database
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('foodventory.db')
        db.open()

        self.query = QtSql.QSqlQuery()
        self.query.exec_("CREATE TABLE food(name STRING, brand STRING, location STRING, quantity REAL, date STRING, UPC INTEGER)")

#        query.exec_("INSERT INTO food VALUES('Crackers', 'Townhouse', 'Pantry', '08/10/17', 123448689100)")


        self.model = QtSql.QSqlTableModel()

        self.model.setTable('food')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()

        # Qtable headers
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Food Item")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Brand")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Location")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Quantity")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Date")
        self.model.setHeaderData(5, QtCore.Qt.Horizontal, "UPC")

        self.ui.tableView.setModel(self.model)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)


        # Set initial clock
        self.date_time()

        # Set timer for clock
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.date_time)
        self.timer.start(1000)

        # Setup button connections
        self.setup_connections()



    def update_table(self):
        self.model.select()
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)


    def setup_connections(self):
        # Side bar connections
        self.ui.homeButton.clicked.connect(self.home_button_pressed)
        self.ui.invButton.clicked.connect(self.inv_button_pressed)
        self.ui.listButton.clicked.connect(self.list_button_pressed)
        self.ui.settingsButton.clicked.connect(self.settings_button_pressed)

        # Home connections
        self.ui.takeOutButton.clicked.connect(self.take_out_button_pressed)

        self.ui.manualButton.clicked.connect(self.manual_enter_button_pressed)
        self.ui.manualAddButton.clicked.connect(self.manual_add_button_pressed)
        self.ui.manualCancelButton.clicked.connect(self.manual_cancel_button_pressed)

        self.ui.putAwayButton.clicked.connect(self.put_away_button_pressed)

        # Inventory connections
        self.ui.invDeleteButton.clicked.connect(self.inv_delete_button_pressed)
        self.ui.invAddButton.clicked.connect(self.inv_add_button_pressed)
        self.ui.invFindButton.clicked.connect(self.inv_find_button_pressed)
        self.ui.invSearchLineEdit.returnPressed.connect(self.inv_find_button_pressed)

        # List connections
        self.ui.addButton.clicked.connect(self.add_button_pressed)
        self.ui.deleteButton.clicked.connect(self.delete_button_pressed)
        self.ui.clearButton.clicked.connect(self.clear_button_pressed)

        # Settings connections
        self.ui.exitButton.clicked.connect(self.exit_button_pressed)


    def date_time(self):
        self.now = datetime.now()
        self.ui.timeLabel.setText(self.now.strftime("%I"+":%M:%S"))
        self.ui.dayLabel.setText(self.now.strftime("%A"))
        self.ui.dateLabel.setText(self.now.strftime("%m/%d/%y"))

    def find(self, searchText, column=0):
        start = self.model.index(0, column)
        return self.model.match(
            start, QtCore.Qt.DisplayRole,
            searchText, -1, QtCore.Qt.MatchContains)

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
    def put_away_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['PutAway'])

    def manual_enter_button_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(self.tabs['ManualEnter'])

    def manual_add_button_pressed(self):
        quantity = self.ui.quantitySpinBox.value()
        name = self.ui.nameLineEdit.text()
        brand = self.ui.brandLineEdit.text()
        location = self.ui.locationLineEdit.text()
        upc = self.ui.upcLineEdit.text()
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
        self.ui.stackedWidget.setCurrentIndex(self.tabs['Home'])

    def take_out_button_pressed(self):
        pass

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

#            self.ui.tableView.setCurrentIndex(index)
            self.ui.tableView.selectRow(index.row())


    # List slots
    def add_button_pressed(self):
        self.ui.listWidget.addItem(u"\u2022 " + self.ui.listEdit.text())
        self.ui.listEdit.clear()

    def delete_button_pressed(self):
        self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())

    def clear_button_pressed(self):
        self.ui.listWidget.clear()

    # Settings slots
    def exit_button_pressed(self):
        self.close()




if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
