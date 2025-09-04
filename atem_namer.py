#!/usr/bin/env/python3
"""atem_namer.py - Sets the names of the outputs in ATEM."""

import argparse
import PyATEMMax


def read_to_array(file):
    array = []
    with open(file) as f:
        for line in f:
            array.append(line.rstrip())
    return array


MAXTRIES = 8

parser = argparse.ArgumentParser()
parser.add_argument('ip', help='switcher IP address')
args = parser.parse_args()

switcher = PyATEMMax.ATEMMax()

switcher.connect(args.ip)

AUXES = read_to_array("outputs.txt")

INPUTS = read_to_array("inputs.txt")

for i in range(MAXTRIES):
    if switcher.waitForConnection(infinite=False):
        counter = 0
        print("Connected on attempt {}.".format(i))
        for inp in INPUTS:
            counter = counter + 1
            switcher.setInputLongName(counter, inp.split('|')[0])
            switcher.setInputShortName(counter, inp.split('|')[1])
        counter = 8000
        for aux in AUXES:
            counter = counter + 1
            switcher.setInputLongName(counter, aux.split('|')[0])
            switcher.setInputShortName(counter, aux.split('|')[1])
        break
    else:
        print("Failed attempt {}.".format(i))

switcher.disconnect()
