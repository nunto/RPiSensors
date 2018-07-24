import Adafruit_MCP3008
import math

CLK = 15
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
#print(mcp.read_adc(0))

#def current_process
ADC_BITS = 10
ADC_COUNTS = ADC_BITS<<1
samples = 1480 #value to be added
offsetI = ADC_COUNTS>>1
SupplyVoltage=5000
sumI = 0
for i in range(samples):
    sampleI = mcp.read_adc(0)
    offsetI = (offsetI + (sampleI-offsetI)/1024)
    filteredI = sampleI - offsetI
    sqI = filteredI * filteredI
    sumI = sumI + sqI
ICAL = 18.5 #Calibration to be added later
I_RATIO = ICAL *((SupplyVoltage/1000.0) / (ADC_COUNTS));
Irms = I_RATIO * math.sqrt(sumI / samples)
print(Irms)