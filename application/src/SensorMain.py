import time
from threading import Thread
from SensorDataRetrieval import SensorDataRetrieval
from DataStorage import DataStorage
from ConnectionHandler import ConnectionHandler
from UpdateGui import UpdateGui
from ConfigGui import ConfigGui
from datetime import datetime
from PyQt5.QtWidgets import QApplication
import sys


def current_time() -> int:
    return int(time.mktime(datetime.now().timetuple()))

def dht_process(sdr, ds, status: bool):
    print('in dht_process')
    dht_data = sdr.dht_reading()
    timestamp = current_time()
    temp = int(dht_data[0])
    hum = int(dht_data[1])

    if (status):
        ds.SQL_insert(timestamp, temp, hum)
    else:
        ds.offline_save(timestamp, temp, hum)


def thermal_process(sdr, ds, status:bool):
    print('in thermal process')
    thermal_data = sdr.thermal_probe_reading()
    timestamp = current_time()
    if(status):
       ds.SQL_insert()
    else:
        ds.offline_save()

def rpm_process(sdr, ds, status:bool):
    print('in rpm process')
    rpm_data = sdr.infrared_rpm_reading()
    timestamp = current_time()
    #need to change these methods to accept all the different return values of sensor data
    if(status):
        ds.SQL_insert()
    else:
        ds.offline_save()
        
if (__name__ == '__main__'):
        
    app2 = QApplication(sys.argv)

    screen = app2.primaryScreen()
    screenSize = screen.size()
    
    gui = ConfigGui(screenSize.width()/2, screenSize.height()/2)
    #sys.exit(app.exec_())
    app2.exec_()
    
    app = QApplication(sys.argv)

    screen = app.primaryScreen()
    screenSize = screen.size()
    
    gui = UpdateGui(screenSize.width()/2, screenSize.height()/2)
    #sys.exit(app.exec_())
    app.exec_()

    dht_interval = gui.getDHTInterval() # Get this from GUI later
    thermal_interval = gui.getProbeInterval()
    current_interval = gui.getCurrentInterval()
    rpm_interval = gui.getRpmInterval()
    pressure_interval = gui.getPressureInterval()
    flow_interval = gui.getFlowInterval()
    
    # Other intervals here---
    #---
    
    is_local_data = False
    dht_last_update = 0
    thermal_last_update = 0
    rpm_last_update = 0

    # Instantiating relevant sensor objects
    sdr = SensorDataRetrieval(gui.getDHTPin(), gui.getProbePin(), gui.getRpmPin(), gui.getCurrentPin(), gui.getPressurePin(), gui.getFlowPin() )
    ds = DataStorage()
    ch = ConnectionHandler()

    # TODO: Add a check for each sensor time, only insert if it is time for them
    while (True):
        if (ch.is_connected()):
            print('connected')
            if (is_local_data):
                ds.data_sync()
                is_local_data = False

            if (dht_last_update + dht_interval <= current_time()):
                dht_last_update = current_time()
                dht_thread = Thread(target = dht_process, args=(sdr, ds, True))
                dht_thread.start()
            
            if (thermal_last_update + thermal_interval <= current_time()):
                thermal_last_update = current_time()
                thermal_thread = Thread(target = thermal_process, args=(sdr, ds, True))
                thermal_thread.start()
            
            if (rpm_last_update + rpm_interval <= current_time()):
                rpm_last_update = current_time()
                rpm_thread = Thread(target = rpm_process, args=(sdr, ds, True))
                rpm_thread.start()

        else:
            print('not connected')
            # Save locally
            if (dht_last_update + dht_interval <= current_time()):
                dht_last_update = current_time()
                dht_thread = Thread(target = dht_process, args=(sdr, ds, False))
                dht_thread.start()
            
            if (thermal_last_update + thermal_interval <= current_time()):
                thermal_last_update = current_time()
                thermal_thread = Thread(target = thermal_process, args=(sdr, ds, False))
                thermal_thread.start()
            
            if (rpm_last_update + rpm_interval <= current_time()):
                rpm_last_update = current_time()
                rpm_thread = Thread(target = rpm_process, args=(sdr, ds, False))
                rpm_thread.start()
            
            if (not is_local_data):
                is_local_data = True
        
                
        dht_thread.join()
        thermal_thread.join()
        rpm_thread.join()