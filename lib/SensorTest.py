import RPi.GPIO as GPIO
import DHT11
import pyodbc
import datetime as dt
import time
import SensorPiGUI as gui
#import json
#import urllib2


#methods to prpoerly retrieve values put into the GUI
DHTInterval = 0
def getDHTInterval():
    return float(graphic.DHTInterval)

def getCurrentInterval():
    return float(graphic.CurrentInterval)

def getRPMInterval():
    return float(graphic.RPMInterval)

def SQLsend():
    reading = sensor.read()
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
    
def timedsend():
    global current_time
    #checks if the right number of seconds have passed based on the GUI 
    if(current_time + getDHTInterval() <= int(time.mktime(dt.datetime.now().timetuple()))):
        SQLsend()
        current_time = int(time.mktime(dt.datetime.now().timetuple()))
	
# Setting up the Raspberry Pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

    

# Setting up the Temp & Humidity sensor
sensor = DHT11.DHT11(pin=14)

# Reads the current sensor data


graphic = gui.GraphicInterface()
graphic.createwindow()
#once the GUI submit button has been pressed
while(not graphic.is_Ready):
    time.sleep(0.5)
    
# Setting current time
current_time = int(time.mktime(dt.datetime.now().timetuple()))


#executing everything indefinitely in a loop
while True:
    timedsend()

else:
        if (reading.error_code == 1):
            print("Error %d: Data missing" % reading.error_code)
        elif (reading.error_code == 2):
            print("Error %d: CRC" % reading.error_code)


