import os
import time
import serial
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

fader_count = 8
current_values = [None for _ in range(8)]

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
    return(ser)

def get_faders():
    position = []

    for i in range(fader_count):
        position.append(int(((faders[i].value / 65290) * 255)))

    return(position)

def write_channels(ser, channel_values):
    for channel, set_value in channel_values.items():
        message = str(channel) + ',' + str(set_value)
        print(message)
    
        ser.write(message.encode())
        current_values[channel] = set_value
    return()

def fade_channels(ser, channel_values, duration):
    step_length = 0.1
    steps = duration / step_length
    result = [{} for _ in range(int(steps))]

    for channel, set_value in channel_values.items():
        current_value = current_values[channel] 
        step_size = set_value - current_value / steps

        for s in range(steps - 1):
            current_value = current_value + step_size
            result[s][channel] = int(current_value)

        result[s][channel] = set_value

    for r in result:
        write_channels(ser, r)
        time.sleep(step_length)

print('=================')
print('  Pi Lightboard  ')
print('=================')
print('')
ser = connect()

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
 
cs1 = digitalio.DigitalInOut(board.D22)
cs2 = digitalio.DigitalInOut(board.D22)
 
mcp1 = MCP.MCP3008(spi, cs1)
mcp2 = MCP.MCP3008(spi, cs2)

faders = []
for i in range(fader_count):
    faders.append(eval('AnalogIn(mcp1, MCP.P{0})'.format(i)))

while True:
    fader_values = get_faders()
    try:
        fade_channels(ser, {1: fader_values[0]}, fader_values[1])
    except OSError:
        print("Connection Lost!")
        ser = connect()
