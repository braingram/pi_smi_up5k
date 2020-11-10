import time

import spidev


spi_speed_hz = 2500000
spi_delay_us = 0

spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode = 0b11  # set mode: pol 1 pha 1
spi.max_speed_hz = 25000000  # maximum speed of 25MHz
spi.no_cs = True  # disable chip selects

msg = b'\x07\x00'
resp = spi.xfer3(msg, spi_speed_hz, spi_delay_us)
spi.close()

print("Raw sent: {}".format(msg))
print("Raw response: {}".format(resp))

print("Sent {}".format(bin(msg[0])))
print("Received {}".format(bin(resp[-1])))
