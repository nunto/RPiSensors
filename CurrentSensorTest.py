import Adafruit_MCP3008
import math
from time import sleep
import RPi.GPIO as GPIO


CLK = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

print(mcp.read_adc(0))


def calcIrms(channel):
    NUMBER_OF_SAMPLES = 1480
    SUPPLYVOLTAGE = 3300
    ICAL = 111.1
    max_read = 0
    min_read = 1024
    for n in range (0, NUMBER_OF_SAMPLES):
        current_reading = mcp.read_adc(0)
        #print(current_reading)
        if current_reading < min_read:
            min_read = current_reading
        if current_reading > max_read:
            max_read = current_reading
            
    total_amp = max_read - min_read
    
    current_amp = total_amp/2
    
    IRMS = current_amp*30/1024
    print(1.25*IRMS)
    sleep(1)
#def current_process(sensor, ds, status:bool):
while True:
    #ADC_BITS = 10
    #ADC_COUNTS = ADC_BITS<<1
    print(mcp.read_adc(0))
    calcIrms(0)
    sleep(1)
    """
    NUMBER_OF_SAMPLES = 1480
    SUPPLYVOLTAGE = 3300
    ICAL = 111.1
    max_read = 0
    min_read = 1024
    for n in range (0, NUMBER_OF_SAMPLES):
        current_reading = mcp.read_adc(7)
        if current_reading < min_read:
            min_read = current_reading
        if current_reading > max_read:
            max_read = current_reading
            
    total_amp = max_read - min_read
    
    current_amp = total_amp/2
    
    IRMS = current_amp*30/1024
    print(18.5*IRMS)
    sleep(1)
    """
"""
  NUMBER_OF_SAMPLES = 1000
    SUPPLYVOLTAGE = 3300
    ICAL = 111.1
    sumI = 0
    sampleI = 512
    filteredI = 0
    for n in range (0, NUMBER_OF_SAMPLES):
        lastSampleI = sampleI
        sampleI = (mcp.read_adc(channel))
        #print sampleI
        lastFilteredI = filteredI
        filteredI = 0.996*(lastFilteredI+sampleI-lastSampleI)
        sqI = filteredI * filteredI
        sumI += sqI
       
    I_RATIO = ICAL * ((SUPPLYVOLTAGE/1000.0) / 1023.0)
    Irms = I_RATIO * math.sqrt(sumI / NUMBER_OF_SAMPLES)
    sumI = 0
    print(Irms)
"""

