#!/usr/bin/env python3

from pymodbus.client import ModbusTcpClient
import sys
from time import sleep

timetomove = 45
ipaddress = ""

def movecurtain(breakernumbers):
    client = ModbusTcpClient(ipaddress)
    client.connect()
    for breaker in breakernumbers:
        client.write_coil(breaker, True, slave=1)
    result = client.read_coils(2, 8, slave=1)
    print(result.bits)
    sleep(timetomove)
    for breaker in breakernumbers:
        client.write_coil(breaker, False, slave=1)
    result = client.read_coils(2, 8, slave=1)
    print(result.bits)
    client.close()

def printhelp():
    print("curtains.py controls the web relays for the curtains at the 288 New Hope campus.\n" +
          "\tusage:" +
          "\tscreen.py [-c X] [-u/-d]\n" + 
          "\tscreen.py -h\n" +
          "\t-c X) curtain to control\n" +
          "\t-u) roll curtain(s) up\n" +
          "\t-d) roll curtain(s) down\n" +
          "\t-h) print this message")

if len(sys.argv) < 2 or len(sys.argv) > 4:
    print("Wrong number of arguments!\n")
    printhelp()
    exit(1)

direction = -1
curtains = 0
skip = 0

curtain1 = [ 2, 6 ]
curtain2 = [ 3, 7 ]
curtain3 = [ 4, 8 ]
curtain4 = [ 5, 9 ]

for iterator in range(1,len(sys.argv)):
    if (skip > 0):
        skip = skip - 1
        continue
    print(sys.argv[iterator])
    match sys.argv[iterator]:
        case "-d":
            direction = 1
        case "-u":
            direction = 0
        case "-h":
            printhelp()
            exit()
        case "-c":
            curtains = int(sys.argv[iterator+1])
            skip = skip + 1
        case _:
            print("Unrecognized argument!\n")
            printhelp()
            exit()

print("direction:", direction, "curtain:", curtains)

if direction < 0 or direction > 1:
    print("Direction must be set!")
    printhelp()
    exit(1)

curtainarray = [ ]
match curtains:
    case 0:
        curtainarray.append(curtain1[direction])
        curtainarray.append(curtain2[direction])
        curtainarray.append(curtain3[direction])
        curtainarray.append(curtain4[direction])
        movecurtain(curtainarray)
    case 1:
        curtainarray.append(curtain1[direction])
        movecurtain(curtainarray)
    case 2:
        curtainarray.append(curtain2[direction])
        movecurtain(curtainarray)
    case 3:
        curtainarray.append(curtain3[direction])
        movecurtain(curtainarray)
    case 4:
        curtainarray.append(curtain4[direction])
        movecurtain(curtainarray)
