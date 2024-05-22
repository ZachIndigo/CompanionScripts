#!/usr/bin/env python3

from pymodbus.client import ModbusTcpClient
import sys
from time import sleep

timetomove = 0
ipaddress = ""

def ctlrelay(ctl):
    client = ModbusTcpClient(ipaddress)
    client.connect()
    for relay in range(2,10):
        client.write_coils(relay, ctl)
    result = client.read_coils(2, 8, slave=1)
    print(result.bits)
    client.close()

def printhelp():
    print("relays.py controls the web relays for the relays at the 288 New Hope campus.\n" +
          "\tusage:" +
          "\tscreen.py [-i/-o]\n" + 
          "\tscreen.py -h\n" +
          "\t-i) turn relay(s) on\n" +
          "\t-o) turn relay(s) off\n" +
          "\t-h) print this message")

if len(sys.argv) < 2 or len(sys.argv) > 4:
    print("Wrong number of arguments!\n")
    printhelp()
    exit(1)

relays = 0
skip = 0
ctl = False

for iterator in range(1,len(sys.argv)):
    if (skip > 0):
        skip = skip - 1
        continue
    print(sys.argv[iterator])
    match sys.argv[iterator]:
        case "-i":
            ctl = True
        case "-o":
            ctl = False
        case "-h":
            printhelp()
            exit()
        case _:
            print("Unrecognized argument!\n")
            printhelp()
            exit()

print("turn on:", ctl)

ctlrelay(ctl)
