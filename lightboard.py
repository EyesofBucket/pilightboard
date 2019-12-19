import os
import time
import serial
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

def read_channel(x, y):
    #scha = remap_range(chan[x].value, raw, pro, y)
    if preval[x] == chan[x].value:
        return
    preval[x] = chan[x].value
	value_scaled = ((chan[x].value / raw) * pro) + (1000 * (y + 1)) 
    print(scha)
    try:
        ser.write(str(scha).encode())
    except OSError:
        print("Connection Lost.  Trying again.")
        ser = serial.Serial(connect(),9600)
    return
    
#def remap_range(value, left_max, right_max, channel):
#    value_scaled = ((value / left_max) * right_max) + (1000 * (channel + 1))
#    return int(value_scaled)

def connect():
    interval=0
    success=0

    while success==0:
        try:
            ser = serial.Serial('/dev/ttyACM' + str(interval),9600)
        except OSError:
            interval+=1
            if interval==20:
                interval=0
        else:
            success=1
    
    print("Connection Established. '/dev/ttyACM" + str(interval))
    return("/dev/ttyACM" + str(interval))

print('================')
print('  Pi Lighboard  ')
print('================')
print('')
print('Awaiting connection to Teensy...')
# establish serial connection
ser = serial.Serial(connect(),9600)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
 
# create the cs (chip select)
cs1 = digitalio.DigitalInOut(board.D22)
cs2 = digitalio.DigitalInOut(board.D22)
 
# create the mcp object
mcp1 = MCP.MCP3008(spi, cs1)
mcp2 = MCP.MCP3008(spi, cs2)

# create analog input channels
chan = [AnalogIn(mcp1, MCP.P0), AnalogIn(mcp1, MCP.P1), AnalogIn(mcp1, MCP.P2), AnalogIn(mcp1, MCP.P3), AnalogIn(mcp1, MCP.P4), AnalogIn(mcp1, MCP.P5), AnalogIn(mcp1, MCP.P6), AnalogIn(mcp1, MCP.P7)]
preval = [0, 0, 0, 0, 0, 0, 0, 0]
# variables for remap_range
raw = 65290
pro = 255

while True:
    # read/write channels
    try:
        read_channel(0, 0)
        read_channel(1, 1)
        read_channel(2, 2)
        read_channel(0, 3)
        read_channel(1, 4)
        read_channel(2, 5)
