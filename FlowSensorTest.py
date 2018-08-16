import Adafruit_MCP3008
from time import sleep
import math
CLK = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

while 1:
    print(mcp.read_adc(0))
    print(mcp.read_adc(1))
    print(mcp.read_adc(2))
    print(mcp.read_adc(3))
    print(mcp.read_adc(4))
    print(mcp.read_adc(5))
    print(mcp.read_adc(6))
    print(mcp.read_adc(7))
    print("   ")
    sleep(1)
