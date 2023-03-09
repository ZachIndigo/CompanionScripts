#!/usr/bin/env python3

from pysdcp import Projector
from time import sleep
import sys

PROJ_IP_ADDRESS="10.45.0.100"

args_len = len(sys.argv)

first_part = ""
is_second_part = False

if args_len == 1:
    exit()

pj = Projector(PROJ_IP_ADDRESS)

for i in range(1, args_len):
    if is_second_part == False:
        if sys.argv[i] == "power":
            is_second_part = True
        elif sys.argv[i] == "mute":
            is_second_part = True
        elif sys.argv[i] == "sleep":
            is_second_part = True
        else:
            print("Command not understood.")
            exit()
        first_part = sys.argv[i]
    else:
        is_second_part = False
        if first_part == "sleep":
            try:
                s = float(sys.argv[i])
            except ValueError:
                print(f"Value {sys.argv[i]} doesn't look like a number!")
                continue
            sleep(s)
        elif first_part == "power":
            if sys.argv[i] == "on":
                pj.set_power(True)
            elif sys.argv[i] == "off":
                pj.set_power(False)
            elif sys.argv[i] == "get":
                print(pj.get_power())
            else:
                print("Command not understood.")
        elif first_part == "mute":
            if sys.argv[i] == "on":
                pj.set_mute(True)
            elif sys.argv[i] == "off":
                pj.set_mute(False)
            elif sys.argv[i] == "get":
                print(pj.get_mute())
            else:
                print("Command not understood.")
