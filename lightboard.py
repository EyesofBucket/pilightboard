import os
import time
import serial
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

fader_count = 8
current_values = [0 for _ in range(8)]

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

    #print(position)
    return(position)

def write_channel(ser, data):
    message = data['value'] + (1000 * (data['channel'] + 1))
    #print(message)

    ser.write(str(message).encode())
    current_values[data['channel']] = data['value']
    return()

def fade_channels(ser, data, duration):
    step_length = 0.05
    steps = (duration / step_length) + 1

    x = 0
    for d in data:
        #print(d)
        data[x]['step_size'] = (d['value_end'] - d['value_start']) / steps
        x+=1
        
    for step in range(int(steps)):
        for d in data:
            ch_data = {'channel': d['channel'],
                       'value': int(d['value_start'] + (d['step_size'] * step))}
            write_channel(ser, ch_data)
        time.sleep(step_length)

    for d in data:
        ch_data = {'channel': d['channel'], 'value': d['value_end']}
        write_channel(ser, ch_data)

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
    fd = [{'channel': 1, 'value_start': current_values[1], 'value_end': fader_values[0]}]

    try:
        fade_channels(ser, fd, fader_values[1] / 100)
    except OSError:
        print("Connection Lost!")
        ser = connect()
