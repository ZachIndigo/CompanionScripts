#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Control TrippLite PowerAlert UPSes')
parser.add_argument('-a', '--all-ports', type=str, default=None,
                    help='Power state for all outlets (overwritten by -1 or -2). (*None)')
parser.add_argument('-i', '--ip', type=str, default=None,
                    help='IP address of the UPS. (*None)')
parser.add_argument('-p', '--passwd', type=str, default=None,
                    help='PADM password for localadmin. (*None)')
parser.add_argument('-u', '--ups-version', type=int, default=15,
                    choices=[12, 15],
                    help='UPS PADM version to use (12,*15)')
parser.add_argument('-1', '--port-1', type=str, default=None,
                    help='Power state for the first outlet. (*None)')
parser.add_argument('-2', '--port-2', type=str, default=None,
                    help='Power state for the second outlet. (*None)')
parser.add_argument('-q', '--quiet', action='store_true',
                    help='Suppress standard output.')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Prints telnet output.')
args = parser.parse_args()

if args.passwd == None or args.ip == None:
    print("ups_ctl needs a password and ip address!")
    quit()

timeout = 5

act1 = args.all_ports
act2 = args.all_ports
if args.port_1:
    act1 = args.port_1
if args.port_2:
    act2 = args.port_2

if act1 == None and act2 == None:
    print("Not doing anything, because no action provided.")

from telnetlib import Telnet as tn
import time

log = ""

ups = tn(args.ip,5214,timeout)
if not args.quiet:
    print("Logging in...")
log = ups.read_until(b"login: ", 15)
if args.verbose:
    print(repr(log))
ups.write(b"localadmin\r\n")
log = ups.read_until(b"Password: ",timeout)
if args.verbose:
    print(repr(log))
ups.write((args.passwd + "\r\n").encode("ascii"))
if args.ups_version == 15:
    log = ups.read_until(b">> ",timeout)
    if args.verbose:
        print(repr(log))
    ups.write(b"e\r\n")
log = ups.read_until(b"$> ",timeout)
if args.verbose:
    print(repr(log))

if act1 == "on" or act1 == "off":
    if not args.quiet:
        print("Turning load 1 " + act1 + ".")
    ups.write(("loadctl {} -o 1 --force\r\n".format(act1)).encode("ascii"))
    log = ups.read_until(b'$> ',timeout)
    if args.verbose:
        print(repr(log))
else:
    if not args.quiet:
        print("Not changing load 1.")
if act2 == "on" or act2 == "off":
    if not args.quiet:
        print("Turning load 2 " + act2 + ".")
    ups.write(("loadctl {} -o 2 --force\r\n".format(act2)).encode("ascii"))
    log = ups.read_until(b'$> ',timeout)
    if args.verbose:
        print(repr(log))
else:
    if not args.quiet:
        print("Not changing load 2.")

if not args.quiet:
    print("Exiting...")
ups.write(b"exit\r\n")
if args.ups_version == 15:
    log = ups.read_until(b"Farewell, localadmin.\r\r\n")
    if args.verbose:
        print(repr(log))
elif args.ups_version == 12:
    log = ups.read_until(b"Goodbye.\r\n")
    if args.verbose:
        print(repr(log))
ups.close()
