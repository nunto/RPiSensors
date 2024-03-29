import time
from threading import Thread
import threading
from SensorDataRetrieval import SensorDataRetrieval
from DataStorage import DataStorage
from ConnectionHandler import ConnectionHandler
from SensorConfigGUI import UpdateGui
from LoginGUI import ConfigGui
from datetime import datetime
from PyQt5.QtWidgets import QApplication
import sys
import os
import pickle
import RPi.GPIO as GPIO

## @brief Returns the current time as an int for easy comparison of seconds passed
#  @return returns time as an int in sceonds from January 1 1970
def current_time() -> int:
    return int(time.mktime(datetime.now().timetuple()))


## @brief Gets data from a DHT sensor using the dht_reading method in SensorDataRetrieval, and either sends that to the sql database or locally saves it
#  @param sensor The current sensor that is being referred to in the list of all sensors
#  @param ds Data Storage Object from which the methods to save the data are taken
#  @param status Whether or not the pi is connected to the internet. True is connected, False is not connected
def dht_process(sensor, ds, status: bool):
    print('in dht_process')
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup
    dht_data = SensorDataRetrieval.dht_reading(sensor)
    timestamp = datetime.now()
    temp = float(dht_data[0])
    hum = int(dht_data[1])
    timestamp_offline = current_time()

    if (status):
        ds.SQL_insert(connect_string, tablename, "'DHT Sensor'", timestamp, temp, hum, 'NULL', 'NULL', 'NULL', 'NULL')
    else:
        print(1)
        ds.offline_save("'DHT Sensor'", timestamp_offline, temp, hum, 'NULL', 'NULL', 'NULL', 'NULL')
        print(2)

