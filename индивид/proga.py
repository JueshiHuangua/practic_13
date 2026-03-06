from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import sqlite3
from main import Ui_Form as main_interface
from authoris import Ui_Dialog as auth_interface
from mebel import Ui_Dialog as mebel_interface
from client import Ui_Dialog as client_interface
from zakaz import Ui_Dialog as zakaz_interface
from sostav import Ui_Dialog as sostav_interface

class main_window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = main_interface()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))

        self.ui.comboBox.addItems(['Мебель', 'Клиенты', 'Заказы', 'Состав заказа'])
        self.ui.comboBox.currentTextChanged.connect(self.change_table)
        self.ui.pushButton.clicked.connect(self.open_add_form)
        self.ui.tableWidget.itemClicked.connect(self.open_update_form)

        self.change_table()

    def change_table(self):
        self.current_table = self.ui.comboBox.currentText()
        self.read_table()

    def read_table(self):
        self.ui.tableWidget.setRowCount(0)
        
        if self.current_table == 'Мебель':
            cursor.execute('SELECT * FROM мебель')
            self.data = cursor.fetchall()
            self.ui.tableWidget.setColumnCount(1)
            self.ui.tableWidget.setRowCount(len(self.data))
            for row in range(len(self.data)):
                text = ('\n' + str(self.data[row][0]) + ' | ' + str(self.data[row][1]) + ' | ' + 
                    str(self.data[row][7]) + '\nКоличество предметов: ' + 
                    str(self.data[row][3]) + '\nМатериал: ' + 
                    str(self.data[row][4]) + '\nЦвет: ' + 
                    str(self.data[row][5]) + '\nЦена: ' + 
                    str(self.data[row][6]) + ' руб.\nИзготовитель: ' + 
                    str(self.data[row][2]) + '\n')
                item = QTableWidgetItem()
                item.setText(text)
                self.ui.tableWidget.setItem(row, 0, item)
                
        elif self.current_table == 'Клиенты':
            cursor.execute('SELECT * FROM клиент')
            self.data = cursor.fetchall()
            self.ui.tableWidget.setColumnCount(1)
            self.ui.tableWidget.setRowCount(len(self.data))
            for row in range(len(self.data)):
                text = ('\n' + str(self.data[row][0]) + ' | ' + str(self.data[row][1]) + ' ' + 
                    str(self.data[row][2]) + ' ' + 
                    str(self.data[row][3]) + '\n')
                item = QTableWidgetItem()
                item.setText(text)
                self.ui.tableWidget.setItem(row, 0, item)
                
        elif self.current_table == 'Заказы':
            cursor.execute('SELECT * FROM заказ')
            self.data = cursor.fetchall()
            self.ui.tableWidget.setColumnCount(2)
            self.ui.tableWidget.setRowCount(len(self.data))
            for row in range(len(self.data)):
                text = ('\n' + 'Номер: ' + str(self.data[row][0]) + '\nДата: ' + 
                    str(self.data[row][1]) + '\nГород: ' + 
                    str(self.data[row][2]) + '\nАдрес: ' + 
                    str(self.data[row][3]) + '\nКлиент: ' + 
                    str(self.data[row][5]) + '\n')
                item = QTableWidgetItem()
                item.setText(text)
                self.ui.tableWidget.setItem(row, 0, item)
                
                skidka_item = QTableWidgetItem()
                skidka_item.setText(str(self.data[row][4]) + '%')
                self.ui.tableWidget.setItem(row, 1, skidka_item)
                
        elif self.current_table == 'Состав заказа':
            cursor.execute('SELECT * FROM состав_заказа')
            self.data = cursor.fetchall()
            self.ui.tableWidget.setColumnCount(1)
            self.ui.tableWidget.setRowCount(len(self.data))
            for row in range(len(self.data)):
                text = ('\n' + 'ID: ' + str(self.data[row][0]) + '\nЗаказ: ' + 
                    str(self.data[row][1]) + '\nТовар: ' + 
                    str(self.data[row][2]) + '\n')
                item = QTableWidgetItem()
                item.setText(text)
                self.ui.tableWidget.setItem(row, 0, item)
                
        self.ui.tableWidget.resizeRowsToContents()

    def open_add_form(self):
        if self.current_table == 'Мебель':
            self.form = mebel_window(self)
            self.form.ui.buttonBox.accepted.connect(self.form.create_mebel)
        elif self.current_table == 'Клиенты':
            self.form = client_window(self)
            self.form.ui.buttonBox.accepted.connect(self.form.create_client)
        elif self.current_table == 'Заказы':
            self.form = zakaz_window(self)
            self.form.ui.buttonBox.accepted.connect(self.form.create_zakaz)
        elif self.current_table == 'Состав заказа':
            self.form = sostav_window(self)
            self.form.ui.buttonBox.accepted.connect(self.form.create_sostav)
        self.form.exec()

    def open_update_form(self):
        if self.current_table == 'Мебель':
            self.form = mebel_window(self)
            data = self.data[self.ui.tableWidget.currentRow()]
            self.form.id = data[0]
            self.form.ui.lineEdit.setText(str(data[1]))
            self.form.ui.lineEdit_2.setText(str(data[2]))
            self.form.ui.spinBox.setValue(int(data[3]))
            self.form.ui.lineEdit_3.setText(str(data[4]))
            self.form.ui.lineEdit_4.setText(str(data[5]))
            self.form.ui.doubleSpinBox.setValue(float(data[6]))
            self.form.ui.lineEdit_5.setText(str(data[7]))
            self.form.ui.buttonBox.accepted.connect(self.form.update_mebel)
            
        elif self.current_table == 'Клиенты':
            self.form = client_window(self)
            data = self.data[self.ui.tableWidget.currentRow()]
            self.form.id = data[0]
            self.form.ui.lineEdit.setText(str(data[1]))
            self.form.ui.lineEdit_2.setText(str(data[2]))
            self.form.ui.lineEdit_3.setText(str(data[3]))
            self.form.ui.buttonBox.accepted.connect(self.form.update_client)
            
        elif self.current_table == 'Заказы':
            self.form = zakaz_window(self)
            data = self.data[self.ui.tableWidget.currentRow()]
            self.form.id = data[0]
            self.form.ui.lineEdit.setText(str(data[1]))
            self.form.ui.lineEdit_2.setText(str(data[2]))
            self.form.ui.lineEdit_3.setText(str(data[3]))
            self.form.ui.spinBox.setValue(int(data[4]))
            self.form.ui.spinBox_2.setValue(int(data[5]))
            self.form.ui.buttonBox.accepted.connect(self.form.update_zakaz)
            
        elif self.current_table == 'Состав заказа':
            self.form = sostav_window(self)
            data = self.data[self.ui.tableWidget.currentRow()]
            self.form.id = data[0]
            self.form.ui.spinBox.setValue(int(data[1]))
            self.form.ui.spinBox_2.setValue(int(data[2]))
            self.form.ui.buttonBox.accepted.connect(self.form.update_sostav)
            
        self.form.exec()

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

                auth_form.main_form.read_table()

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

                auth_form.main_form.read_table()

                QMessageBox.information(self, 'Действие выполнено', 'Мебель была изменена', QMessageBox.Ok)
                self.accept()
                return

            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка изменения мебели', QMessageBox.Ok)

