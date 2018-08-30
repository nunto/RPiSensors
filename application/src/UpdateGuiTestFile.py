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
        
        self.SensorList = []
        self.DHTList = []
        self.ThermalList = []
        self.RPMList = []
        self.CurrentList = []
        self.PressureList = []
        self.FlowList = []
        
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
        
        sensor_column = QLabel('Sensors')
        interval_column = QLabel('Interval of Measurement')
        pin_column = QLabel('Pin Number')
        
        sensor_column.setProperty('Test', True)
        interval_column.setProperty('Test', True)
        pin_column.setProperty('Test', True)
        

        self.pinlayout = QLabel(self)
        self.pinlayout.setPixmap(QPixmap('RPiPinLayout.png'))

        
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
        
        grid.addWidget(new_sensor_box, 5, 2)
        grid.addWidget(self.new_sensor_btn, 5, 3)
        grid.addWidget(self.submit_btn, 5, 4)
        
        grid.addWidget(self.pinlayout, 1, 1, -1, 1)
        #self.pinlayout.setScaledContents(True)
        
        self.setLayout(grid)

        self.resize(self.width, self.height)
        self.center()
        self.setWindowTitle('UpdateGui')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def submitButtonClick(self):
        print("Button clicked")
        print(str(self.dht_pin_number))
        print(str(self.probe_pin_number))
        print(str(self.current_pin_number)) 
        self.close()
    
    def sensorButtonClick(self):
        if(new_sensor_box.activated[str] == "DHT Sensor"):
            DHT = DHTSensorGui()
            SensorList.append(DHT)
            grid.addWidget(SensorList[-1].dht_label, SensorList[-1:], 2)
            grid.addWidget(SensorList[-1].dhtintervalbox, SensorList[-1:], 3)
            grid.addWidget(SensorList[-1].dht_pin_box, SensorList[-1:], 4)
            self.setLayout(grid)
            
        elif(new_sensor_box.activated[str] == "Temperature Probe Sensor"):
            Thermal = ThermalSensorGui()
            SensorList.append(Thermal)
            grid.addWidget(SensorList[-1].probe_label, SensorList[-1:], 2)
            grid.addWidget(SensorList[-1].probeintervalbox, SensorList[-1:], 3)
            grid.addWidget(SensorList[-1].probe_pin_box, SensorList[-1:], 4)
            self.setLayout(grid)
            
        elif(new_sensor_box.activated[str] == "RPM Sensor"):
            grid.addWidget(SensorList[-1].rpm_label, SensorList[-1:], 2)
            grid.addWidget(SensorList[-1].rpmintervalbox, SensorList[-1:], 3)
            grid.addWidget(SensorList[-1].rpm_pin_box, SensorList[-1:], 4)
            self.setLayout(grid)
    
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
        return int(self.dht_pin_number)
    def getProbePin(self):
        return int(self.probe_pin_number)
    def getCurrentPin(self):
        return int(self.current_pin_number)
    def getRpmPin(self):
        return int(self.rpm_pin_number)
    def getPressurePin(self):
        return int(self.pressure_pin_number)
    def getFlowPin(self):
        return int(self.flow_pin_number)

class DHTSensorGUI():
    def __init__(self):
        self.dht_label = QLabel('DHT Sensor:')   
        self.dht_interval = 1
        self.dht_pin_number = 2
        
        self.dhtintervalbox = QComboBox(self)
        self.dhtintervalbox.addItem("1")
        self.dhtintervalbox.addItem("2")
        self.dhtintervalbox.addItem("3")
        self.dhtintervalbox.addItem("4")
        self.dhtintervalbox.setProperty('Test', True)
        self.dhtintervalbox.activated[str].connect(self.onDHTIntervalChange)
        
        self.dht_pin_box = QComboBox(self)
        self.dht_pin_box.addItem("2")
        self.dht_pin_box.addItem("3")
        self.dht_pin_box.addItem("14")
        self.dht_pin_box.addItem("15")
        self.dht_pin_box.addItem("18")
        self.dht_pin_box.setProperty('Test', True)
        self.dht_pin_box.activated[str].connect(self.onDHTPinChange)
    
    def onDHTIntervalChange(self, text):
        self.dht_interval = int(text)
    
    def onDHTPinChange(self, text):
        self.dht_pin_number = int(text)

class ThermalSensorGUI():
    def __init__(self):
        self.probe_label = QLabel('Thermal Probe Sensor: ')
        self.probe_interval = 1
        self.probe_pin_number = 2
        
        self.probeintervalbox = QComboBox(self)
        self.probeintervalbox.addItem("1")
        self.probeintervalbox.addItem("2")
        self.probeintervalbox.addItem("3")
        self.probeintervalbox.addItem("4")
        self.probeintervalbox.setProperty('Test', True)
        self.probeintervalbox.activated[str].connect(self.onprobeIntervalChange)
        
        self.probe_pin_box = QComboBox(self)
        self.probe_pin_box.addItem("2")
        self.probe_pin_box.addItem("3")
        self.probe_pin_box.addItem("14")
        self.probe_pin_box.addItem("15")
        self.probe_pin_box.addItem("18")
        self.probe_pin_box.setProperty('Test', True)
        self.probe_pin_box.activated[str].connect(self.onprobePinChange)
    
    def onProbeIntervalChange(self, text):
        self.probe_interval = int(text)
    
    def onProbePinChange(self, text):
        self.probe_pin_number = int(text)
        

