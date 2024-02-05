#!/usr/bin/env python3

from datetime import datetime
import serial
import sys
import re

# Open serial port
port = serial.Serial(sys.argv[1], sys.argv[2], rtscts=True, dsrdtr=False)
port.dtr = True
port.rts = False

# Flush input and output buffers
port.flushInput()
port.flushOutput()

# Infinite loop to continuously read from serial port
while True:
    # Read a line from serial port
    line = port.readline()

    # Push everything to console
    print('[{}] {}'.format(datetime.now(), line.decode('utf-8')), end='')

    # Write logs day-wise to a file
    lfname = '{}-{}.log'.format(datetime.today().strftime('%Y-%m-%d'), sys.argv[1].split('/')[-1])
    with open(lfname, 'ab+') as f:
        f.write(bytes('[{}] {}\n'.format(datetime.now(), line.decode('utf-8')), encoding='utf8'))

    # Filter and push errors to a separate file
    efname = '{}-{}-errors.log'.format(datetime.today().strftime('%Y-%m-%d'), sys.argv[1].split('/')[-1])
    if re.search(b'\x1b\[0;31mE \(', line):
        with open(efname, 'ab+') as f:
            f.write(bytes('[{}] {}\n'.format(datetime.now(), line.decode('utf-8')), encoding='utf8'))

