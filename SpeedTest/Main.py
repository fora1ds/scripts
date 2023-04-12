#!/usr/bin/env python3

'''
This program is a command line interface for working with Ookla speedtest.net
'''

import SpeedTest
import argparse

def Convert_To_JSON(servers, keys):
    for index, server in enumerate(servers):
        print('\n{}:'.format(index), '\n {', end='')

        for key in keys:
            Last = ',\n '

            if key == keys[-1]:
                Last = '}\n'

            print('"{}": "{}"'.format(key, server.get(key)), end=Last)

Argument = argparse.ArgumentParser(description='Internet Speed Test Using Ookla www.speedtest.net', add_help=False, usage=argparse.SUPPRESS)

Argument.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show This Help Message')
Argument.add_argument('--all', action='store_true', help='Perform Download And Upload Test')
Argument.add_argument('--no-perform-download', action='store_true', help='Do Not Perform Download Test')
Argument.add_argument('--no-perform-upload', action='store_true', help='Do Not Perform Upload Test')
Argument.add_argument('--servers', action='store_true', help='Show List Of Ookla Servers')
Argument.add_argument('--server', type=int, help='Select A Server Number From The List Of Ookla Servers')
Argument.add_argument('--format', help='Show Bytes In Other Units (Bps, Kbps, Mbps, Gbps, Tbps)')
Argument.add_argument('--json', action='store_true', default=True, help='Show Scan Result In JSON Format')
Argument.add_argument('--csv', action='store_true', help='Show Scan Result In CSV Format')

Arguments = vars(Argument.parse_args())

Internet = SpeedTest.SpeedTest()

Statistics = {}

if Arguments['server'] is not None:
    if Arguments['server'] <= len(Internet.servers()):
        Internet.select_server(number=Arguments['server'])
    else:
        print('The Value Is Greater Than The Number Of Servers In The List')
        exit(0)

if Arguments['all'] == True:
    Statistics['Download'] = Internet.download()
    Statistics['Upload'] = Internet.upload()

elif Arguments['no_perform_download'] == True:
    Statistics['Upload'] = Internet.upload()

elif Arguments['no_perform_upload'] == True:
    Statistics['Download'] = Internet.download()

if Arguments['servers'] == True:
    Convert_To_JSON(Internet.servers(),
            ['name', 'country', 'sponsor', 'host', 'distance', 'lat', 'lon', 'id'])

if Arguments['format'] != None:
    Types = SpeedTest.Format()

    Formatters = {'bps': Types.to_Bps, 'kbps': Types.to_Kbps,
                  'mbps': Types.to_Mbps, 'gbps': Types.to_Gbps, 'tbps': Types.to_Tbps}

    Format = Arguments['format'].lower()
    Formatter = Formatters.get(Format)

    try:
        for name, value in Statistics.items():
            Statistics[name] = Formatter(value)
    except AttributeError:
        print('Format {} Not Found'.format(Format))
        exit(0)

if Arguments['csv'] == True:
    print(', '.join(Statistics.keys()))

    for value in Statistics.values():
        print(value, end=', ')

elif True in [Arguments['all'], Arguments['no_perform_download'], Arguments['no_perform_upload']]:
    print(Statistics)