class client_window(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = client_interface()
        self.ui.setupUi(self)

    def create_client(self):
        client_data = [
            self.ui.lineEdit.text(),
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
        ]

        if any([item == '' for item in client_data]):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните поля', QMessageBox.Ok)
            return

        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите добавить клиента?', QMessageBox.Ok | QMessageBox.Cancel)

        if q == QMessageBox.Ok:
            try:
                cursor.execute('INSERT INTO клиент(фамилия, имя, отчество) VALUES(?, ?, ?)', client_data)
                conn.commit()

                auth_form.main_form.read_table()

                QMessageBox.information(self, 'Действие выполнено', 'Клиент был добавлен', QMessageBox.Ok)
                self.accept()
                return

            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка добавления клиента', QMessageBox.Ok)

    def update_client(self):
        client_data = [
            self.ui.lineEdit.text(),
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.id
        ]

        if any([item == '' for item in client_data]):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните поля', QMessageBox.Ok)
            return

        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите изменить клиента?', QMessageBox.Ok | QMessageBox.Cancel)

        if q == QMessageBox.Ok:
            try:
                cursor.execute('UPDATE клиент SET фамилия = ?, имя = ?, отчество = ? WHERE id = ?', client_data)
                conn.commit()

                auth_form.main_form.read_table()

                QMessageBox.information(self, 'Действие выполнено', 'Клиент был изменен', QMessageBox.Ok)
                self.accept()
                return

            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка изменения клиента', QMessageBox.Ok)

class zakaz_window(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = zakaz_interface()
        self.ui.setupUi(self)

    def create_zakaz(self):
        zakaz_data = [
            self.ui.lineEdit.text(),
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.spinBox.value(),
            self.ui.spinBox_2.value(),
        ]

        if any([self.ui.lineEdit.text() == '', self.ui.lineEdit_2.text() == '', self.ui.lineEdit_3.text() == '']):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните поля', QMessageBox.Ok)
            return

        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите добавить заказ?', QMessageBox.Ok | QMessageBox.Cancel)

        if q == QMessageBox.Ok:
            try:
                cursor.execute('INSERT INTO заказ(дата, город, адрес, скидка, клиент) VALUES(?, ?, ?, ?, ?)', zakaz_data)
                conn.commit()

                auth_form.main_form.read_table()

                QMessageBox.information(self, 'Действие выполнено', 'Заказ был добавлен', QMessageBox.Ok)
                self.accept()
                return

            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка добавления заказа', QMessageBox.Ok)

    def update_zakaz(self):
        zakaz_data = [
            self.ui.lineEdit.text(),
            self.ui.lineEdit_2.text(),
            self.ui.lineEdit_3.text(),
            self.ui.spinBox.value(),
            self.ui.spinBox_2.value(),
            self.id
        ]

        if any([self.ui.lineEdit.text() == '', self.ui.lineEdit_2.text() == '', self.ui.lineEdit_3.text() == '']):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните поля', QMessageBox.Ok)
            return

        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите изменить заказ?', QMessageBox.Ok | QMessageBox.Cancel)

        if q == QMessageBox.Ok:
            try:
                cursor.execute('UPDATE заказ SET дата = ?, город = ?, адрес = ?, скидка = ?, клиент = ? WHERE номер = ?', zakaz_data)
                conn.commit()

                auth_form.main_form.read_table()

                QMessageBox.information(self, 'Действие выполнено', 'Заказ был изменен', QMessageBox.Ok)
                self.accept()
                return

            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка изменения заказа', QMessageBox.Ok)

class sostav_window(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = sostav_interface()
        self.ui.setupUi(self)

    def create_sostav(self):
        sostav_data = [
            self.ui.spinBox.value(),
            self.ui.spinBox_2.value(),
        ]

        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите добавить запись в состав заказа?', QMessageBox.Ok | QMessageBox.Cancel)

        if q == QMessageBox.Ok:
            try:
                cursor.execute('INSERT INTO состав_заказа(заказ, товар) VALUES(?, ?)', sostav_data)
                conn.commit()

                auth_form.main_form.read_table()

                QMessageBox.information(self, 'Действие выполнено', 'Запись была добавлена', QMessageBox.Ok)
                self.accept()
                return

            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка добавления записи', QMessageBox.Ok)

    def update_sostav(self):
        sostav_data = [
            self.ui.spinBox.value(),
            self.ui.spinBox_2.value(),
            self.id
        ]

        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите изменить запись в составе заказа?', QMessageBox.Ok | QMessageBox.Cancel)

        if q == QMessageBox.Ok:
            try:
                cursor.execute('UPDATE состав_заказа SET заказ = ?, товар = ? WHERE id = ?', sostav_data)
                conn.commit()

                auth_form.main_form.read_table()

                QMessageBox.information(self, 'Действие выполнено', 'Запись была изменена', QMessageBox.Ok)
                self.accept()
                return

            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка изменения записи', QMessageBox.Ok)

app = QApplication(sys.argv)
conn = sqlite3.connect('furniture.db')
cursor = conn.cursor()

auth_form = auth_window()
auth_form.show()
sys.exit(app.exec_())
cursor.close()
conn.close()
