import os
import time
import serial
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

def read_channel(x, y, ser):
    value_scaled = int(((chan[x].value / raw) * pro))
    if preval[x] == value_scaled:
        return
    preval[x] = value_scaled

    chval = value_scaled + (1000 * (y + 1))
    print(chval)
    
    try:
        ser.write(str(chval).encode())
    except OSError:
        print("Connection Lost!")
        connect()
    return(0)

def connect():
    interval=0
    success=0

    print('Awaiting connection to Teensy...')
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

print('=================')
print('  Pi Lightboard  ')
print('=================')
print('')
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
chan = []
for i in range(8):
    chan.append(eval('AnalogIn(mcp1, MCP.P{1}'.format(i)))

preval = [0, 0, 0, 0, 0, 0, 0, 0]
# variables for remap_range
raw = 65290
pro = 255

while True:
    # read/write channels
    # time.sleep(1)
    fail = read_channel(0, 0, ser)
    fail = read_channel(1, 1, ser)
    fail = read_channel(2, 2, ser)
    fail = read_channel(3, 3, ser)
    fail = read_channel(4, 4, ser)
    fail = read_channel(5, 5, ser)
    fail = read_channel(6, 6, ser)
    if fail!=0:
        ser = serial.Serial(connect(),9600)
