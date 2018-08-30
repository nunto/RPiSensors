import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QMessageBox, QComboBox, QLabel, QGridLayout, QPushButton, QLineEdit
import pyodbc
import pickle
import os

class ConfigGui (QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.setStyleSheet("""
            QComboBox[Test=true] {
                border: 2px solid #000000;
                background-color: #bbe6ff;
                color: #790000;
            }
            QPushButton[Test=true] {
                border: 2px solid #000000;
                background-color: #bbe6ff;
                color: #790000;
            }
            QPushButton[Test=true]:hover {
                border: 2px solid #00ff00;
                background-color: #bbe66d;
                color: #7934ef;
            }


        """)
        
        self.initUi()
    
    def initUi(self):
        self.dataBase = QLineEdit(self)
        self.userLogin = QLineEdit(self)
        self.userPassword = QLineEdit(self)
        self.tableName = QLineEdit(self)
        
        if(os.path.exists('configuration.pickle') and os.path.getsize('configuration.pickle') > 0):
            with open('configuration.pickle', 'rb') as handle:
                b = pickle.load(handle)
            handle.close()
            self.dataBase.setText(b[0])
            self.userLogin.setText(b[1])
            self.tableName.setText(b[2])
        
        self.dataBaseLabel = QLabel("Database:")
        self.userLoginLabel = QLabel("User Login:")
        self.userPasswordLabel = QLabel("Password:")
        self.tableNameLabel = QLabel("Table Name:")
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.buttonLogin.setProperty('Test', True)
        
        grid = QGridLayout()
        grid.setSpacing(10)

        
        grid.addWidget(self.dataBaseLabel, 1, 1)
        grid.addWidget(self.dataBase, 1, 2)
        
        grid.addWidget(self.userLoginLabel, 2, 1)
        grid.addWidget(self.userLogin, 2, 2)
        
        grid.addWidget(self.userPasswordLabel, 3, 1)
        grid.addWidget(self.userPassword, 3, 2)
        
        grid.addWidget(self.tableNameLabel, 4, 1)
        grid.addWidget(self.tableName, 4, 2)
        
        grid.addWidget(self.buttonLogin, 5, 2)
        
        self.setLayout(grid)

        self.resize(self.width, self.height)
        self.center()
        self.setWindowTitle('Login')
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def handleLogin(self):
        self.dsn = 'sqlserverdatasource'
        self.db = self.dataBase.text()
        self.uid = self.userLogin.text()
        self.pwd = self.userPassword.text()
        self.tablename = self.tableName.text()
        
        self.cnxn_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (self.dsn, self.uid, self.pwd, self.db)
        print(self.cnxn_string)
        self.config_settings  = [self.db, self.uid, self.tablename]
        
        with open('configuration.pickle', 'wb') as handle:
            pickle.dump(self.config_settings, handle, protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()
                        
        
        try:
            self.cnxn = pyodbc.connect(self.cnxn_string)
            self.close()
        except pyodbc.Error:
            QMessageBox.warning(self, 'Error', 'Unable to connect, try again')

        
 


if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    screenSize = screen.size()
    
    gui = ConfigGui(screenSize.width()/2, screenSize.height()/2)
    #sys.exit(app.exec_())
    app.exec_()
