#!/usr/bin/env python3.7

import signal
import sys
import time

import smbus

assert len(sys.argv) == 2, "missing output file"
ofile = sys.argv[1]

# handle ctr-c
def signal_handler(sig, frame):
        print('done')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

sr = 100.

channel = 1
READ_BIT = 0x01
WRITE_BIT = 0x00
DUMMY_BYTE = 0xAA
MEASURE_MODE = 0x06 # Only accelerometer


bus = smbus.SMBus(channel)    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
DEVICE_ADDRESS = 0x1D

DEVICE_REG_MODE1 = 0x00
DEVICE_REG_LEDOUT0 = 0x1d

#Addresses
RANGE = 0x2C
RANGE_2G = 0x01
POWER_CTL = 0x2D
AXIS_START          = 0x08
AXIS_LENGTH         = 9

# range of the accelerometric data
bus.write_byte_data(DEVICE_ADDRESS, RANGE, RANGE_2G)

# enable measure mode
bus.write_byte_data(DEVICE_ADDRESS, POWER_CTL, MEASURE_MODE)

# read Z acceleration

with open(ofile, 'w') as f:
  while 1:

    initial_time = time.perf_counter()
    axisBytes = bus.read_i2c_block_data(0x1d, AXIS_START, AXIS_LENGTH)
    axisX = (axisBytes[0] << 16 | axisBytes[1] << 8 | axisBytes[2]) >> 4
    axisY = (axisBytes[3] << 16 | axisBytes[4] << 8 | axisBytes[5]) >> 4
    axisZ = (axisBytes[6] << 16 | axisBytes[7] << 8 | axisBytes[8]) >> 4

    if(axisX & (1 << 20 - 1)):
        axisX = axisX - (1 << 20)

    if(axisY & (1 << 20 - 1)):
        axisY = axisY - (1 << 20)

    if(axisZ & (1 << 20 - 1)):
        axisZ = axisZ - (1 << 20)

    f.write("{} {} {} {}\n".format(initial_time, axisX, axisY, axisZ))
    ending_time = time.perf_counter()
    sleep_time = 1.0/sr - (ending_time - initial_time) if 1.0/sr > (ending_time - initial_time) else 0.0

    time.sleep(sleep_time)
