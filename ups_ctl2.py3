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
                    choices=[0, 12, 15],
                    help='UPS PADM version to use (0 for JuiceGoose) (0,12,*15)')
parser.add_argument('-1', '--port-1', type=str, default=None,
                    help='Power state for the first outlet. (*None)')
parser.add_argument('-2', '--port-2', type=str, default=None,
                    help='Power state for the second outlet. (*None)')
parser.add_argument('-3', '--port-3', type=str, default=None,
                    help='Power state for the third outlet (only applicable for JuiceGeese). (*None)')
parser.add_argument('-q', '--quiet', action='store_true',
                    help='Suppress standard output.')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Prints telnet output.')
args = parser.parse_args()

if (args.passwd == None and args.ups_version != 0) or args.ip == None:
    print("ups_ctl needs a password (if not a JuiceGoose) and ip address!")
    quit()

timeout = 5

act1 = args.all_ports
act2 = args.all_ports
if args.ups_version == 0:
    act3 = args.all_ports
else:
    act3 = None
if args.port_1:
    act1 = args.port_1
if args.port_2:
    act2 = args.port_2
if args.ups_version == 0 and args.port_3:
    act3 = args.port_3
if act1 == None and act2 == None and act3 == None:
    print("Not doing anything, because no action provided.")
    quit()

action_bitmask = 0

if act1 == "on" or act1 == "off":
    action_bitmask = action_bitmask + 0b1
if act2 == "on" or act2 == "off":
    action_bitmask = action_bitmask + 0b10
if act3 == "on" or act3 == "off":
    action_bitmask = action_bitmask + 0b100

import telnetlib3, asyncio
from time import sleep

async def shell(reader, writer):
    global action_bitmask
    action_bitmask = action_bitmask % 0b1000
    if args.ups_version == 0:
        if not args.quiet:
            print('Connecting...\n')
        writer.write('help\r\n')
    while True:
        output = await reader.read(1024)
        if not output:
            break
        elif args.ups_version == 0:
            if output.endswith('>'):
                if action_bitmask > 0b111:
                    action_bitmask = action_bitmask - 0b1000
                elif action_bitmask > 0b11:
                    if not args.quiet:
                        print('Turning group 3 {}...\n'.format(act3))
                    # login
                    action_bitmask = action_bitmask - 0b100
                    writer.write('POD3{}\r\n'.format(act3))
                elif action_bitmask > 0b1:
                    if not args.quiet:
                        print('Turning group 2 {}...\n'.format(act2))
                    # login
                    action_bitmask = action_bitmask - 0b10
                    writer.write('POD2{}\r\n'.format(act2))
                elif action_bitmask > 0:
                    if not args.quiet:
                        print('Turning group 1 {}...\n'.format(act1))
                    # login
                    action_bitmask = 0
                    writer.write('POD1{}\r\n'.format(act1))
                else:
                    return
        elif args.ups_version == 12 or args.ups_version == 15:
            if output.endswith('login: ') or output.endswith('Username: '):
                if not args.quiet:
                    print('Logging in...\n')
                # login
                writer.write('localadmin\n')
            elif output.endswith('Password: '):
                # password
                writer.write('{}\n'.format(args.passwd))
            elif output.endswith('>> '):
                # get to the menu
                writer.write('e\n')
            elif output.endswith('$> '):
                # actually do stuff
                if action_bitmask > 0b11:
                    action_bitmask = action_bitmask - 0b100
                elif action_bitmask > 0b1:
                    if not args.quiet:
                        print('\nTurning group 2 {}...\n'.format(act2))
                    writer.write('loadctl {} -o 2 --force\n'.format(act2))
                    action_bitmask = action_bitmask - 0b10
                elif action_bitmask > 0:
                    if not args.quiet:
                        print('\nTurning group 1 {}...\n'.format(act1))
                    writer.write('loadctl {} -o 1 --force\n'.format(act1))
                    action_bitmask = 0
                else:
                    if not args.quiet:
                        print('\nLogging off...\n')
                    writer.write('quit\n')
        if args.verbose:
            print(output, flush=True, end='')
    if args.verbose:
        print()

loop = asyncio.get_event_loop()
coro = telnetlib3.open_connection(args.ip, 5214, shell=shell)
reader, writer = loop.run_until_complete(coro)
loop.run_until_complete(writer.protocol.waiter_closed)

for i in range(4):
    if action_bitmask != 0:
        print("Connection failed, trying again...")
        sleep(5)
        coro = telnetlib3.open_connection(args.ip, 5214, shell=shell)
        reader, writer = loop.run_until_complete(coro)
        loop.run_until_complete(writer.protocol.waiter_closed)
    else:
        break
