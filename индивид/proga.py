from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import sqlite3
from main import Ui_Form as main_interface

class main_window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = main_interface()
        self.ui.setupUi(self)

        self.read_furniture()

    def read_partners(self):
        self.ui.tableWidget.setRowCount(0)
        cursor.execute('SELECT * FROM Partners')
        self.partners_data = cursor.fetchall()


app = QApplication(sys.argv)
conn = sqlite3.connect('furniture.db')
cursor = conn.cursor()
main_form = main_window()

main_form.show()
sys.exit(app.exec_())
cursor.close()
conn.close()

