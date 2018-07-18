import time
from threading import Thread
from SensorDataRetrieval import SensorDataRetrieval
from DataStorage import DataStorage
from ConnectionHandler import ConnectionHandler
from UpdateGuiTestFile import UpdateGui
from ConfigGui import ConfigGui
from datetime import datetime
from PyQt5.QtWidgets import QApplication
import sys


def current_time() -> int:
    return int(time.mktime(datetime.now().timetuple()))

def dht_process(sensor, ds, status: bool):
    print('in dht_process')
    dht_data = SensorDataRetrieval.dht_reading(sensor)
    timestamp = current_time()
    temp = float(dht_data[0])
    hum = int(dht_data[1])

    if (status):
        ds.SQL_insert(connect_string, tablename, "'DHTSensor'", timestamp, temp, hum, 0.0, 0.0, 0.0, 0.0)
    else:
        ds.offline_save("'DHTSensor'", timestamp, temp, hum, 0.0, 0.0, 0.0, 0.0)


def thermal_process(sensor, ds, status:bool):
    print('in thermal process')
    thermal_data = SensorDataRetrieval.thermal_probe_reading(sensor)
    timestamp = current_time()
    
    if(status):
       ds.SQL_insert(connect_string, tablename, "'ThermalProbe'", timestamp, thermal_data, 0, 0.0, 0.0, 0.0, 0.0)
    else:
        ds.offline_save("'ThermalProbe'", timestamp, thermal_data, 0, 0.0, 0.0, 0.0, 0.0)

def rpm_process(pin, ds, status:bool):
    print('in rpm process')
    rpm_data = SensorDataRetrieval.infrared_rpm_reading(pin)
    timestamp = current_time()
    #need to change these methods to accept all the different return values of sensor data
    if(status):
        ds.SQL_insert(connect_string, tablename, "'RPM Sensor'", timestamp, 0.0, 0.0, rpm_data, 0.0, 0.0, 0.0)
    else:
        ds.offline_save("'RPM Sensor'", timestamp, 0.0, 0.0, rpm_data, 0.0, 0.0, 0.0)
        
if (__name__ == '__main__'):
        
    app2 = QApplication(sys.argv)

    screen = app2.primaryScreen()
    screenSize = screen.size()
    
    config_gui = ConfigGui(screenSize.width()/2, screenSize.height()/2)
    #sys.exit(app.exec_())
    app2.exec_()
    
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    screenSize = screen.size()
    
    update_gui = UpdateGui(screenSize.width()/2, screenSize.height()/2)
    #sys.exit(app.exec_())
    app.exec_()
    if(not update_gui.is_ready):
        sys.exit()

    sensor_list = update_gui.SensorObjectList
    
    
    
    connect_string = config_gui.cnxn_string
    tablename = config_gui.tablename 
    # Other intervals here---
    #---
    
    is_local_data = False
    dht_last_update = 0
    thermal_last_update = 0
    rpm_last_update = 0

    # Instantiating relevant sensor objects
    #sdr = SensorDataRetrieval(update_gui.getDHTPin(), update_gui.getProbePin(), update_gui.getRpmPin(), update_gui.getCurrentPin(), update_gui.getPressurePin(), update_gui.getFlowPin() )
    ds = DataStorage()
    ch = ConnectionHandler()

    # TODO: Add a check for each sensor time, only insert if it is time for them
    while (True):
        if (ch.is_connected()):
            if (is_local_data):
                ds.data_sync(connect_string, tablename)
                is_local_data = False
            for sensor in sensor_list:
                if(sensor.getType() == 0):
                    if (dht_last_update + sensor.getInterval() <= current_time()):
                        dht_last_update = current_time()
                        dht_thread = Thread(target = dht_process, args=(sensor.dht_sensor, ds, True))
                        dht_thread.start()
                elif(sensor.getType() == 1):   
                    if (thermal_last_update + sensor.getInterval() <= current_time()):
                        thermal_last_update = current_time()
                        thermal_thread = Thread(target = thermal_process, args=(sensor.thermal_sensor, ds, True))
                        thermal_thread.start()
                elif(sensor.getType() == 2):
                    if (rpm_last_update + sensor.getInterval() <= current_time()):
                        rpm_last_update = current_time()
                        rpm_thread = Thread(target = rpm_process, args=(sensor.getPin(), ds, True))
                        rpm_thread.start()

        else:
            print('not connected')
            # Save locally
            for sensor in sensor_list:
                if(sensor.getType() == 0):
                    if (dht_last_update + sensor.getInterval() <= current_time()):
                        dht_last_update = current_time()
                        dht_thread = Thread(target = dht_process, args=(sensor.dht_sensor, ds, False))
                        dht_thread.start()
                elif(sensor.getType() == 1):
                    if (thermal_last_update + sensor.getInterval() <= current_time()):
                        thermal_last_update = current_time()
                        thermal_thread = Thread(target = thermal_process, args=(sensor.thermal_sensor, ds, False))
                        thermal_thread.start()
                elif(sensor.getType() == 2):
                    if(rpm_last_update + sensor.getInterval() <= current_time()):
                        rpm_last_update = current_time()
                        rpm_thread = Thread(target = rpm_process, args=(sensor.getPin(), ds, False))
                        rpm_thread.start()
            
            if (not is_local_data):
                is_local_data = True
        
                
        dht_thread.join()
