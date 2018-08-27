import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QMessageBox, QComboBox, QLabel, QGridLayout, QPushButton, QLineEdit
import pyodbc
import pickle
import os
from configparser import ConfigParser

class ConfigGui (QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.is_ready = False
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
        self.userPassword.setEchoMode(QLineEdit.Password)
        self.tableName = QLineEdit(self)
        self.hostName = QLineEdit(self)
        self.portAddress = QLineEdit(self)
        
        #if there is a file named configuration.pickle and it is not empty, use the data in it to set the default values of the input fields
        if(os.path.exists('configuration.pickle') and os.path.getsize('configuration.pickle') > 0):
            with open('configuration.pickle', 'rb') as handle:
                b = pickle.load(handle)
            handle.close()
            self.dataBase.setText(b[0])
            self.userLogin.setText(b[1])
            self.tableName.setText(b[3])
        
        self.dataBaseLabel = QLabel("Database:")
        self.userLoginLabel = QLabel("User Login:")
        self.userPasswordLabel = QLabel("Password:")
        self.tableNameLabel = QLabel("Table Name:")
        self.hostNameLabel = QLabel("Host:")
        self.portAddressLabel = QLabel("Port Address")
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
        
        grid.addWidget(self.hostNameLabel, 5, 1)
        grid.addWidget(self.hostName, 5, 2)
        
        grid.addWidget(self.portAddressLabel, 6, 1)
        grid.addWidget(self.portAddress, 6, 2)
        
        grid.addWidget(self.buttonLogin, 7, 2)
        
        self.setLayout(grid)

        self.resize(self.width, self.height)
        self.center()
        self.setWindowTitle('Login')
        self.show()
    ## @brief Center everything in the frame   
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    ## @brief Attempt to connect to SQL with the credentials given by the user. If it doesn't work, throw an error
    def handleLogin(self):
        self.hostname = self.hostName.text()
        self.dsn = 'sqlserverdatasource'
        self.db = self.dataBase.text()
        
        if(self.portAddress.isModified()):
            self.portaddress = self.portAddress.text()
        else:
            self.portaddress = str(1433)
        
        cp = ConfigParser() 
        cp.optionxform = str # Preserves case sensitivity
        cp.read_file(open('/etc/freetds/freetds.conf'))
        section = 'sqlserver'
        options = {'host': self.hostname,
                   'port': self.portaddress,
                   'tds version': str(7.0)}
        for option, value in options.items():
            cp.set(section, option, value)
        with open('/etc/freetds/freetds.conf', 'w') as configfile:
            cp.write(configfile)
        
        cp2 = ConfigParser() 
        cp2.optionxform = str # Preserves case sensitivity
        cp2.read_file(open('/etc/odbc.ini'))
        section = 'sqlserverdatasource'
        options = {'Driver': 'FreeTDS',
                   'Description': 'ODBC connection to SQL Server',
                   'Trace': 'None',
                   'Servername': 'sqlserver',
                   'Database': self.db}
        for option, value in options.items():
            cp2.set(section, option, value)
        with open('/etc/odbc.ini', 'w') as configfile:
            cp2.write(configfile)
        
        self.uid = self.userLogin.text()
        self.pwd = self.userPassword.text()
        self.tablename = self.tableName.text()
        
        #creating a connection string based on what the user inputted
        self.cnxn_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (self.dsn, self.uid, self.pwd, self.db)
        print(self.cnxn_string)
        self.config_settings  = [self.db, self.uid, self.pwd, self.tablename]
        
        #dump the values that the user input into a pickle file
        with open('configuration.pickle', 'wb') as handle:
            pickle.dump(self.config_settings, handle, protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()
                        
        #Try to connect, if unable to, tell the user to try again
        try:
            self.cnxn = pyodbc.connect(self.cnxn_string)
            self.is_ready = True
            self.close()
        except pyodbc.Error:
            QMessageBox.warning(self, 'Error', 'Unable to connect, try again')

        
 


if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    screenSize = screen.size()
    
    gui = ConfigGui(screenSize.width()/2, screenSize.height()/2)
    app.exec_()
