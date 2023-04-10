#!/usr/bin/env python3

import sys

if not (len(sys.argv) == 5):
    print("Number of arguments doesn't make sense!\n")
    exit(1)

from telnetlib import Telnet as tn

timeout = 8

ups = tn(sys.argv[1],5214,timeout)
ups.read_until(b"login: ",timeout)
ups.write(b"localadmin\r\n")
ups.read_until(b"Password: ",timeout)
ups.write((sys.argv[2] + "\r\n").encode("ascii"))
ups.read_until(b">> ",timeout)
ups.write(b"e\r\n")
ups.read_until(b"$> ",timeout)
if (sys.argv[3] == "on") or (sys.argv[3] == "off"):
    print("Turning load 1 " + sys.argv[3] + ".")
    ups.write(("loadctl " + sys.argv[3] + " -o 1\r\n").encode("ascii"))
    ups.read_until(b'[y/n]? ',timeout)
    ups.write(b"y\r\n")
    ups.read_until(b'$> ',timeout)
else:
    print("Not changing load 1.")
if (sys.argv[4] == "on") or (sys.argv[4] == "off"):
    print("Turning load 2 " + sys.argv[4] + ".")
    ups.write(("loadctl " + sys.argv[4] + " -o 2\r\n").encode("ascii"))
    ups.read_until(b'[y/n]? ',timeout)
    ups.write(b"y\r\n")
    ups.read_until(b'$> ',timeout)
else:
    print("Not changing load 2.")
ups.write(b"exit\r\n")
ups.read_until(b"Farewell, localadmin.\r\r\n")
