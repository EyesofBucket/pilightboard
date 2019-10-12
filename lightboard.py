import os
import time
import serial
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

def remap_range(value, left_max, right_max, channel):
    value_scaled = ((value / left_max) * right_max) + (1000 * (channel + 1))
    return int(value_scaled)

def read_channel(x, y):
    scha = remap_range(chan[x].value, raw, pro, y)
    print(scha)
    return int(scha)

def connect():
    interval=0
    success=0
    while success==0:
        try:
            ser = serial.Serial('/dev/ttyACM' + str(interval),9600)
        except:
            interval+=1
        else:
            success=1
    print("Connection Established. '/dev/ttyACM" + str(interval))
    return


# establish serial connection
# ser = serial.Serial('/dev/ttyACM0',9600)
connect()

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

# variables for remap_range
raw = 65290
pro = 255

while True:
    # read/write channels
    # try:
        ser.write(str(read_channel(0, 0)).encode())
        ser.write(str(read_channel(1, 1)).encode())
        ser.write(str(read_channel(2, 2)).encode())
        ser.write(str(read_channel(0, 3)).encode())
        ser.write(str(read_channel(1, 4)).encode())
        ser.write(str(read_channel(2, 5)).encode())
    # except:
        # print("Connection Lost.  Trying again.")
       # connect()