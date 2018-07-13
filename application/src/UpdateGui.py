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
        self.rpm_interval = 1
        self.pressure_interval = 1
        self.flow_interval = 1
        self.is_ready = False
        self.dht_pin_number = 3
        self.probe_pin_number = 3
        self.current_pin_number = 3
        self.rpm_pin_number = 3
        self.pressure_pin_number = 3
        self.flow_pin_number = 3
        
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
            QLabel[Test=true] {
                text-decoration: underline;
                font-weight: bold;
                font-size: 20px;
            }


        """)

        self.initUi()

    def initUi(self):

        dht_label = QLabel('DHT Sensor:')
        self.dht_value = QLabel('1')
        probe_label = QLabel('Thermal Probe Sensor: ')
        self.probe_value = QLabel('1')
        current_label = QLabel('Current Sensor: ')
        self.current_value = QLabel('1')
        rpm_label = QLabel('RPM Sensor:')
        self.rpm_value = QLabel('1')
        pressure_label = QLabel('Pressure Sensor')
        self.pressure_value = QLabel('1')
        flow_label = QLabel('Flow Sensor:')
        self.flow_value = QLabel('1')
        
        dht_pin_label = QLabel('DHT Pin:')
        self.dht_pin = QLabel('3')
        probe_pin_label = QLabel('Temp Pin: ')
        self.probe_pin = QLabel('3')
        current_pin_label = QLabel('Current Pin: ')
        self.current_pin = QLabel('3')
        rpm_pin_label = QLabel('RPM Pin:')
        self.rpm_pin = QLabel('3')
        pressure_pin_label = QLabel('Pressure Pin:')
        self.pressure_pin = QLabel('3')
        flow_pin_label = QLabel('Flow Pin:')
        self.flow_pin = QLabel('3')
        
        sensor_column = QLabel('Sensors')
        interval_column = QLabel('Interval of Measurement')
        pin_column = QLabel('Pin Number')
        
        sensor_column.setProperty('Test', True)
        interval_column.setProperty('Test', True)
        pin_column.setProperty('Test', True)
        

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
        
        rpmintervalbox = QComboBox(self)
        rpmintervalbox.addItem("1")
        rpmintervalbox.addItem("2")
        rpmintervalbox.addItem("3")
        rpmintervalbox.addItem("4")
        rpmintervalbox.setProperty('Test', True)

        rpmintervalbox.activated[str].connect(self.onRpmLabelChange)        
        
        pressureintervalbox = QComboBox(self)
        pressureintervalbox.addItem("1")
        pressureintervalbox.addItem("2")
        pressureintervalbox.addItem("3")
        pressureintervalbox.addItem("4")
        pressureintervalbox.setProperty('Test', True)

        pressureintervalbox.activated[str].connect(self.onPressureLabelChange)        

        flowintervalbox = QComboBox(self)
        flowintervalbox.addItem("1")
        flowintervalbox.addItem("2")
        flowintervalbox.addItem("3")
        flowintervalbox.addItem("4")
        flowintervalbox.setProperty('Test', True)

        flowintervalbox.activated[str].connect(self.onFlowLabelChange)        


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

        rpm_pin_box = QComboBox(self)
        rpm_pin_box.addItem("3")
        rpm_pin_box.addItem("5")
        rpm_pin_box.addItem("8")
        rpm_pin_box.addItem("10")
        rpm_pin_box.addItem("18")
        rpm_pin_box.setProperty('Test', True)
        
        rpm_pin_box.activated[str].connect(self.onRpmPinChange)
        
        pressure_pin_box = QComboBox(self)
        pressure_pin_box.addItem("3")
        pressure_pin_box.addItem("5")
        pressure_pin_box.addItem("8")
        pressure_pin_box.addItem("10")
        pressure_pin_box.addItem("18")
        pressure_pin_box.setProperty('Test', True)
        
        pressure_pin_box.activated[str].connect(self.onPressurePinChange)

        flow_pin_box = QComboBox(self)
        flow_pin_box.addItem("3")
        flow_pin_box.addItem("5")
        flow_pin_box.addItem("8")
        flow_pin_box.addItem("10")
        flow_pin_box.addItem("18")
        flow_pin_box.setProperty('Test', True)
        
        flow_pin_box.activated[str].connect(self.onFlowPinChange)
        
        new_sensor_box = QComboBox(self)
        new_sensor_box.addItem("DHT Sensor")
        new_sensor_box.addItem("Temperature Probe Sensor")
        new_sensor_box.addItem("RPM Sensor")
        new_sensor_box.addItem("Current Sensor")
        new_sensor_box.addItem("Pressure Sensor")
        new_sensor_box.addItem("Flow Sensor")
        new_sensor_box.setProperty('Test', True)
        
        self.new_sensor_btn = QPushButton("New Sensor", self)
        self.new_sensor_btn.resize(100,50)
        self.new_sensor_btn.setProperty('Test', True)
        self.new_sensor_btn.clicked.connect(self.sensorButtonClick)
        
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.resize(100,50)
        self.submit_btn.setProperty('Test', True)
        self.submit_btn.clicked.connect(self.submitButtonClick)

        grid = QGridLayout()
        grid.setSpacing(10)
        
        
        grid.addWidget(sensor_column, 0, 2)
        grid.addWidget(interval_column, 0, 3)
        grid.addWidget(pin_column, 0, 4)
        
        grid.addWidget(dht_label, 1, 2)
        #grid.addWidget(self.dht_value, 1, 2)
        grid.addWidget(dhtintervalbox, 1, 3)
        
        #grid.addWidget(dht_pin_label, 1, 5)
        #grid.addWidget(self.dht_pin, 1, 4)
        grid.addWidget(dht_pin_box, 1, 4)
        
        grid.addWidget(probe_label, 2, 2)
        #grid.addWidget(self.probe_value, 2, 2)
        grid.addWidget(probeintervalbox, 2, 3)
        
        #grid.addWidget(probe_pin_label, 2, 5)
        #grid.addWidget(self.probe_pin, 2, 4)
        grid.addWidget(probe_pin_box, 2, 4)        
        
        grid.addWidget(current_label, 3, 2)
        #grid.addWidget(self.current_value, 3, 2)
        grid.addWidget(currentintervalbox, 3, 3)
        
        #grid.addWidget(current_pin_label, 3, 5)
        #grid.addWidget(self.current_pin, 3, 4)
        grid.addWidget(current_pin_box, 3, 4)        
        
        grid.addWidget(rpm_label, 4, 2)
        #grid.addWidget(self.rpm_value, 4, 2)
        grid.addWidget(rpmintervalbox, 4, 3)   
        
        #grid.addWidget(rpm_pin_label, 4, 5)
        #grid.addWidget(self.rpm_pin, 4, 4)
        grid.addWidget(rpm_pin_box, 4, 4)
        
        grid.addWidget(pressure_label, 5, 2)
        #grid.addWidget(self.pressure_value, 5, 2)
        grid.addWidget(pressureintervalbox, 5, 3)        

        #grid.addWidget(pressure_pin_label, 5, 5)
        #grid.addWidget(self.pressure_pin, 5, 4)
        grid.addWidget(pressure_pin_box, 5, 4)
        
        grid.addWidget(flow_label, 6, 2)
        #grid.addWidget(self.flow_value, 6, 2)
        grid.addWidget(flowintervalbox, 6, 3)  

        #grid.addWidget(flow_pin_label, 6, 5)
        #grid.addWidget(self.flow_pin, 6, 4)
        grid.addWidget(flow_pin_box, 6, 4)


        grid.addWidget(new_sensor_box, 7, 2)
        grid.addWidget(self.new_sensor_btn, 7, 3)
        grid.addWidget(self.submit_btn, 7, 4)
        
        grid.addWidget(self.pinlayout, 1, 1, -1, 1)
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
    
    def onRpmLabelChange(self, text):
        self.rpm_value.setText(text)
        self.rpm_value.adjustSize()
        self.rpm_interval = int(text)
        
    def onPressureLabelChange(self, text):
        self.pressure_value.setText(text)
        self.pressure_value.adjustSize()
        self.pressure_interval = int(text)        

    def onFlowLabelChange(self, text):
        self.flow_value.setText(text)
        self.flow_value.adjustSize()
        self.flow_interval = int(text)
        
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
    
    def onRpmPinChange(self, text):
        self.rpm_pin.setText(text)
        self.rpm_pin.adjustSize()
        self.rpm_pin_number = int(text)

    def onPressurePinChange(self, text):
        self.pressure_pin.setText(text)
        self.pressure_pin.adjustSize()
        self.pressure_pin_number = int(text)
        
    def onFlowPinChange(self, text):
        self.flow_pin.setText(text)
        self.flow_pin.adjustSize()
        self.flow_pin_number = int(text)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you wish to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            is_ready = True
            event.accept()
        else:
            event.ignore()
    
    def submitButtonClick(self):
        print("Button clicked")
        print(str(self.dht_pin_number))
        print(str(self.probe_pin_number))
        print(str(self.current_pin_number)) 
        self.close()
    
    def sensorButtonClick(self):
        pass
    
    def getDHTInterval(self):
        return float(self.dht_interval)
    def getProbeInterval(self):
        return float(self.probe_interval)
    def getCurrentInterval(self):
        return float(self.current_interval)
    def getRpmInterval(self):
        return float(self.rpm_interval)
    def getPressureInterval(self):
        return float(self.pressure_interval)
    def getFlowInterval(self):
        return float(self.flow_interval)
    
    def getDHTPin(self):
        return float(self.dht_pin_number)
    def getProbePin(self):
        return float(self.probe_pin_number)
    def getCurrentPin(self):
        return float(self.current_pin_number)
    def getRpmPin(self):
        return float(self.rpm_pin_number)
    def getPressurePin(self):
        return float(self.pressure_pin_number)
    def getFlowPin(self):
        return float(self.flow_pin_number)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    screenSize = screen.size()
    
    gui = UpdateGui(screenSize.width()/2, screenSize.height()/2)
    #sys.exit(app.exec_())
    app.exec_()