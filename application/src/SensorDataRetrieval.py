import RPi.GPIO as GPIO
import DHT11
from w1thermsensor import W1ThermSensor
import datetime as dt
import Adafruit_MCP3008

# @brief Reads data from the different sensors
class SensorDataRetrieval:
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
    #  @param operation The operation chosen by the user for the rpm to be corrected 0 is multiply, 1 is divide
    #  @param factor The factor of correction as entered by the user
    #  @return Revolutions per minute based on how often the beam breaks
    @classmethod
    def infrared_rpm_reading(cls, rpm_pin, operation, factor) -> float:
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
        if(operation == 0):
            new_rpm = rpm*factor
        elif(operation == 1):
            new_rpm = rpm/factor
        return new_rpm
    
    ## @brief calculates the current based on a current sesnor going through an ADC chip
    #  @param current_channel The channel on the ADC chip to which the sensor is sending data. Between 0-7
    #  @return Current measured in amps between +- 0.9 Amps
    @classmethod
    def current_reading(cls, current_channel) -> float:
        CLK = 18
        MISO = 23
        MOSI = 24
        CS   = 25
        mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
        number_of_samples = 1480
        supply_voltage = 3300
        calibration = 1.25
        max_read = 0
        min_read = 1024
        for n in range (0, number_of_samples):
            current_reading = mcp.read_adc(current_channel)
            #print(current_reading)
            if current_reading < min_read:
                min_read = current_reading
            if current_reading > max_read:
                max_read = current_reading
                
        total_difference = max_read - min_read
        
        half_difference = total_difference/2
        
        raw_amps = half_difference*30/1024
        real_amps = calibration*raw_amps
        return real_amps
    
    
    ## @brief calculates the flow of air based on a flow sesnor going through an ADC chip
    #  @param flow_channel The channel on the ADC chip to which the sensor is sending data. Between 0-7
    #  @return Flow measured in cfm
    @classmethod
    def flow_reading(cls, flow_channel):
        CLK = 18
        MISO = 23
        MOSI = 24
        CS   = 25
        mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
        sum = 0
        number_of_samples = 1480
        for n in range (0, number_of_samples):
            flow_reading = mcp.read_adc(flow_channel)
            sum += flow_reading
        average_flow = sum/number_of_samples
        return average_flow
            
