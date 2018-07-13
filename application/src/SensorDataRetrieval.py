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
        #add in other sensor objects where the pin is the one passed to the method
        #need to add the overwriting of temperature probe in file
    ## @brief Gets the data from the dht sensor
    #  @return An array, [Temp, Humidity]
    def dht_reading(self) -> list:
        dht_data = self.dht_sensor.read()
        if (dht_data.is_valid()):
            dht_array = [dht_data.temperature, dht_data.humidity]
            return dht_array
        else:
            if (dht_data.error_code == 1):
                print("Error %d: Data missing" % dht_data.error_code)
            elif (dht_data.error_code == 2):
                print("Error %d: CRC" % dht_data.error_code)

    ## @brief Gets the data from the thermal temperature sensor
    #  @return Temperature in degrees celsius
    def thermal_probe_reading(self) -> float:
        temp_cel = self.thermal_sensor.get_temperature(W1ThermSensor.DEGREES_C)
        return temp_cel
    
    ## @brief Gets the data from the infrared sensor 
    # @return Revolutions per minute based on how often the beam breaks
    def infrared_rpm_reading(self) -> float:
        current_time = dt.datetime.now()
        GPIO.setup(self.rpm_pin , GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #change this to be the pin on which the sensor is on from the GUI
        while GPIO.input(self.rpm_pin):
            pass
        difference = dt.datetime.now() - current_time
        current_time = dt.datetime.now()
        # be sure to ask about a difference in machines with holes and input field?
        milliseconds = (difference.days * 24 * 60 * 60 + difference.seconds) * 1000 + difference.microseconds / 1000.0
        rpm = (1000/milliseconds)*60
        return rpm
            
                
