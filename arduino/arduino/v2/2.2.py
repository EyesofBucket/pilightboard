import os
import time
import serial
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
##CONNECT TO TEENCY
ser = serial.Serial('/dev/ttyACM0',9600)
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)
##channels
#chan = AnalogIn(mcp, MCP.P0)
##set vals
raw = 65290
top = 255
chcount = 7
##remap
def remap_range(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    value_scaled = int(value - left_min) / int(left_span)
    return int(right_min + (value_scaled * right_span))

##while True:
##    
##    ch1 = chan0.value
##    ch1val = remap_range(ch1, 0, raw, 0, top)
##    ch1 = ch1val + 1000
##    ##send serial
##    ser.write(str(ch1).encode())

while True:
    x = 0

    while (x <= chcount):     
        #ch = MCP.P + str(x)
        chan = AnalogIn(mcp, x).value
        #pot = chan.value
        val = remap_range(chan, 0, raw, 0, top)
        channel = ("chan" + str(x)) 
        exec(channel + " = str(val)")   
        #print(y)
        y = val + ((x+1) * 1000)
        print(str(y))
        ser.write(str(y).encode())
        x+=1