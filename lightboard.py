import os
import time
import serial
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# establish serial connection
ser = serial.Serial('/dev/ttyACM0',9600)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
 
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)
 
# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create analog input channels
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)
chan3 = AnalogIn(mcp, MCP.P3)
chan4 = AnalogIn(mcp, MCP.P4)
chan5 = AnalogIn(mcp, MCP.P5)

# variables for remap_range
lin_max_raw = 65290
lin_max_pro = 255

def remap_range(value, left_max, right_max, channel):
    value_scaled = ((value / left_max) * right_max) + (1000 * (channel + 1))
    return int(value_scaled)

def read_channel(x):
    if x == 0:
        scha = remap_range(chan0.value, lin_max_raw, lin_max_pro, x)
    if x == 1:
        scha = remap_range(chan1.value, lin_max_raw, lin_max_pro, x)
    if x == 2:
        scha = remap_range(chan2.value, lin_max_raw, lin_max_pro, x)
    if x == 3:
        scha = remap_range(chan0.value, lin_max_raw, lin_max_pro, x)
    if x == 4:
        scha = remap_range(chan1.value, lin_max_raw, lin_max_pro, x)
    if x == 5:
        scha = remap_range(chan2.value, lin_max_raw, lin_max_pro, x)
    print(scha)
    return int(scha)

while True:
    # read/write channels
    ser.write(str(read_channel(0)).encode())
    ser.write(str(read_channel(1)).encode())
    ser.write(str(read_channel(2)).encode())
    ser.write(str(read_channel(3)).encode())
    ser.write(str(read_channel(4)).encode())
    ser.write(str(read_channel(5)).encode())