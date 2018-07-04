import RPi.GPIO as GPIO
import DHT11
import pyodbc
import datetime as dt
import time
import SensorPiGUI as g
#import json
#import urllib2

def SQLsend():
	# Inserting the temp and humidity data into SQL
    dataInsert = "INSERT INTO TempHumidity(Temperature, Humidity) values (%d, %d)" % (reading.temperature, reading.humidity)
    cursor.execute(dataInsert)
    cnxn.commit()

def timedsend():
    global current_time
    if(current_time + 5 <= int(time.mktime(dt.datetime.now().timetuple()))):
        SQLsend()
        current_time = int(time.mktime(dt.datetime.now().timetuple()))
	
# Setting up the Raspberry Pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Setting up the Temp & Humidity sensor
sensor = DHT11.DHT11(pin=14)

# Reads the current sensor data
reading = sensor.read()

# Setting current time
current_time = int(time.mktime(dt.datetime.now().timetuple()))

graphic = g.GraphicInterface()
graphic.createwindow()
while(graphic.is_Ready == False):
    sleep(0.5)




if reading.is_valid():
    print("Temp: %d C" % reading.temperature)
    print("Humidity: %d %%" % reading.humidity)
    print("Sending to SQL")

    # SQL Server connection details
    dsn = 'sqlserverdatasource'
    db = 'SensorReadings'
    uid = 'root_sensor'
    pwd = 'Sensorread1'
    cnxn_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, uid, pwd, db)

    # Connecting SQL Server
    cnxn = pyodbc.connect(cnxn_string)
    cursor = cnxn.cursor()

while True:
    timedsend()
    if 0xFF == ord('q'):
            break

#TODO: Implement proper method for retrieving data every x seconds

else:
    if (reading.error_code == 1):
        print("Error %d: Data missing" % reading.error_code)
    #else if (reading.error_code == 2):
     #   print("Error %d: CRC" % reading.error_code)