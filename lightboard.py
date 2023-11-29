import os
import time
import serial
import threading
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
    message = 's{0} {1}\n'.format(data['channel'], data['value'])
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

def read_serial(ser):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(f"[CONTROL BOX] {line}")

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

thread = threading.Thread(target=read_serial, args=(ser,))
thread.start()

while True:
    fader_values = get_faders()
    fd = [{'channel': 2, 'value_start': 0, 'value_end': 255},
           {'channel': 3, 'value_start': 0, 'value_end': 255},
           {'channel': 4, 'value_start': 0, 'value_end': 255},
           {'channel': 5, 'value_start': 0, 'value_end': 255},
           {'channel': 6, 'value_start': 0, 'value_end': 255},
           {'channel': 7, 'value_start': 0, 'value_end': 255}]

    try:
        #if ser.inWaiting() > 0:
            #print(ser.read(ser.inWaiting() ))
        fade_channels(ser, fd, 5)
    except OSError:
        print("Connection Lost!")
        ser = connect()
