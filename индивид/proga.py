from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import sqlite3
from main import Ui_Form as main_interface
from authoris import Ui_Dialog as auth_interface
from mebel import Ui_Dialog as mebel_interface

class main_window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = main_interface()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))

        self.read_furniture()
        self.ui.pushButton.clicked.connect(self.open_add_mebel_form)
        self.ui.tableWidget.itemClicked.connect(self.open_update_mebel_form)

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

    def open_add_mebel_form(self):
        self.mebel_form = mebel_window(self)
        self.mebel_form.ui.buttonBox.accepted.connect(self.mebel_form.create_mebel)
        self.mebel_form.exec()

    def open_update_mebel_form(self):
        self.mebel_form = mebel_window(self)
        mebel_data = self.data[self.ui.tableWidget.currentRow()]
        self.mebel_form.id = mebel_data[0]

        self.mebel_form.ui.lineEdit.setText(str(mebel_data[1]))
        self.mebel_form.ui.lineEdit_2.setText(str(mebel_data[2]))
        self.mebel_form.ui.spinBox.setValue(int(mebel_data[3]))
        self.mebel_form.ui.lineEdit_3.setText(str(mebel_data[4]))
        self.mebel_form.ui.lineEdit_4.setText(str(mebel_data[5]))
        self.mebel_form.ui.doubleSpinBox.setValue(float(mebel_data[6]))
        self.mebel_form.ui.lineEdit_5.setText(str(mebel_data[7]))

        self.mebel_form.ui.buttonBox.accepted.connect(self.mebel_form.update_mebel)
        self.mebel_form.exec()

class auth_window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = auth_interface()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
        self.ui.pushButton.clicked.connect(self.check)

    def check(self):
        log = self.ui.lineEdit.text()
        pas = self.ui.lineEdit_2.text()
        if log == 'admin' and pas == '1234567':
            self.close()
            self.main_form = main_window()
            self.main_form.show()

class mebel_window(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = mebel_interface()
        self.ui.setupUi(self)

    def create_mebel(self):
        mebel_data = [
            self.ui.lineEdit.text(),
            self.ui.lineEdit_2.text(),
            self.ui.spinBox.value(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text(),
            self.ui.doubleSpinBox.value(),
            self.ui.lineEdit_5.text(),
        ]

        if any([item == '' for item in mebel_data]):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните поля', QMessageBox.Ok)
            return

        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите добавить мебель?', QMessageBox.Ok | QMessageBox.Cancel)

        if q == QMessageBox.Ok:
            try:
                cursor.execute('INSERT INTO мебель(название, страна_изготовитель, количество_предметов, материал, цвет, цена, тип) VALUES(?, ?, ?, ?, ?, ?, ?)', mebel_data)
                conn.commit()

                auth_form.main_form.read_furniture()

                QMessageBox.information(self, 'Действие выполнено', 'Мебель была добавлена', QMessageBox.Ok)
                self.accept()
                return

            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка добавления мебели', QMessageBox.Ok)

    def update_mebel(self):
        mebel_data = [
            self.ui.lineEdit.text(),
            self.ui.lineEdit_2.text(),
            self.ui.spinBox.value(),
            self.ui.lineEdit_3.text(),
            self.ui.lineEdit_4.text(),
            self.ui.doubleSpinBox.value(),
            self.ui.lineEdit_5.text(),
            self.id
        ]

        if any([item == '' for item in mebel_data]):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните поля', QMessageBox.Ok)
            return

        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите изменить мебель?', QMessageBox.Ok | QMessageBox.Cancel)

        if q == QMessageBox.Ok:
            try:
                cursor.execute('UPDATE мебель SET название = ?, страна_изготовитель = ?, количество_предметов = ?, материал = ?, цвет = ?, цена = ?, тип = ? WHERE код_продукции = ?', mebel_data)
                conn.commit()

                auth_form.main_form.read_furniture()

                QMessageBox.information(self, 'Действие выполнено', 'Мебель была изменена', QMessageBox.Ok)
                self.accept()
                return

            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка изменения мебели', QMessageBox.Ok)

app = QApplication(sys.argv)
conn = sqlite3.connect('furniture.db')
cursor = conn.cursor()

auth_form = auth_window()
auth_form.show()
sys.exit(app.exec_())
cursor.close()
conn.close()

