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
    
    ## @brief Return the type of sensor of that particular instance of the Sensor object
    #  @return Returns the sensor type as an integer where 0 is DHT, 1 is Thermal Probe, 3 is Current, 4 is Pressure, 5 is Flow
    def getType(self):
        return self.sensor_type
    ## @brief Returns the interval set by the user for that specific instance of a sensor
    #  @return Returns the interval at which readings are recorded in seconds
    def getInterval(self):
        return self.interval
    
    ## @brief Return the pin as set by the user from which that Sensor object is receiving data
    #  @return Returns the pin as an integer based on the GPIO pin numbering
    def getPin(self):
        return self.pin