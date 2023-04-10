#!/usr/bin/env python3

import sys

login = True

if sys.argv[2] == "nologin":
    login = False

if len(sys.argv) < 5 or len(sys.argv) > 6:
    print("Number of arguments doesn't make sense!\n")
    exit(1)

from telnetlib import Telnet as tn
import time

timeout = 8

act1=sys.argv[3]
act2=sys.argv[4]
if not login:
    act3=sys.argv[5]

ups = tn(sys.argv[1],5214,timeout)
if login:
    ups.read_until(b"login: ",timeout)
    ups.write(b"localadmin\r\n")
    ups.read_until(b"Password: ",timeout)
    ups.write((sys.argv[2] + "\r\n").encode("ascii"))
    ups.read_until(b">> ",timeout)
    ups.write(b"e\r\n")
    ups.read_until(b"$> ",timeout)
else:
    time.sleep(4)
if login and (act1 == "on" or act1 == "off"):
    print("Turning load 1 " + act1 + ".")
    ups.write(("loadctl " + act1 + " -o 1 --force\r\n").encode("ascii"))
    ups.read_until(b'$> ',timeout)
elif sys.argv[3] == "on" or act1 == "off":
    print("Turning load 1 " + act1 + ".")
    ups.write(("POD1" + act1.upper() + "\r\n").encode("ascii"))
    time.sleep(2)
else:
    print("Not changing load 1.")
if login and (act2 == "on" or act2 == "off"):
    print("Turning load 2 " + act2 + ".")
    ups.write(("loadctl " + act2 + " -o 2 --force\r\n").encode("ascii"))
    ups.read_until(b'$> ',timeout)
elif act2 == "on" or act2 == "off":
    print("Turning load 2 " + act2 + ".")
    ups.write(("POD2" + act2.upper() + "\r\n").encode("ascii"))
    time.sleep(2)
else:
    print("Not changing load 2.")
if not login and (act3 == "on" or act3 == "off"):
    print("Turning load 3 " + act3 + ".")
    ups.write(("POD3" + act3.upper() + "\r\n").encode("ascii"))
    time.sleep(2)
if login:
    ups.write(b"exit\r\n")
    ups.read_until(b"Farewell, localadmin.\r\r\n")
ups.close()
