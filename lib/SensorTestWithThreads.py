import RPi.GPIO as GPIO
import DHT11
import pyodbc
import datetime as dt
import time
import SensorPiGUI as gui
from threading import Thread, Semaphore
import threading
import sys
import socket
#import json
#import urllib2
#Connection variable initialized and lock set up
ConnectionLock= Semaphore(1)
is_connected = False

#Thread Classes setup 
class ConnectionCheckThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        connectiontest()

class SQLSendThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        OnlineDump()
        
class LocalDataDump (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        OfflineDump()

def connectiontest():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ConnectionLock.acquire()
    try:
        host_ip = socket.gethostbyname('www.google.com')
        is_connected = True
    except:
        is_connected = False
    ConnectionLock.release()


def ReadingData():
    # Setting up the Raspberry Pi
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

        

    # Setting up the Temp & Humidity sensor
    sensor = DHT11.DHT11(pin=14)
    #sets reading to be the sensor data
    reading = sensor.read()

#Online sending methods

def OnlineDump():
    #executing everything indefinitely in a loop
    while True:
        ConnectionLock.acquire()
        if(is_connected):
            timedsendOnline()
            ConnectionLock.release()
        else:
            ConnectionLock.release()

def timedsendOnline():
    global current_time
    #checks if the right number of seconds have passed based on the GUI 
    if(current_time + getDHTInterval() <= int(time.mktime(dt.datetime.now().timetuple()))):
        SQLsend()
        current_time = int(time.mktime(dt.datetime.now().timetuple()))

def SQLsend():
    
    #checks if there is data still in the reading
    if reading.is_valid():

        # SQL Server connection details
        dsn = 'sqlserverdatasource'
        db = 'SensorReadings'
        uid = 'root_sensor'
        pwd = 'Sensorread1'
        cnxn_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, uid, pwd, db)

        # Connecting SQL Server
        cnxn = pyodbc.connect(cnxn_string)
        cursor = cnxn.cursor()
        global current_time
        # Inserting the temp and humidity data into SQL
        dataInsert = "INSERT INTO TempHumidity(Timestamp, Temperature, Humidity) values (%d, %d, %d)" % (current_time, reading.temperature, reading.humidity)
        cursor.execute(dataInsert)
        cnxn.commit()

#Offline data sending methods

def OfflineDump():
    #executing everything indefinitely in a loop
    while True:
        ConnectionLock.acquire()
        if(not is_connected):
            timedsendOffline()
            ConnectionLock.release()
        else:
            ConnectionLock.release()

def timedsendOffline():
    global current_time
    #checks if the right number of seconds have passed based on the GUI 
    if(current_time + getDHTInterval() <= int(time.mktime(dt.datetime.now().timetuple()))):
        LocalFileSend()
        current_time = int(time.mktime(dt.datetime.now().timetuple()))

def LocalFileSend():
    if reading.is_valid():
        a= [current_time, reading.temperature, reading.temperature]
        with open('localdatadump.pickle', 'wb') as handle:
            pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
            

#methods to prpoerly retrieve values put into the GUI
DHTInterval = 0
def getDHTInterval():
    return float(graphic.DHTInterval)

def getCurrentInterval():
    return float(graphic.CurrentInterval)

def getRPMInterval():
    return float(graphic.RPMInterval)


#GUI Popup method called when program is started

def GUIPopup():
    
    graphic = gui.GraphicInterface()
    graphic.createwindow()
    #once the GUI submit button has been pressed
    while(not graphic.is_Ready):
        time.sleep(0.5)
        
    # Setting current time
    current_time = int(time.mktime(dt.datetime.now().timetuple()))

    
"""
else:
    if (reading.error_code == 1):
        print("Error %d: Data missing" % reading.error_code)
    elif (reading.error_code == 2):
        print("Error %d: CRC" % reading.error_code)
"""
GUIPopup()
ReadingData()

ConnectionThread = ConnectionCheckThread()
SQLSending = SQLSendThread()
LocalDataDumping = LocalDataDump()

ConnectionThread.start()
SQLSending.start()
LocalDataDumping.start()

ConnectionThread.join()
SQLSending.join()
LocalDataDumping.join()
