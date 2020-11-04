"""
To program the fpga: (when does cdone go low?)
    - bring fpga into creset (pull reset low)
    - set sclk to 1, [drive ss_b to low (hw pulled low)]
    - wait >=200 ns
    - release creset or drive creset to high
    - wait >=300 us
    - send bitstream over spi (MSB, CLK falling edge, no interruption 1mHz to 25MHz)
    - check cdone == 1, if not ERROR
    - send >=49 dummy SPI bits (rising-to-rising edge)

TODO
    - enable/disable spi (dtparam ?)
    - disable spi chipselect lines (GPIO8/7)
"""
import sys
import time

import RPi.GPIO as GPIO
import spidev


cdone_pin = 26
creset_pin = 27

sclk_pin = 11
mosi_pin = 10
miso_pin = 9

spi_speed_hz = 1000000
spi_delay_us = 1

# read bitstream
if len(sys.argv) < 2:
    raise Exception("Requires bitstream filename as argument")
bit_filename = sys.argv[1]
with open(bit_filename, 'rb') as f:
    bitstream = f.read()
print("Read {} bytes from {}".format(len(bitstream), bit_filename))

# make >=49 dummy bits [7 bytes = 56 bits]
dummy_bits = bytes([170] * 7)

# setup gpio pins
print("Setting up gpio pins...")
GPIO.setmode(GPIO.BCM)
GPIO.setup(cdone_pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(creset_pin, GPIO.OUT, initial=GPIO.HIGH)
# helper functions
cdone = lambda: GPIO.input(cdone_pin)
creset = lambda v: GPIO.output(creset_pin, v)

# prep spi
spi = spidev.SpiDev()

print("Initial cdone state is: {}".format(cdone()))

# bring fpga into reset
print("Resetting fpga...")
creset(0)

# setup spi
print("Enabling spi...")
spi.open(0, 0)
spi.mode = 0b11  # set mode: pol 1 pha 1
spi.max_speed_hz = 25000000  # maximum speed of 25MHz
spi.no_cs = True  # disable chip selects

# wait >=200 ns
time.sleep(0.001)

print("Releasing reset for programming...")
creset(1)

# wait >=300 us
time.sleep(0.001)

print("Sending bitstream...")
spi.xfer3(bitstream, spi_speed_hz, spi_delay_us)

print("pausing...")
t0 = time.monotonic()
while not cdone():
    if time.monotonic() - t0 > 0.1:
        raise Exception("Programming failed!")

print("Programmed! enabling...")
spi.xfer3(dummy_bits, spi_speed_hz, spi_delay_us)

print("Cleaning up...")
spi.close()