class RPMSensorGUI():
    def __init__(self):
        self.rpm_label = QLabel('RPM Sensor: ')
        self.rpm_interval = 1
        self.rpm_pin_number = 2
        
        self.rpmintervalbox = QComboBox(self)
        self.rpmintervalbox.addItem("1")
        self.rpmintervalbox.addItem("2")
        self.rpmintervalbox.addItem("3")
        self.rpmintervalbox.addItem("4")
        self.rpmintervalbox.setProperty('Test', True)
        self.rpmintervalbox.activated[str].connect(self.onRPMIntervalChange)
        
        self.rpm_pin_box = QComboBox(self)
        self.rpm_pin_box.addItem("2")
        self.rpm_pin_box.addItem("3")
        self.rpm_pin_box.addItem("14")
        self.rpm_pin_box.addItem("15")
        self.rpm_pin_box.addItem("18")
        self.rpm_pin_box.setProperty('Test', True)
        self.rpm_pin_box.activated[str].connect(self.onRPMPinChange)
    
    def onRPMIntervalChange(self, text):
        self.rpm_interval = int(text)
    
    def onRPMPinChange(self, text):
        self.rpm_pin_number = int(text)
        
class CurrentSensorGUI():
    def __init__(self):
        self.current_label = QLabel('Current Sensor: ')
        self.current_interval = 1
        self.current_pin_number = 2
        
        self.currentintervalbox = QComboBox(self)
        self.currentintervalbox.addItem("1")
        self.currentintervalbox.addItem("2")
        self.currentintervalbox.addItem("3")
        self.currentintervalbox.addItem("4")
        self.currentintervalbox.setProperty('Test', True)
        self.currentintervalbox.activated[str].connect(self.onCurrentIntervalChange)
        
        self.current_pin_box = QComboBox(self)
        self.current_pin_box.addItem("2")
        self.current_pin_box.addItem("3")
        self.current_pin_box.addItem("14")
        self.current_pin_box.addItem("15")
        self.current_pin_box.addItem("18")
        self.current_pin_box.setProperty('Test', True)
        self.current_pin_box.activated[str].connect(self.onCurrentPinChange)
    
    def onCurrentIntervalChange(self, text):
        self.current_interval = int(text)
    
    def onCurrentPinChange(self, text):
        self.current_pin_number = int(text)
        
class PressureSensorGUI():
    def __init__(self):
        self.pressure_label = QLabel('Pressure Sensor: ')
        self.pressure_interval = 1
        self.pressure_pin_number = 2
        
        self.pressureintervalbox = QComboBox(self)
        self.pressureintervalbox.addItem("1")
        self.pressureintervalbox.addItem("2")
        self.pressureintervalbox.addItem("3")
        self.pressureintervalbox.addItem("4")
        self.pressureintervalbox.setProperty('Test', True)
        self.pressureintervalbox.activated[str].connect(self.onPressureIntervalChange)
        
        self.pressure_pin_box = QComboBox(self)
        self.pressure_pin_box.addItem("2")
        self.pressure_pin_box.addItem("3")
        self.pressure_pin_box.addItem("14")
        self.pressure_pin_box.addItem("15")
        self.pressure_pin_box.addItem("18")
        self.pressure_pin_box.setProperty('Test', True)
        self.pressure_pin_box.activated[str].connect(self.onPressurePinChange)
    
    def onPressureIntervalChange(self, text):
        self.pressure_interval = int(text)
    
    def onPressurePinChange(self, text):
        self.pressure_pin_number = int(text)
        
class FlowSensorGUI():
    def __init__(self):
        self.flow_label = QLabel('flow Sensor: ')
        self.flow_interval = 1
        self.flow_pin_number = 2
        
        self.flowintervalbox = QComboBox(self)
        self.flowintervalbox.addItem("1")
        self.flowintervalbox.addItem("2")
        self.flowintervalbox.addItem("3")
        self.flowintervalbox.addItem("4")
        self.flowintervalbox.setProperty('Test', True)
        self.flowintervalbox.activated[str].connect(self.onFlowIntervalChange)
        
        self.flow_pin_box = QComboBox(self)
        self.flow_pin_box.addItem("2")
        self.flow_pin_box.addItem("3")
        self.flow_pin_box.addItem("14")
        self.flow_pin_box.addItem("15")
        self.flow_pin_box.addItem("18")
        self.flow_pin_box.setProperty('Test', True)
        self.flow_pin_box.activated[str].connect(self.onFlowPinChange)
    
    def onFlowIntervalChange(self, text):
        self.flow_interval = int(text)
    
    def onFlowPinChange(self, text):
        self.flow_pin_number = int(text)
        




if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    screenSize = screen.size()
    
    gui = UpdateGui(screenSize.width()/2, screenSize.height()/2)
    #sys.exit(app.exec_())
    app.exec_()