#!/usr/bin/env python3

from time import sleep
import adlinkusb
import sys
from screen_config import up, down, clear


def printhelp():
    print("screen.py controls the adlink relays at New Hope.\n" +
          "\tusage:" +
          "\tscreen.py [-u/-d/-h]\n" +
          "\t-u) roll screen up\n" +
          "\t-d) roll screen down\n" +
          "\t-h) print this message")


if len(sys.argv) != 2:
    print("Wrong number of arguments!\n")
    printhelp()
    exit(1)

match sys.argv[1]:
    case "-d":
        code = down
    case "-u":
        code = up
    case "-h":
        printhelp()
        exit()
    case _:
        print("Unrecognized argument!\n")
        printhelp()
        exit()


device = adlinkusb.DAQ7250()
device.connect()

device.set_dos(code)
sleep(0.5)
device.set_dos(clear)
