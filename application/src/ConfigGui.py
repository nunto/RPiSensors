import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QMessageBox, QComboBox, QLabel, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap

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

        self.username_label = QLabel('Username:')
        self.password_label = QLabel('Password:')
        self.sql_label = QLabel('SQL Credentials:')
        self.username_value = None
        self.password_value = None
        self.sql_value = None
                           
        self.username_input = QLineEdit("Username")
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        #enterPress is a function that is linked to the finishing of this if needed
        #password_input.editingFinished.connect(enterPress)
        self.sql_input = QLineEdit()
        
        
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.resize(100,50)
        self.submit_btn.setProperty('Test', True)
        self.submit_btn.clicked.connect(self.buttonClick)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.username_label, 1, 1)
        grid.addWidget(self.username_input, 1, 2)
        
        grid.addWidget(self.password_label, 2, 1)
        grid.addWidget(self.password_input, 2, 2)
        
        grid.addWidget(self.sql_label, 3, 1)
        grid.addWidget(self.sql_input, 3, 2)
        
        grid.addWidget(self.submit_btn, 4, 2)

        #self.pinlayout.setScaledContents(True)
        
        self.setLayout(grid)

        self.resize(self.width, self.height)
        self.center()
        self.setWindowTitle('ConfigGui')
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you wish to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            event.accept()
        else:
            event.ignore()
    
    def buttonClick(self):
        print("Button clicked")
        is_ready = True
        self.username_value = self.username_input.text()
        self.password_value = self.password_input.text()
        self.sql_value = self.sql_input.text()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    screenSize = screen.size()
    
    gui = ConfigGui(screenSize.width()/2, screenSize.height()/2)
    #sys.exit(app.exec_())
    app.exec_()