## @brief Gets data from a Thermal Probe sensor using the thermal_probe_reading method in SensorDataRetrieval, and either sends that to the sql database or locally saves it
#  @param sensor The current sensor that is being referred to in the list of all sensors
#  @param ds Data Storage Object from which the methods to save the data are taken
#  @param status Whether or not the pi is connected to the internet. True is connected, False is not connected
def thermal_process(sensor, ds, status:bool):
    print('in thermal process')
    thermal_data = SensorDataRetrieval.thermal_probe_reading(sensor)
    timestamp = datetime.now()
    timestamp_offline = current_time()
    
    if(status):
       ds.SQL_insert(connect_string, tablename, "'Thermal Probe'", timestamp, thermal_data, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL')
    else:
        ds.offline_save("'Thermal Probe'", timestamp_offline, thermal_data, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL')
        

## @brief Gets data from a RPM sensor using the infrared_rpm_reading method in SensorDataRetrieval, and either sends that to the sql database or locally saves it
#  @param pin Pin from which to read data
#  @param ds Data Storage Object from which the methods to save the data are taken
#  @param status Whether or not the pi is connected to the internet. True is connected, False is not connected
def rpm_process(pin, ds, status:bool, operation:int, factor:float):
    print('in rpm process')
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup
    rpm_data = SensorDataRetrieval.infrared_rpm_reading(pin, operation, factor)
    timestamp = datetime.now()
    timestamp_offline = current_time()
    
    if(status):
        ds.SQL_insert(connect_string, tablename, "'RPM Sensor'", timestamp, 'NULL', 'NULL', rpm_data, 'NULL', 'NULL', 'NULL')
    else:
        ds.offline_save("'RPM Sensor'", timestamp_offline, 'NULL', 'NULL', rpm_data, 'NULL', 'NULL', 'NULL')

## @brief Gets data from a Current sensor using the current_reading method in SensorDataRetrieval, and either sends that to the sql database or locally saves it
#  @param channel  Channel on the ADC chip from which to read the data from
#  @param ds Data Storage Object from which the methods to save the data are taken
#  @param status Whether or not the pi is connected to the internet. True is connected, False is not connected
def current_process(channel, ds, status:bool):
    print('in current process')
    current_data = SensorDataRetrieval.current_reading(channel)
    timestamp = datetime.now()
    timestamp_offline = current_time()
    
    if(status):
        ds.SQL_insert(connect_string, tablename, "'Current Sensor'", timestamp, 'NULL', 'NULL', 'NULL', current_data, 'NULL', 'NULL')
    else:
        ds.offline_save("'Current Sensor'", timestamp_offline, 'NULL', 'NULL', 'NULL', current_data, 'NULL', 'NULL')
        
## @brief Gets data from a flow sensor using the flow_reading method in SensorDataRetrieval, and either sends it to the sql database or saves it locally
#  @param channel Channel on the ADC chip from which the data is read
#  @param ds Data Storage Object from which the methods to save the data are taken
#  @param status Whether or not the pi is connected to the internet. True is connected, False is not connected
def flow_process(channel, ds, status:bool):
    print('in flow process')
    flow_data = SensorDataRetrieval.flow_reading(channel)
    timestamp = datetime.now()
    timestamp_offline = current_time()
    if(status):
        ds.SQL_insert(connect_string, tablename, "'Flow Sensor'", timestamp, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', flow_data)
    else:
        ds.offline_save("'Flow Sensor'", timestamp_offline, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', flow_data)
        


if (__name__ == '__main__'):
    #ntp time sync
    """
    os.system('sudo service ntp stop')
    os.system('sudo ntpd -gq')
    os.system('sudo service ntp start')
    """
    #preload the settings for the connection string if the login gui has been run before
    if(os.path.exists('configuration.pickle') and os.path.getsize('configuration.pickle') > 0):
            with open('configuration.pickle', 'rb') as handle:
                k = pickle.load(handle)
                connect_string = 'DSN=sqlserverdatasource;UID=%s;PWD=%s;DATABASE=%s;' % (k[1], k[2], k[0])
                print(connect_string)
                tablename = k[3]
            handle.close()
    else:
        #otherwise run the login gui
        app2 = QApplication(sys.argv)
        screen = app2.primaryScreen()
        screenSize = screen.size()
        
        #setting up the initial gui
        config_gui = ConfigGui(screenSize.width()/2, screenSize.height()/2)
        
        app2.exec_()
        #get the connection string and table the user inputted in config_gui
        connect_string = config_gui.cnxn_string
        tablename = config_gui.tablename 
        #if submit was not hit, close the program
        if(not config_gui.is_ready):
            sys.exit()
    #if there is a sensor configuration already, use what is saved in that file
    if(os.path.exists('sensorconfiguration.pickle') and os.path.getsize('sensorconfiguration.pickle') > 0):
        with open('sensorconfiguration.pickle', 'rb') as handle:
            b = pickle.load(handle)
        handle.close()
        
        sensor_list = b
    else:
        #otherwise start the sensor configuration gui
        app = QApplication(sys.argv)
        print('starting second gui')
        screen = app.primaryScreen()
        screenSize = screen.size()
        
        #creating the gui for all the settings
        update_gui = UpdateGui(screenSize.width()/2, screenSize.height()/2)
        
        app.exec_()
        
        
        #if submit has not been pressed
        if(not update_gui.is_ready):
            sys.exit()
        
        #creating list of all sensors that were created in update_gui
        sensor_list = update_gui.SensorObjectList
    
    
    is_local_data = False
    dht_last_update = 0
    thermal_last_update = 0
    rpm_last_update = 0
    current_last_update = 0
    flow_last_update = 0
    
    dht_thread = None
    thermal_thread = None
    rpm_thread = None
    current_thread = None
    
    # Instantiating relevant sensor objects
    #sdr = SensorDataRetrieval(update_gui.getDHTPin(), update_gui.getProbePin(), update_gui.getRpmPin(), update_gui.getCurrentPin(), update_gui.getPressurePin(), update_gui.getFlowPin() )
    ds = DataStorage()
    ch = ConnectionHandler()
    print('starting loop')
    
    while (True):
        if(datetime.now().hour == 0 and datetime.now().minute == 0):
            #if it is midnight, sync the time with ntp
            os.system('sudo service ntp stop')
            os.system('sudo ntpd -gq')
            os.system('sudo service ntp start')
        if (ch.is_connected()):
            if (is_local_data):
                #if there is local data, sync it, and set the variable to false
                ds.data_sync(connect_string, tablename)
                is_local_data = False
            #for every sensor that is created by the user
            for sensor in sensor_list:
                #if the sensor is of type 0, execute the DHT Process 
                if(sensor.getType() == 0):
                    #if the interval for recording data has passed
                    if (dht_last_update + sensor.getInterval() <= current_time()):
                        dht_last_update = current_time()
                        dht_thread = Thread(target = dht_process, args=(sensor.dht_sensor, ds, True))
                        dht_thread.start()
                #if the sensor is of type 1, execute the Thermal Probe Process
                elif(sensor.getType() == 1):   
                    #if the interval for recording data has passed
                    if (thermal_last_update + sensor.getInterval() <= current_time()):
                        thermal_last_update = current_time()
                        thermal_thread = Thread(target = thermal_process, args=(sensor.thermal_sensor, ds, True))
                        thermal_thread.start()
                #if the sensor is of type 2, execute the RPM Sensor Process
                elif(sensor.getType() == 2):
                    #if the interval for recording data has passed
                    if (rpm_last_update + sensor.getInterval() <= current_time()):
                        rpm_last_update = current_time()
                        rpm_thread = Thread(target = rpm_process, args=(sensor.getPin(), ds, True, sensor.getOperation(), sensor.getFactor()))
                        rpm_thread.start()
                #if the sensor is of type 3, execute the Current Sensor Process
                elif(sensor.getType() == 3):
                    #if the interval for recording data has passed
                    if (current_last_update + sensor.getInterval() <= current_time()):
                        current_last_update = current_time()
                        current_thread = Thread(target = current_process, args=(sensor.getPin(), ds, True))
                        current_thread.start()
                elif(sensor.getType() == 4):
                    #if the interval for recording data has passed
                    if(flow_last_update + sensor.getInterval() <= current_time()):
                        flow_last_update = current_time()
                        flow_thread = Thread(target = flow_process, arg=(sensor.getPin(), ds, True))
                        flow_thread.start()

        else:
            #print('not connected')
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
                        rpm_thread = Thread(target = rpm_process, args=(sensor.getPin(), ds, False, sensor.getOperation(), sensor.getFactor()))
                        rpm_thread.start()
                elif(sensor.getType() == 3):
                    if (current_last_update + sensor.getInterval() <= current_time()):
                        current_last_update = current_time()
                        current_thread = Thread(target = current_process, args=(sensor.getPin(), ds, False))
                        current_thread.start()
                elif(sensor.getType() == 4):
                    #if the interval for recording data has passed
                    if(flow_last_update + sensor.getInterval() <= current_time()):
                        flow_last_update = current_time()
                        flow_thread = Thread(target = flow_process, arg=(sensor.getPin(), ds, False))
                        flow_thread.start()
                        
            if (not is_local_data):
                is_local_data = True
        #if a dht thread was created, join that thread, likewise with the other sensor types
        if(hasattr(dht_thread, 'isAlive')):
            dht_thread.join()
        elif(hasattr(thermal_thread, 'isAlive')):
            thermal_thread.join()
        elif(hasattr(rpm_thread, 'isAlive')):
            rpm_thread.join()
        elif(hasattr(current_thread, 'isAlive')):
            current_thread.join()
        elif(hasattr(flow_thread, 'isAlive')):
            flow_thread.join()
