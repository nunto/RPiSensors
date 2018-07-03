import RPi.GPIO as GPIO
import DHT11
#import json
#import urllib2
import pyodbc

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

sensor = DHT11.DHT11(pin=14)
reading = sensor.read()

if reading.is_valid():
    print("Temp: %d C" % reading.temperature)
    print("Humidity: %d %%" % reading.humidity)
    print("Sending to SQL")

    #data = {
    #    'temp' : reading.temperature,
    #    'humidity' : reading.humidity
    #}

    #request = urllib2.Request("172.18.19.130/submit_data.php")
    #request.add_header('Content-Type', 'application/json')

    #response = urllib2.urlopen(request, json.dumps(data))

    dsn = 'sqlserverdatasource'
    db = 'SensorReadings'
    uid = 'root_sensor'
    pwd = 'Sensorread1'

    cnxn_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;' % (dsn, uid, pwd, db)
    cnxn = pyodbc.connect(cnxn_string)
    cursor = cnxn.cursor()

    dataInsert = "INSERT INTO TempHumidity(Temperature, Humidity) values (%d, %d)" % (reading.temperature, reading.humidity)
    cursor.execute(dataInsert)
    cnxn.commit()


else:
    print("Error: %d" % reading.error_code)