from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import sqlite3
from users import Ui_MainWindow as main_interface
from user_dialog import Ui_Dialog as user_interface

class main_window(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = main_interface()
        self.ui.setupUi(self)

        self.read_users()
        self.ui.pushButton.clicked.connect(self.open_add_form)
        self.ui.pushButton_2.clicked.connect(self.delete_user)
        self.ui.pushButton_3.clicked.connect(self.open_update_form)
        self.ui.pushButton_4.clicked.connect(self.read_users)

    def read_users(self):
        self.ui.tableWidget.setRowCount(0)
        cursor.execute('SELECT * FROM Users')
        self.data = cursor.fetchall()
        
        self.ui.tableWidget.setColumnCount(6)
        self.ui.tableWidget.setRowCount(len(self.data))
        self.ui.tableWidget.setHorizontalHeaderLabels(['ID', 'Username', 'Email', 'Age', 'Active', 'Created'])
        
        for row in range(len(self.data)):
            for col in range(6):
                item = QTableWidgetItem()
                if col == 4:
                    item.setText(str(self.data[row][col]) == '1' and 'Да' or 'Нет')
                elif col == 5:
                    item.setText(str(self.data[row][col]))
                else:
                    item.setText(str(self.data[row][col]))
                self.ui.tableWidget.setItem(row, col, item)
        
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def open_add_form(self):
        self.form = user_window(self)
        self.form.ui.buttonBox.accepted.connect(self.form.create_user)
        self.form.exec()

    def open_update_form(self):
        current_row = self.ui.tableWidget.currentRow()
        if current_row < 0:
            QMessageBox.critical(self, 'Ошибка', 'Выберите запись для изменения', QMessageBox.Ok)
            return
            
        self.form = user_window(self)
        user_data = self.data[current_row]
        self.form.id = user_data[0]

        self.form.ui.lineEdit.setText(str(user_data[1]))
        self.form.ui.lineEdit_2.setText(str(user_data[2]))
        self.form.ui.spinBox.setValue(int(user_data[3]))
        self.form.ui.comboBox.setCurrentIndex(int(user_data[4]))

        self.form.ui.buttonBox.accepted.connect(self.form.update_user)
        self.form.exec()

    def delete_user(self):
        current_row = self.ui.tableWidget.currentRow()
        if current_row < 0:
            QMessageBox.critical(self, 'Ошибка', 'Выберите запись для удаления', QMessageBox.Ok)
            return
            
        user_id = self.data[current_row][0]
        
        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите удалить пользователя?', QMessageBox.Ok | QMessageBox.Cancel)

        if q == QMessageBox.Ok:
            try:
                cursor.execute('DELETE FROM Users WHERE id = ?', [user_id])
                conn.commit()
                self.read_users()
                QMessageBox.information(self, 'Действие выполнено', 'Пользователь был удален', QMessageBox.Ok)
            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка удаления пользователя', QMessageBox.Ok)

class user_window(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = user_interface()
        self.ui.setupUi(self)

    def create_user(self):
        user_data = [
            self.ui.lineEdit.text(),
            self.ui.lineEdit_2.text(),
            self.ui.spinBox.value(),
            self.ui.comboBox.currentIndex()
        ]

        if any([user_data[0] == '', user_data[1] == '']):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните обязательные поля', QMessageBox.Ok)
            return

        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите добавить пользователя?', QMessageBox.Ok | QMessageBox.Cancel)

        if q == QMessageBox.Ok:
            try:
                cursor.execute('INSERT INTO Users(username, email, age, is_active) VALUES(?, ?, ?, ?)', user_data)
                conn.commit()

                main_form.read_users()

                QMessageBox.information(self, 'Действие выполнено', 'Пользователь был добавлен', QMessageBox.Ok)
                self.accept()
                return

            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка добавления пользователя', QMessageBox.Ok)

    def update_user(self):
        user_data = [
            self.ui.lineEdit.text(),
            self.ui.lineEdit_2.text(),
            self.ui.spinBox.value(),
            self.ui.comboBox.currentIndex(),
            self.id
        ]

        if any([user_data[0] == '', user_data[1] == '']):
            QMessageBox.critical(self, 'Действие не выполнено', 'Заполните обязательные поля', QMessageBox.Ok)
            return

        q = QMessageBox.question(self, 'Подтвердите действие', 'Вы действительно хотите изменить пользователя?', QMessageBox.Ok | QMessageBox.Cancel)

        if q == QMessageBox.Ok:
            try:
                cursor.execute('UPDATE Users SET username = ?, email = ?, age = ?, is_active = ? WHERE id = ?', user_data)
                conn.commit()

                main_form.read_users()

                QMessageBox.information(self, 'Действие выполнено', 'Пользователь был изменен', QMessageBox.Ok)
                self.accept()
                return

            except:
                QMessageBox.critical(self, 'Действие не выполнено', 'Ошибка изменения пользователя', QMessageBox.Ok)

app = QApplication(sys.argv)
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

main_form = main_window()
main_form.show()
sys.exit(app.exec_())
cursor.close()
conn.close()
