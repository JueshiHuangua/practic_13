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
        self.setWindowIcon(QIcon('icon.png'))

        self.read_furniture()

    def read_furniture(self):
        self.ui.tableWidget.setRowCount(0)
        cursor.execute('SELECT * FROM мебель')
        self.data = cursor.fetchall()
        print(self.data)
                
        self.ui.tableWidget.setRowCount(len(self.data))
        self.ui.tableWidget.setColumnCount(1)
        for row in range(len(self.data)):
            text = ('\n' + str(self.data[row][1]) + ' | ' + 
                str(self.data[row][7]) + '\nКоличество предметов: ' + 
                str(self.data[row][3]) + '\nМатериал: ' + 
                str(self.data[row][4]) + '\nЦвет: ' + 
                str(self.data[row][5]) + '\nЦена: ' + 
                str(self.data[row][6]) + ' руб.\nИзготовитель: ' + 
                str(self.data[row][2]) + '\n')
            item = QTableWidgetItem()
            item.setText(text)
            self.ui.tableWidget.setItem(row, 0, item)
        self.ui.tableWidget.resizeRowsToContents()


app = QApplication(sys.argv)
conn = sqlite3.connect('furniture.db')
cursor = conn.cursor()
main_form = main_window()

main_form.show()
sys.exit(app.exec_())
cursor.close()
conn.close()

