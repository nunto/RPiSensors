from w1thermsensor import W1ThermSensor
import time

sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20)

while (True):
    temp_cel = sensor.get_temperature(W1ThermSensor.DEGREES_C)
    print (temp_cel)
    time.sleep(5)