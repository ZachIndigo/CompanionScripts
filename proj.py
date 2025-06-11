#!/usr/bin/env python3

from pysdcp import Projector
from time import sleep
import sys

args_len = len(sys.argv)

first_part = ""
is_second_part = False

if args_len <= 2:
    exit()

PROJ_IP_ADDRESS = sys.argv[1]

pj = Projector(PROJ_IP_ADDRESS)


def do_first_part(arg):
    if arg == "power":
        return True
    elif arg == "mute":
        return True
    elif arg == "sleep":
        return True
    else:
        return False


def do_sleep(arg):
    try:
        s = float(arg)
    except ValueError:
        print(f"Value {arg} doesn't look like a number!")
        return False
    sleep(s)
    return True


def do_power(arg, pj):
    if arg == "on":
        pj.set_power(True)
    elif arg == "off":
        pj.set_power(False)
    elif arg == "get":
        print(pj.get_power())
    else:
        print("Command not understood.")
        return False
    return True


def do_mute(arg, pj):
    if arg == "on":
        pj.set_mute(True)
    elif arg == "off":
        pj.set_mute(False)
    elif arg == "get":
        print(pj.get_mute())
    else:
        print("Command not understood.")
        return False
    return True


for i in range(2, args_len):
    if not is_second_part:
        if not do_first_part(sys.argv[i]):
            print("Command not understood.")
            exit()
        else:
            is_second_part = True
        first_part = sys.argv[i]
    else:
        is_second_part = False
        if first_part == "sleep":
            if not do_sleep(sys.argv[i]):
                break
        elif first_part == "power":
            if not do_power(sys.argv[i], pj):
                break
        elif first_part == "mute":
            if not do_mute(sys.argv[i], pj):
                break
