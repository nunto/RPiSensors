import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QMessageBox, QComboBox, QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap
from SensorOBJ import SensorOBJ
import RPi.GPIO as GPIO

class UpdateGui (QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        

        self.is_ready = False
        
        
        self.SensorList = []
        self.SensorObjectList = []

        
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

        
        self.new_sensor_box = QComboBox(self)
        self.new_sensor_box.addItem("DHT Sensor")
        self.new_sensor_box.addItem("Temperature Probe Sensor")
        self.new_sensor_box.addItem("RPM Sensor")
        self.new_sensor_box.addItem("Current Sensor")
        self.new_sensor_box.addItem("Pressure Sensor")
        self.new_sensor_box.addItem("Flow Sensor")
        self.new_sensor_box.setProperty('Test', True)
        
        self.new_sensor_btn = QPushButton("New Sensor", self)
        self.new_sensor_btn.resize(100,50)
        self.new_sensor_btn.setProperty('Test', True)
        self.new_sensor_btn.clicked.connect(self.sensorButtonClick)
        
        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.resize(100,50)
        self.submit_btn.setProperty('Test', True)
        self.submit_btn.clicked.connect(self.submitButtonClick)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        
        
        self.grid.addWidget(sensor_column, 0, 2)
        self.grid.addWidget(interval_column, 0, 3)
        self.grid.addWidget(pin_column, 0, 4)
        
        self.grid.addWidget(self.new_sensor_box, len(self.SensorList) +1, 2)
        self.grid.addWidget(self.new_sensor_btn, len(self.SensorList) +1, 3)
        self.grid.addWidget(self.submit_btn, len(self.SensorList) +1, 4)
        
        self.grid.addWidget(self.pinlayout, 1, 1, -1, 1)
        
        
        self.setLayout(self.grid)

        self.resize(self.width, self.height)
        self.center()
        self.setWindowTitle('UpdateGui')
        self.show()
    
    ## @brief centres the frame
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    ## @brief On the button click, loop through all the sensors, create new SensorOBJ objects that have their specific properties and append them to SensorObjectList, and set the is_ready variable to True to allow for the program to continue
    def submitButtonClick(self):
        print("Button clicked")
        for Sensor in self.SensorList:
            print(Sensor.getInterval())
            if(hasattr(Sensor, 'dht_label')):
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.cleanup
                dht = SensorOBJ(0, Sensor.getInterval(), Sensor.getPin())
                self.SensorObjectList.append(dht)
            elif(hasattr(Sensor, 'probe_label')):
                thermal = SensorOBJ(1, Sensor.getInterval(), Sensor.getPin())
                self.SensorObjectList.append(thermal)
            elif(hasattr(Sensor, 'rpm_label')):
                rpm = SensorOBJ(2, Sensor.getInterval(), Sensor.getPin())
                self.SensorObjectList.append(rpm)
            elif(hasattr(Sensor, 'current_label')):
                current = SensorOBJ(3, Sensor.getInterval(), Sensor.getPin())
                self.SensorObjectList.append(current)
            elif(hasattr(Sensor, 'pressure_label')):
                pressure = SensorOBJ(4, Sensor.getInterval(), Sensor.getPin())
                self.SensorObjectList.append(pressure)
            elif(hasattr(Sensor, 'flow_label')):
                flow = SensorOBJ(5, Sensor.getInterval(), Sensor.getPin())
                self.SensorObjectList.append(flow)
                
        self.is_ready = True
        self.close()
    
    ## @brief Creates a new sensor object on screen based on what is in the dropdown and appends it to SensorList
    def sensorButtonClick(self):      
        if(self.new_sensor_box.currentText() == "DHT Sensor"):
            DHT = DHTSensorGUI()
            self.SensorList.append(DHT)
            self.grid.addWidget(self.SensorList[-1].dht_label, len(self.SensorList), 2)
            self.grid.addWidget(self.SensorList[-1].dhtintervalbox, len(self.SensorList), 3)
            self.grid.addWidget(self.SensorList[-1].dht_pin_box, len(self.SensorList), 4)
            self.grid.addWidget(self.new_sensor_box, len(self.SensorList) +1, 2)
            self.grid.addWidget(self.new_sensor_btn, len(self.SensorList) +1, 3)
            self.grid.addWidget(self.submit_btn, len(self.SensorList) +1, 4)
            self.setLayout(self.grid)
            
        elif(self.new_sensor_box.currentText() == "Temperature Probe Sensor"):
            Thermal = ThermalSensorGUI()
            self.SensorList.append(Thermal)
            self.grid.addWidget(self.SensorList[-1].probe_label, len(self.SensorList), 2)
            self.grid.addWidget(self.SensorList[-1].probeintervalbox, len(self.SensorList), 3)
            self.grid.addWidget(self.SensorList[-1].probe_pin_box, len(self.SensorList), 4)
            self.grid.addWidget(self.new_sensor_box, len(self.SensorList) +1, 2)
            self.grid.addWidget(self.new_sensor_btn, len(self.SensorList) +1, 3)
            self.grid.addWidget(self.submit_btn, len(self.SensorList) +1, 4)
            self.setLayout(self.grid)
            
        elif(self.new_sensor_box.currentText() == "RPM Sensor"):
            Rpm = RPMSensorGUI()
            self.SensorList.append(Rpm)
            self.grid.addWidget(self.SensorList[-1].rpm_label, len(self.SensorList), 2)
            self.grid.addWidget(self.SensorList[-1].rpmintervalbox, len(self.SensorList), 3)
            self.grid.addWidget(self.SensorList[-1].rpm_pin_box, len(self.SensorList), 4)
            self.grid.addWidget(self.new_sensor_box, len(self.SensorList) +1, 2)
            self.grid.addWidget(self.new_sensor_btn, len(self.SensorList) +1, 3)
            self.grid.addWidget(self.submit_btn, len(self.SensorList) +1, 4)
            self.setLayout(self.grid)
        elif(self.new_sensor_box.currentText() == "Current Sensor"):
            Current = CurrentSensorGUI()
            self.SensorList.append(Current)
            self.grid.addWidget(self.SensorList[-1].current_label, len(self.SensorList), 2)
            self.grid.addWidget(self.SensorList[-1].currentintervalbox, len(self.SensorList), 3)
            self.grid.addWidget(self.SensorList[-1].current_pin_box, len(self.SensorList), 4)
            self.grid.addWidget(self.new_sensor_box, len(self.SensorList) +1, 2)
            self.grid.addWidget(self.new_sensor_btn, len(self.SensorList) +1, 3)
            self.grid.addWidget(self.submit_btn, len(self.SensorList) +1, 4)
            self.setLayout(self.grid)
        
        elif(self.new_sensor_box.currentText() == "Pressure Sensor"):
            Pressure = PressureSensorGUI()
            self.SensorList.append(Pressure)
            self.grid.addWidget(self.SensorList[-1].pressure_label, len(self.SensorList), 2)
            self.grid.addWidget(self.SensorList[-1].pressureintervalbox, len(self.SensorList), 3)
            self.grid.addWidget(self.SensorList[-1].pressure_pin_box, len(self.SensorList), 4)
            self.grid.addWidget(self.new_sensor_box, len(self.SensorList) +1, 2)
            self.grid.addWidget(self.new_sensor_btn, len(self.SensorList) +1, 3)
            self.grid.addWidget(self.submit_btn, len(self.SensorList) +1, 4)
            self.setLayout(self.grid)
        
        elif(self.new_sensor_box.currentText() == "Flow Sensor"):
            Flow = FlowSensorGUI()
            self.SensorList.append(Flow)
            self.grid.addWidget(self.SensorList[-1].flow_label, len(self.SensorList), 2)
            self.grid.addWidget(self.SensorList[-1].flowintervalbox, len(self.SensorList), 3)
            self.grid.addWidget(self.SensorList[-1].flow_pin_box, len(self.SensorList), 4)
            self.grid.addWidget(self.new_sensor_box, len(self.SensorList) +1, 2)
            self.grid.addWidget(self.new_sensor_btn, len(self.SensorList) +1, 3)
            self.grid.addWidget(self.submit_btn, len(self.SensorList) +1, 4)
            self.setLayout(self.grid)


class DHTSensorGUI():
    def __init__(self):
        self.dht_label = QLabel('DHT Sensor:')   
        self.dht_interval = 1
        self.dht_pin_number = 2
        
        self.dhtintervalbox = QComboBox()
        self.dhtintervalbox.addItem("1")
        self.dhtintervalbox.addItem("2")
        self.dhtintervalbox.addItem("3")
        self.dhtintervalbox.addItem("4")
        self.dhtintervalbox.setProperty('Test', True)
        self.dhtintervalbox.activated[str].connect(self.onDHTIntervalChange)
        
        self.dht_pin_box = QComboBox()
        self.dht_pin_box.addItem("2")
        self.dht_pin_box.addItem("3")
        self.dht_pin_box.addItem("14")
        self.dht_pin_box.addItem("15")
        self.dht_pin_box.addItem("18")
        self.dht_pin_box.setProperty('Test', True)
        self.dht_pin_box.activated[str].connect(self.onDHTPinChange)
    
    ## @brief Changes interval to what is specified in the dropdown
    def onDHTIntervalChange(self, text):
        self.dht_interval = int(text)
    
    ## @brief Changes pin to what is specified in the dropdown
    def onDHTPinChange(self, text):
        self.dht_pin_number = int(text)
    
    ## @brief Gets the interval of this object
    #  @return Returns the interval as an int in seconds
    def getInterval(self):
        return self.dht_interval
    
    ## @brief Gets the pin for this object
    #  @return Returns the pin that this object will be hooked up as an int
    def getPin(self):
        return self.dht_pin_number

class ThermalSensorGUI():
    def __init__(self):
        self.probe_label = QLabel('Thermal Probe Sensor: ')
        self.probe_interval = 1
        self.probe_pin_number = 2
        
        self.probeintervalbox = QComboBox()
        self.probeintervalbox.addItem("1")
        self.probeintervalbox.addItem("2")
        self.probeintervalbox.addItem("3")
        self.probeintervalbox.addItem("4")
        self.probeintervalbox.setProperty('Test', True)
        self.probeintervalbox.activated[str].connect(self.onProbeIntervalChange)
        
        self.probe_pin_box = QComboBox()
        self.probe_pin_box.addItem("2")
        self.probe_pin_box.addItem("3")
        self.probe_pin_box.addItem("14")
        self.probe_pin_box.addItem("15")
        self.probe_pin_box.addItem("18")
        self.probe_pin_box.setProperty('Test', True)
        self.probe_pin_box.activated[str].connect(self.onProbePinChange)
    
    ## @brief Changes interval to what is specified in the dropdown
    def onProbeIntervalChange(self, text):
        self.probe_interval = int(text)
    
    ## @brief Changes pin to what is specified in the dropdown
    def onProbePinChange(self, text):
        self.probe_pin_number = int(text)
    
    ## @brief Gets the interval of this object
    #  @return Returns the interval as an int in seconds
    def getInterval(self):
        return self.probe_interval
    
    ## @brief Gets the pin for this object
    #  @return Returns the pin that this object will be hooked up as an int
    def getPin(self):
        return self.probe_pin_number
    
class RPMSensorGUI():
    def __init__(self):
        self.rpm_label = QLabel('RPM Sensor: ')
        self.rpm_interval = 1
        self.rpm_pin_number = 2
        
        self.rpmintervalbox = QComboBox()
        self.rpmintervalbox.addItem("1")
        self.rpmintervalbox.addItem("2")
        self.rpmintervalbox.addItem("3")
        self.rpmintervalbox.addItem("4")
        self.rpmintervalbox.setProperty('Test', True)
        self.rpmintervalbox.activated[str].connect(self.onRPMIntervalChange)
        
        self.rpm_pin_box = QComboBox()
        self.rpm_pin_box.addItem("2")
        self.rpm_pin_box.addItem("3")
        self.rpm_pin_box.addItem("14")
        self.rpm_pin_box.addItem("15")
        self.rpm_pin_box.addItem("18")
        self.rpm_pin_box.setProperty('Test', True)
        self.rpm_pin_box.activated[str].connect(self.onRPMPinChange)
    
    ## @brief Changes interval to what is specified in the dropdown
    def onRPMIntervalChange(self, text):
        self.rpm_interval = int(text)
    
    ## @brief Changes pin to what is specified in the dropdown
    def onRPMPinChange(self, text):
        self.rpm_pin_number = int(text)
    
    ## @brief Gets the interval of this object
    #  @return Returns the interval as an int in seconds
    def getInterval(self):
        return self.rpm_interval

    ## @brief Gets the pin for this object
    #  @return Returns the pin that this object will be hooked up as an int
    def getPin(self):
        return self.rpm_pin_number
    
class CurrentSensorGUI():
    def __init__(self):
        self.current_label = QLabel('Current Sensor: ')
        self.current_interval = 1
        self.current_pin_number = 2
        
        self.currentintervalbox = QComboBox()
        self.currentintervalbox.addItem("1")
        self.currentintervalbox.addItem("2")
        self.currentintervalbox.addItem("3")
        self.currentintervalbox.addItem("4")
        self.currentintervalbox.setProperty('Test', True)
        self.currentintervalbox.activated[str].connect(self.onCurrentIntervalChange)
        
        self.current_pin_box = QComboBox()
        self.current_pin_box.addItem("2")
        self.current_pin_box.addItem("3")
        self.current_pin_box.addItem("14")
        self.current_pin_box.addItem("15")
        self.current_pin_box.addItem("18")
        self.current_pin_box.setProperty('Test', True)
        self.current_pin_box.activated[str].connect(self.onCurrentPinChange)
    
    ## @brief Changes interval to what is specified in the dropdown
    def onCurrentIntervalChange(self, text):
        self.current_interval = int(text)
    
    ## @brief Changes pin to what is specified in the dropdown
    def onCurrentPinChange(self, text):
        self.current_pin_number = int(text)
    
    ## @brief Gets the interval of this object
    #  @return Returns the interval as an int in seconds
    def getInterval(self):
        return self.current_interval

    ## @brief Gets the pin for this object
    #  @return Returns the pin that this object will be hooked up as an int
    def getPin(self):
        return self.current_pin_number

class PressureSensorGUI():
    def __init__(self):
        self.pressure_label = QLabel('Pressure Sensor: ')
        self.pressure_interval = 1
        self.pressure_pin_number = 2
        
        self.pressureintervalbox = QComboBox()
        self.pressureintervalbox.addItem("1")
        self.pressureintervalbox.addItem("2")
        self.pressureintervalbox.addItem("3")
        self.pressureintervalbox.addItem("4")
        self.pressureintervalbox.setProperty('Test', True)
        self.pressureintervalbox.activated[str].connect(self.onPressureIntervalChange)
        
        self.pressure_pin_box = QComboBox()
        self.pressure_pin_box.addItem("2")
        self.pressure_pin_box.addItem("3")
        self.pressure_pin_box.addItem("14")
        self.pressure_pin_box.addItem("15")
        self.pressure_pin_box.addItem("18")
        self.pressure_pin_box.setProperty('Test', True)
        self.pressure_pin_box.activated[str].connect(self.onPressurePinChange)
    
    ## @brief Changes interval to what is specified in the dropdown
    def onPressureIntervalChange(self, text):
        self.pressure_interval = int(text)
    
    ## @brief Changes pin to what is specified in the dropdown
    def onPressurePinChange(self, text):
        self.pressure_pin_number = int(text)
    
    ## @brief Gets the interval of this object
    #  @return Returns the interval as an int in seconds
    def getInterval(self):
        return self.pressure_interval

    ## @brief Gets the pin for this object
    #  @return Returns the pin that this object will be hooked up as an int
    def getPin(self):
        return self.pressure_pin_number

class FlowSensorGUI():
    def __init__(self):
        self.flow_label = QLabel('Flow Sensor: ')
        self.flow_interval = 1
        self.flow_pin_number = 2
        
        self.flowintervalbox = QComboBox()
        self.flowintervalbox.addItem("1")
        self.flowintervalbox.addItem("2")
        self.flowintervalbox.addItem("3")
        self.flowintervalbox.addItem("4")
        self.flowintervalbox.setProperty('Test', True)
        self.flowintervalbox.activated[str].connect(self.onFlowIntervalChange)
        
        self.flow_pin_box = QComboBox()
        self.flow_pin_box.addItem("2")
        self.flow_pin_box.addItem("3")
        self.flow_pin_box.addItem("14")
        self.flow_pin_box.addItem("15")
        self.flow_pin_box.addItem("18")
        self.flow_pin_box.setProperty('Test', True)
        self.flow_pin_box.activated[str].connect(self.onFlowPinChange)
    
    ## @brief Changes interval to what is specified in the dropdown
    def onFlowIntervalChange(self, text):
        self.flow_interval = int(text)
    
    ## @brief Changes pin to what is specified in the dropdown
    def onFlowPinChange(self, text):
        self.flow_pin_number = int(text)
    
    ## @brief Gets the interval of this object
    #  @return Returns the interval as an int in seconds
    def getInterval(self):
        return self.flow_interval

    ## @brief Gets the pin for this object
    #  @return Returns the pin that this object will be hooked up as an int
    def getPin(self):
        return self.flow_pin_number

if __name__ == '__main__':
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    screenSize = screen.size()
    
    gui = UpdateGui(screenSize.width()/2, screenSize.height()/2)
    #sys.exit(app.exec_())
    app.exec_()