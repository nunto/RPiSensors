import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QMessageBox, QComboBox, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap

class UpdateGui (QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        
        self.dht_interval = 1
        self.probe_interval = 1
        self.current_interval = 1
        self.is_ready = False
        self.dht_pin_number = 3
        self.probe_pin_number = 3
        self.current_pin_number = 3
        
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

        dht_label = QLabel('DHT Interval:')
        self.dht_value = QLabel('1')
        probe_label = QLabel('Temp Probe Interval: ')
        self.probe_value = QLabel('1')
        current_label = QLabel('Current Interval: ')
        self.current_value = QLabel('1')
        
        dht_pin_label = QLabel('DHT Pin:')
        self.dht_pin = QLabel('3')
        probe_pin_label = QLabel('Temp Pin: ')
        self.probe_pin = QLabel('3')
        current_pin_label = QLabel('Current Pin: ')
        self.current_pin = QLabel('3')

        # DHT Dropdown
        dhtintervalbox = QComboBox(self)
        dhtintervalbox.addItem("1")
        dhtintervalbox.addItem("2")
        dhtintervalbox.addItem("3")
        dhtintervalbox.addItem("4")
        dhtintervalbox.setProperty('Test', True)

        # On selected item change
        dhtintervalbox.activated[str].connect(self.onDHTLabelChange)

        # Temp Probe Dropdown
        probeintervalbox = QComboBox(self)
        probeintervalbox.addItem("1")
        probeintervalbox.addItem("2")
        probeintervalbox.addItem("3")
        probeintervalbox.addItem("4")
        probeintervalbox.setProperty('Test', True)

        probeintervalbox.activated[str].connect(self.onProbeLabelChange)

        # Current Dropdown
        currentintervalbox = QComboBox(self)
        currentintervalbox.addItem("1")
        currentintervalbox.addItem("2")
        currentintervalbox.addItem("3")
        currentintervalbox.addItem("4")
        currentintervalbox.setProperty('Test', True)

        currentintervalbox.activated[str].connect(self.onCurrentLabelChange)
        
        self.pinlayout = QLabel(self)
        self.pinlayout.setPixmap(QPixmap('RPiPinLayout.png'))
        
        dht_pin_box = QComboBox(self)
        dht_pin_box.addItem("3")
        dht_pin_box.addItem("5")
        dht_pin_box.addItem("8")
        dht_pin_box.addItem("10")
        dht_pin_box.addItem("18")
        dht_pin_box.setProperty('Test', True)
        
        dht_pin_box.activated[str].connect(self.onDHTPinChange)
        
        probe_pin_box = QComboBox(self)
        probe_pin_box.addItem("3")
        probe_pin_box.addItem("5")
        probe_pin_box.addItem("8")
        probe_pin_box.addItem("10")
        probe_pin_box.addItem("18")
        probe_pin_box.setProperty('Test', True)
        
        probe_pin_box.activated[str].connect(self.onProbePinChange)
        
        current_pin_box = QComboBox(self)
        current_pin_box.addItem("3")
        current_pin_box.addItem("5")
        current_pin_box.addItem("8")
        current_pin_box.addItem("10")
        current_pin_box.addItem("18")
        current_pin_box.setProperty('Test', True)
        
        current_pin_box.activated[str].connect(self.onCurrentPinChange)
        
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.resize(100,50)
        self.submit_btn.setProperty('Test', True)
        self.submit_btn.clicked.connect(self.buttonClick)

        grid = QGridLayout()
        grid.setSpacing(1)

        grid.addWidget(dht_label, 1, 2)
        grid.addWidget(self.dht_value, 1, 3)
        grid.addWidget(dhtintervalbox, 1, 4)
        
        grid.addWidget(probe_label, 2, 2)
        grid.addWidget(self.probe_value, 2, 3)
        grid.addWidget(probeintervalbox, 2, 4)
        
        grid.addWidget(current_label, 3, 2)
        grid.addWidget(self.current_value, 3, 3)
        grid.addWidget(currentintervalbox, 3, 4)
        
        grid.addWidget(dht_pin_label, 4, 2)
        grid.addWidget(self.dht_pin, 4, 3)
        grid.addWidget(dht_pin_box, 4, 4)
        
        grid.addWidget(probe_pin_label, 5, 2)
        grid.addWidget(self.probe_pin, 5, 3)
        grid.addWidget(probe_pin_box, 5, 4)
        
        grid.addWidget(current_pin_label, 6, 2)
        grid.addWidget(self.current_pin, 6, 3)
        grid.addWidget(current_pin_box, 6, 4)
        
        grid.addWidget(self.submit_btn, 7, 3)
        
        grid.addWidget(self.pinlayout, 5, 1, -1, 1)
        #self.pinlayout.setScaledContents(True)
        
        self.setLayout(grid)

        self.resize(self.width, self.height)
        self.center()
        self.setWindowTitle('UpdateGui')
        self.show()

    def onDHTLabelChange(self, text):
        self.dht_value.setText(text)
        self.dht_value.adjustSize()
        self.dht_interval = int(text)

    def onProbeLabelChange(self, text):
        self.probe_value.setText(text)
        self.probe_value.adjustSize()
        self.probe_interval = int(text)

    def onCurrentLabelChange(self, text):
        self.current_value.setText(text)
        self.current_value.adjustSize()
        self.current_interval = int(text)
        
    def onDHTPinChange(self, text):
        self.dht_pin.setText(text)
        self.dht_pin.adjustSize()
        self.dht_pin_number = int(text)

    def onProbePinChange(self, text):
        self.probe_pin.setText(text)
        self.probe_pin.adjustSize()
        self.probe_pin_number = int(text)
        
    def onCurrentPinChange(self, text):
        self.current_pin.setText(text)
        self.current_pin.adjustSize()
        self.current_pin_number = int(text)
        
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
        print(str(self.dht_pin_number))
        print(str(self.probe_pin_number))
        print(str(self.current_pin_number))
        is_ready = True
        self.close()
       
    def getDHTInterval():
        return float(dht_interval)
    def getProbeInterval():
        return float(probe_interval)
    def getCurrentInterval():
        return float(current_interval)
    def getDHTPin():
        return float(dht_pin_number)
    def getProbePin():
        return float(probe_pin_number)
    def getCurrentPin():
        return float(current_pin_number)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    screenSize = screen.size()
    
    gui = UpdateGui(screenSize.width()/2, screenSize.height()/2)
    sys.exit(app.exec_())