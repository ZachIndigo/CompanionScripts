#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import math
import re
import sys
import time
from dmxpy.DmxPy import *

data = [0, 0, 0, 0, 0, 0]

CHANNELS = 6

def set_dmx_channels(dmx_data = data):
    global dmx
    if len(dmx_data) != CHANNELS:
        print("Wrong number of channels!")
        quit()
    for i in range(CHANNELS):
        dmx.set_channel(i + 1, dmx_data[i])

parser = argparse.ArgumentParser(description='Control Enttec DMX USB Pro')
parser.add_argument('-r', '--rate', type=int, default=57600,
                    help='baud rate for USB communication '
                         '(default: 57600)')
parser.add_argument('-p', '--port', type=str,
                    help='Serial(COM) port, e.g., /dev/ttyUSB1 or COM3')
parser.add_argument('-g', '--port-grep', type=str, default='0403:6001',
                    help='if port not specified attempt to auto-detect '
                         'serial matching grep (default: 0403:6001)')
parser.add_argument('-l', '--level', type=int, default=255,
                    choices=range(0, 256),
                    help='default level [0-255] of unspecified channels '
                         '(default: 255)')
parser.add_argument('-s', '--size', type=int, default=512,
                    help='DMX Size (default: 512)')
parser.add_argument('-b', '--blackout', action='store_true',
                    help='Turn off all lights (level=0)')
parser.add_argument('-w', '--whiteout', action='store_true',
                    help='Turn on all lights at level')
parser.add_argument('-d', '--demo', action='store_true',
                    help='Play demo light pattern')
parser.add_argument('-c', '--colors', type=str, default='',
                    help='Sets channel values in hex')
parser.add_argument('-t', '--change', type=str, default='',
                    help='Sets channel values in hex')
args = parser.parse_args()

dmx = DmxPy(args.port, baud_rate=args.rate, default_level=args.level,
            dmx_size=args.size, port_grep=args.port_grep)

if not args.blackout and not args.whiteout and not args.demo and not args.colors and not args.change:
    print('Select an action: [b]lackout, [w]hiteout, [d]emo, or [c]olors')
    parser.print_usage()
    exit(1)

if args.change:
    try:
        with open('lightdata.txt', 'r') as d:
            last_value = d.readline()
    except FileNotFoundError:
        print("File lightdata.txt does not exist, will create later.")
        last_value = '000000000000'
    channels = math.floor(len(last_value) / 2)
    for i in range(CHANNELS):
        if (i >= channels):
            value = 0
        else:
            chan = last_value[(i*2):(2+i*2)]
            value = int(chan, 16)
            data[i] = value

if args.blackout:
    dmx.blackout()
    dmx.render()
    with open('lightdata.txt', 'w') as d:
        last_value = d.write('000000000000' + '\n')
elif args.whiteout:
    dmx.whiteout()
    dmx.render()
    with open('lightdata.txt', 'w') as d:
        last_value = d.write('ffffffffffff' + '\n')
elif args.demo:
    dmx.set_channel(1, 100)
    dmx.set_channel(2, 50)
    dmx.render()
    time.sleep(5)
    dmx.set_channel(3, 100)
    dmx.render()
    time.sleep(5)
    dmx.blackout()
    dmx.render()
    time.sleep(5)
    dmx.whiteout()
    dmx.render()
    print(dmx.dmxData[1])
elif args.colors:
    channels = math.floor(len(args.colors) / 2)
    if not args.change:
        for i in range(CHANNELS):
            if (i >= channels):
                value = 0
            else:
                chan = args.colors[(i*2):(2+i*2)]
                value = int(chan, 16)
            data[i] = value
            print(i, value)
    elif args.change == "up":
        for i in range(CHANNELS):
            if (i >= channels):
                delta = 0
            else:
                chan = args.colors[(i*2):(2+i*2)]
                delta = int(chan, 16)
            value = min(255, max(0, data[i] + delta))
            data[i] = value
            print(i, value)
    elif args.change == "down":
        for i in range(CHANNELS):
            if (i >= channels):
                delta = 0
            else:
                chan = args.colors[(i*2):(2+i*2)]
                delta = int(chan, 16)
            value = min(255, max(0, data[i] - delta))
            data[i] = value
            print(i, value)
    set_dmx_channels(data)
    dmx.render()
    with open('lightdata.txt', 'w') as d:
            for i in range(CHANNELS):
                d.write('{:0>2x}'.format(data[i]))
            d.write("\n")
