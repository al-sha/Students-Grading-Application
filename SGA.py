from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox, QVBoxLayout, QLineEdit
import sys
from PyQt5.QtPrintSupport import *
import sqlite3
import os
#--------------------------------------------------------------------------------------------------------------------------------
class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()

        self.QBtn = QPushButton()
        self.QBtn.setText("Submit")

        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        

        self.setWindowTitle("Student Information")
        self.setFixedWidth(400)
        self.setFixedHeight(300)

        self.QBtn.clicked.connect(self.addstudent)

        

        self.Lastinput = QLineEdit()
        self.Lastinput.setPlaceholderText("Student ID")
        layout.addWidget(self.Lastinput)

        self.Firstinput = QLineEdit()
        self.Firstinput.setPlaceholderText("Full Name")
        layout.addWidget(self.Firstinput)

        self.Courseinput = QLineEdit()
        self.Courseinput.setPlaceholderText("Course")
        layout.addWidget(self.Courseinput)

        self.Homeworkinput = QLineEdit()
        self.Homeworkinput.setPlaceholderText("Homework grade")
        layout.addWidget(self.Homeworkinput)
        
        self.Testinput = QLineEdit()
        self.Testinput.setPlaceholderText("Test Grade")
        layout.addWidget(self.Testinput)
        
        layout.addWidget(self.QBtn)
        self.setLayout(layout)
#--------------------------------------------------------------------------------------------------------------------------------
    def addstudent(self,widget):

        Last = ""
        First = ""
        Course = ""
        Homework = ""
        Test = ""
        Final = ""

        Last = self.Lastinput.text()
        First = self.Firstinput.text()
        Course = self.Courseinput.text()
        Homework = self.Homeworkinput.text()
        Test = self.Testinput.text()
        Final = (0.3 * int(Homework) + 0.7 * int(Test))
        if Final > 92:
                Final = ("A , "+ str(Final)+"%")
        elif Final >= 90:
                Final = ("A- , "+ str(Final)+"%")
        elif Final >= 86:
                Final = ("B+ , "+ str(Final)+"%")
        elif Final >= 84:
                Final = ("B , "+ str(Final)+"%")
        elif Final >= 80:
                Final = ("B- , "+ str(Final)+"%")
        elif Final >=78:
                Final = ("C+ , "+ str(Final)+"%")
        elif Final >=74:
                Final = ("C , "+ str(Final)+"%")
        elif Final >=70:
                Final = ("C- , "+ str(Final)+"%")
        elif Final >= 68:
                Final = ("D+ , "+ str(Final)+"%")
        elif Final >= 64:
                Final = ("D , "+ str(Final)+"%")
        elif Final >= 60:
                Final = ("D- , "+ str(Final)+"%")
        else:
            Final = ("F , "+ str(Final)+"%")

        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO students (Last, First, Course, Homework, Test, Final ) VALUES (?,?,?,?,?,?)",(Last, First, Course, Homework, Test, Final))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Successful!')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Did not add student to the database.')
#--------------------------------------------------------------------------------------------------------------------------------
class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Delete")

        self.setWindowTitle("Delete Student Record")
        self.setFixedWidth(350)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deletestudent)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Student ID")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)
#--------------------------------------------------------------------------------------------------------------------------------
    def deletestudent(self):

        delrol = ""
        delrol = self.deleteinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("DELETE from students WHERE Last="+str(delrol))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','Deleted From Table Successful')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not Delete student from the database.')


#--------------------------------------------------------------------------------------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('icon1.png'))
        
       
        
    
       

        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS students(Last INTEGER, First TEXT,Course TEXT, Homework INTEGER, Test INTEGER, Final TEXT)")
        self.c.close()

      
        self.setWindowTitle("Student Grading Application")
        self.setMinimumSize(1000, 700)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("ID", "Full Name",  "Course", "Homework grade", "Test grade","Final grade (Letter, Total)"))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction("Add Student", self)   
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Student")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_delete = QAction("Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Delete User")
        toolbar.addAction(btn_ac_delete)

        btn_ac_refresh = QAction("Refresh",self)   
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

      

#--------------------------------------------------------------------------------------------------------------------------------
 

    def loaddata(self):
        self.connection = sqlite3.connect("database.db")
        query = "SELECT * FROM students"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.connection.close()
#--------------------------------------------------------------------------------------------------------------------------------

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()

#--------------------------------------------------------------------------------------------------------------------------------


app = QApplication(sys.argv)
if(QDialog.Accepted == True):
    window = MainWindow()
    window.show()
    window.loaddata()
sys.exit(app.exec_())
