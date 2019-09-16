#!/usr/bin/env python3.7

import sys
import time
import smbus

assert len(sys.argv) == 2, "missing output file"
ofile = sys.argv[1]

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
XDATA3 = 0x08
XDATA2 = 0x09
XDATA1 = 0x0A
YDATA3 = 0x0B
YDATA2 = 0x0C
YDATA1 = 0x0D
ZDATA3 = 0x0E
ZDATA2 = 0x0F
ZDATA1 = 0x10
RANGE = 0x2C
POWER_CTL = 0x2D

# Data Range
RANGE_2G = 0x01

# range of the accelerometric data
bus.write_byte_data(DEVICE_ADDRESS, RANGE, RANGE_2G)

# enable measure mode
bus.write_byte_data(DEVICE_ADDRESS, POWER_CTL, MEASURE_MODE)

# read Z acceleration

with open(ofile, 'w') as f:
  while 1:

    zdata = []
    zdata.append(bus.read_byte_data(DEVICE_ADDRESS, ZDATA1) << 1 | READ_BIT)
    zdata.append(bus.read_byte_data(DEVICE_ADDRESS, ZDATA2) << 1 | READ_BIT)
    zdata.append(bus.read_byte_data(DEVICE_ADDRESS, ZDATA3) << 1 | READ_BIT)
    zdata = (zdata[0] >> 4) + (zdata[1] << 4) + (zdata[2] << 12)
    xdata = []
    if zdata & 0x80000 == 0x80000:
        zdata = ~zdata + 1

    xdata.append(bus.read_byte_data(DEVICE_ADDRESS, XDATA1) << 1 | READ_BIT)
    xdata.append(bus.read_byte_data(DEVICE_ADDRESS, XDATA2) << 1 | READ_BIT)
    xdata.append(bus.read_byte_data(DEVICE_ADDRESS, XDATA3) << 1 | READ_BIT)
    xdata = (xdata[0] >> 4) + (xdata[1] << 4) + (xdata[2] << 12)
    if xdata & 0x80000 == 0x80000:
        xdata = ~xdata + 1

    ydata = []
    ydata.append(bus.read_byte_data(DEVICE_ADDRESS, YDATA1) << 1 | READ_BIT)
    ydata.append(bus.read_byte_data(DEVICE_ADDRESS, YDATA2) << 1 | READ_BIT)
    ydata.append(bus.read_byte_data(DEVICE_ADDRESS, YDATA3) << 1 | READ_BIT)
    ydata = (ydata[0] >> 4) + (ydata[1] << 4) + (ydata[2] << 12)
    if ydata & 0x80000 == 0x80000:
        ydata = ~ydata + 1

    f.write("{} {} {} {}\n".format(time.perf_counter(), xdata, ydata, zdata))
    time.sleep(0.004) # 250Hz



