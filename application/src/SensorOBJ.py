import DHT11
from w1thermsensor import W1ThermSensor
class SensorOBJ():
    def __init__(self, type: int, interval:int, pin:int):
        self.sensor_type = type
        self.interval = interval
        self.pin = pin
        self.dht_sensor = None
        self.thermal_sensor = None
        self.rpm_sensor = None
        self.current_sensor = None
        self.pressure_sensor = None
        self.flow_sensor = None
        if(self.sensor_type == 0):
            self.dht_sensor = DHT11.DHT11(pin = self.pin)
        if(self.sensor_type == 1):
            self.thermal_sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20)
        #add more sensor initializations when they come in 
        #if(sensor_type == 3):
    def getType(self):
        return self.sensor_type
    def getInterval(self):
        return self.interval
    def getPin(self):
        return self.pin