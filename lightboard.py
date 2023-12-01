import os
import time
import serial
import multiprocessing
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

fader_count = 8
current_values = [0 for _ in range(16)]

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

def get_faders(faders):
    position = []

    for i in range(fader_count):
        position.append(int(((faders[i].value / 65290) * 255)))

    #print(position)
    return(position)

def write_channel(ser, data):
    message = 's{0}:{1}\n'.format(data['channel'], data['value'])
    #print(message)

    ser.write(str(message).encode())
    current_values[data['channel']] = data['value']
    return()

def fade_channels(ser, data, duration):
    steps = 100
    step_length = duration / steps

    x = 0
    for d in data:
        data[x]['step_size'] = (d['value_end'] - d['value_start']) / steps
        x+=1
        
    for step in range(int(steps) + 1):
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
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(f"[CONTROL BOX] {line}")
        except OSError:
            pass

def interactive_mode(ser):
    shell = str(input('> ')) + '\n'
    ser.write(shell.encode())

def wave_test(ser):
    delay = 0.01

    for i in range(1,16):
        comm = 's{0}:1\n'.format(i)
        ser.write(comm.encode())
        time.sleep(delay)

    for i in range(1,16):
        comm = 's{0}:0\n'.format(i)
        ser.write(comm.encode())
        time.sleep(delay)

def fade_test(ser):
    d = 1
    fd1 = []
    fd2 = []

    for c in range(16):
        fd1.append({'channel': c, 'value_start': 0, 'value_end': 255})
        fd2.append({'channel': c, 'value_start': 255, 'value_end': 0})

    fade_channels(ser, fd1, d)
    fade_channels(ser, fd2, d)

def main():
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

    process = multiprocessing.Process(target=read_serial, args=(ser,))
    process.start()

    while True:
        fader_values = get_faders(faders)

        try:
            fade_test(ser)
        except OSError:
            print("Connection Lost!")
            ser = connect()
        except KeyboardInterrupt:
            print("\nExiting")
            process.terminate()
            exit()

if __name__=="__main__": 
    main() 
