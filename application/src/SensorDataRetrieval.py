import RPi.GPIO as GPIO
import DHT11
from w1thermsensor import W1ThermSensor
import datetime as dt

# @brief Reads data from the different sensors
class SensorDataRetrieval:
    def __init__(self, dht_pin: int, thermal_pin:int, rpm_pin:int, current_pin:int, pressure_pin:int, flow_pin:int):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup
        self.rpm_pin = rpm_pin
        self.dht_sensor = DHT11.DHT11(pin=dht_pin)
        self.thermal_sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20)
        #need to add the overwriting of temperature probe in file
    
    ## @brief Gets the data from a dht sensor
    #  @param dht_sensor A specific instance of a DHT Sensor from which data will be acquired
    #  @return An array, [Temp, Humidity]
    @classmethod
    def dht_reading(cls, dht_sensor) -> list:
        dht_data = dht_sensor.read()
        if (dht_data.is_valid()):
            dht_array = [dht_data.temperature, dht_data.humidity]
            return dht_array
        else:
            if (dht_data.error_code == 1):
                print("Error %d: Data missing" % dht_data.error_code)
            elif (dht_data.error_code == 2):
                print("Error %d: CRC" % dht_data.error_code)

    ## @brief Gets the data from the thermal temperature sensor
    #  @param thermal_sensor A specific instance of a Thermal Sensor from which data will be acquired
    #  @return Temperature in degrees celsius
    @classmethod
    def thermal_probe_reading(cls, thermal_sensor) -> float:
        temp_cel = thermal_sensor.get_temperature(W1ThermSensor.DEGREES_C)
        return temp_cel
    
    ## @brief Gets the data from the infrared sensor 
    #  @param rpm_pin The pin from which the IR sensor is sending data
    #  @return Revolutions per minute based on how often the beam breaks
    @classmethod
    def infrared_rpm_reading(cls, rpm_pin) -> float:
        GPIO.setup(rpm_pin , GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #if the sensor is sending a signal(not broken)
        if(GPIO.input(rpm_pin)):
            #wait until the sensor is not sending a signal(beam is broken)
            while GPIO.input(rpm_pin):
                pass
            current_time = dt.datetime.now()
            while not GPIO.input(rpm_pin):
                pass
            #wait until the beam is broken again(by passing while it is not broken)
            while GPIO.input(rpm_pin):
                pass
            difference = dt.datetime.now() - current_time
        else:
            #if the beam is broken, wait until is is broken again
            while not GPIO.input(rpm_pin):
                pass
            current_time = dt.datetime.now()
            while GPIO.input(rpm_pin):
                pass
            while not GPIO.input(rpm_pin):
                pass
            difference = dt.datetime.now() - current_time
        # be sure to ask about a difference in machines with holes and input field?
        milliseconds = (difference.days * 24 * 60 * 60 + difference.seconds) * 1000 + difference.microseconds / 1000.0
        rpm = (1000/milliseconds)*60
        print(rpm)
        return rpm
            
                
