import RPi.GPIO as GPIO
import DHT11
import pyodbc
import datetime as dt
import time
import UpdateGui as graphic
from threading import Thread, Semaphore
import threading
import sys
import socket
import pickle
import os

#import json
#import urllib2

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
    global is_connected
    while 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            host_ip = socket.gethostbyname('www.google.com')
            if(not is_connected):
                ConnectionLock.acquire()
                is_connected = True
                ConnectionLock.release()
        except:
            if(is_connected):
                ConnectionLock.acquire()
                is_connected = False
                ConnectionLock.release()


def syncfromlocal():
    global objects
    global DumpingFile
    global cnxn_string
    ConnectionLock.acquire()
    if(is_connected and (os.stat("localdatadump.pickle").st_size==0)):
        ConnectionLock.release()
        DumpingFile.close()
        
        with open('localdatadump.pickle', 'rb') as DumpingFile:
            while True:
                try:
                    objects.append(pickle.load(DumpingFile))
                except EOFError:
                    break
        print("reloading offline data")


        # Connecting SQL Server
        cnxn = pyodbc.connect(cnxn_string)
        cursor = cnxn.cursor()
        global current_time
        
        # Inserting the temp and humidity data into SQL
                   
        for i in range(len(objects)):
            dataInsert = "INSERT INTO TempHumidity(Timestamp, Temperature, Humidity) values (%d, %d, %d)" % (objects[i][0], objects[i][1], objects[i][2])
            cursor.execute(dataInsert)
            cnxn.commit()
    else:
        ConnectionLock.release()

#Online sending methods

def OnlineDump():
    #executing everything indefinitely in a loop
    global is_connected
    while 1:
        ConnectionLock.acquire()
        if(is_connected):
            ConnectionLock.release()
            timedsendOnline()
            syncfromlocal()

        else:
            ConnectionLock.release()

def timedsendOnline():
    global current_time
    #checks if the right number of seconds have passed based on the GUI 
    if(current_time + getDHTInterval() <= int(time.mktime(dt.datetime.now().timetuple()))):
        SQLsend()
        current_time = int(time.mktime(dt.datetime.now().timetuple()))

def SQLsend():
    #sets reading to be the sensor data
    global cnxn_string
    readingSQL = sensor.read()
    #checks if there is data still in the reading
    if readingSQL.is_valid():
        print("sending online data")

        # Connecting SQL Server
        cnxn = pyodbc.connect(cnxn_string)
        cursor = cnxn.cursor()
        global current_time
        # Inserting the temp and humidity data into SQL
        dataInsert = "INSERT INTO TempHumidity(Timestamp, Temperature, Humidity) values (%d, %d, %d)" % (current_time, readingSQL.temperature, readingSQL.humidity)
        cursor.execute(dataInsert)
        cnxn.commit()

#Offline data sending methods

def OfflineDump():
    #executing everything indefinitely in a loop
    global is_connected
    while 1:
        ConnectionLock.acquire()
        if(not is_connected):
            ConnectionLock.release()            
            timedsendOffline()
            
        else:
            ConnectionLock.release()

def timedsendOffline():
    global current_time
    #checks if the right number of seconds have passed based on the GUI 
    if(current_time + getDHTInterval() <= int(time.mktime(dt.datetime.now().timetuple()))):
        LocalFileSend()
        current_time = int(time.mktime(dt.datetime.now().timetuple()))

def LocalFileSend():
    global DumpingFile
    global is_connected
    readinglocal = sensor.read()
    if readinglocal.is_valid():
        print("sending local data")
        a= [current_time, readinglocal.temperature, readinglocal.humidity]
        print(current_time)
        pickle.dump(a, DumpingFile, protocol=pickle.HIGHEST_PROTOCOL)
        
#methods to prpoerly retrieve values put into the GUI

def getDHTInterval():
    return float(gui.dht_interval)

def getThermalInterval():
    return float(gui.probe_interval)

def getCurrentInterval():
    return float(gui.current_interval)


        
"""
else:
    if (reading.error_code == 1):
        print("Error %d: Data missing" % reading.error_code)
    elif (reading.error_code == 2):
        print("Error %d: CRC" % reading.error_code)
"""

#Connection variable initialized and lock set up

# SQL Server connection details
dsn = 'sqlserverdatasource'
db = 'SensorReadings'
uid = 'root_sensor'
pwd = 'Sensorread1'
cnxn_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, uid, pwd, db)

ConnectionLock= Semaphore(1)
is_connected = False

DumpingFile = open('localdatadump.pickle', 'wb')

# Setting current time
current_time = int(time.mktime(dt.datetime.now().timetuple()))

objects =[]

graphic = gui.GraphicInterface()
graphic.createwindow()
#once the GUI submit button has been pressed
while(not graphic.is_Ready):
    time.sleep(0.5)

# Setting up the Raspberry Pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

    

# Setting up the Temp & Humidity sensor
sensor = DHT11.DHT11(pin=14)



ConnectionThread = ConnectionCheckThread()
SQLSending = SQLSendThread()
LocalDataDumping = LocalDataDump()

ConnectionThread.start()
SQLSending.start()
LocalDataDumping.start()

ConnectionThread.join()
LocalDataDumping.join()
SQLSending.join()

