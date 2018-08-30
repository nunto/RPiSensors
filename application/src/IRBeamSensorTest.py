import time
import RPi.GPIO as GPIO
import datetime as dt

#current_time = float(time.mktime(dt.datetime.now().timetuple()))
GPIO.setmode(GPIO.BCM)
GPIO.setup(18 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.add_event_detect(18, GPIO.BOTH, callback=sensorCallback, bouncetime=200)
current_time = dt.datetime.now()
while True:
    if not GPIO.input(18):
        time.sleep(1.0)
        print("Beam is broken")
        c = dt.datetime.now() - current_time 
        current_time = dt.datetime.now()
        milliseconds = (c.days * 24 * 60 * 60 + c.seconds) * 1000 + c.microseconds / 1000.0 - 1000
        print(current_time)
        print(milliseconds)
        rpm = (1000/milliseconds)*60
        print(rpm)
