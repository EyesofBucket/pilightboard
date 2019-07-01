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
 
# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)
 
#print('Raw ADC 0: ', chan0.value)
#print('ADC V0: ' + str(chan0.voltage) + 'V')
#print('Raw ADC 1: ', chan1.value)
#print('ADC V1: ' + str(chan1.voltage) + 'V')
#print('Raw ADC 2: ', chan2.value)
#print('ADC V2: ' + str(chan2.voltage) + 'V')

lin_max_raw = 65290
lin_max_pro = 255


def remap_range(value, left_min, left_max, right_min, right_max):
    # this remaps a value from original (left) range to new (right) range
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min
 
    # Convert the left range into a 0-1 range (int)
    value_scaled = int(value - left_min) / int(left_span)
    #todo add 1000 for each channel
    # Convert the 0-1 range into a value in the right range.
    return int(right_min + (value_scaled * right_span))
 
while True:
    # read the analog pin
    pot_0 = chan0.value
    val_0 = remap_range(pot_0, 0, lin_max_raw, 0, lin_max_pro)
    pot_1 = chan1.value
    val_1 = remap_range(pot_1, 0, lin_max_raw, 0, lin_max_pro)
    pot_2 = chan2.value
    val_2 = remap_range(pot_2, 0, lin_max_raw, 0, lin_max_pro)
#    print(pot_0)
    print(str(val_0) + ', ' + str(val_1) + ', ' + str(val_2))
    
    scha_1 = val_0 + 1000
    print(str(scha_1))
    ##scha2 = str(scha_1).encode()
    ser.write(str(scha_1).encode())
    time.sleep(.01)
    scha_2 = val_1 + 2000
    print(str(scha_2))
    ser.write(str(scha_2).encode())
    time.sleep(.01)
    scha_3 = val_2 + 3000
    print(str(scha_3))
    ser.write(str(scha_3).encode())
    time.sleep(.01)

    
##    ser.write(str(scha_1).encode())
