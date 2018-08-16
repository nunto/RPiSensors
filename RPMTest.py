import RPi.GPIO as GPIO
import datetime as dt
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup
GPIO.setup(3 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
#if the sensor is sending a signal(not broken)
while True:
    if(GPIO.input(3)):
        #wait until the sensor is not sending a signal(beam is broken)
        while GPIO.input(3):
            pass
        current_time = dt.datetime.now()
        while not GPIO.input(3):
            pass
        #wait until the beam is broken again(by passing while it is not broken)
        while GPIO.input(3):
            pass
        difference = dt.datetime.now() - current_time
    else:
        #if the beam is broken, wait until is is broken again
        while not GPIO.input(3):
            pass
        current_time = dt.datetime.now()
        while GPIO.input(3):
            pass
        while not GPIO.input(3):
            pass
        difference = dt.datetime.now() - current_time
    # be sure to ask about a difference in machines with holes and input field?
    milliseconds = (difference.days * 24 * 60 * 60 + difference.seconds) * 1000 + difference.microseconds / 1000.0
    rpm = (1000/milliseconds)*60
    print(rpm/3.2)
    sleep(1)