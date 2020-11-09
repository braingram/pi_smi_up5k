import time

import spidev


spi_speed_hz = 1000000
spi_delay_us = 1

spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode = 0b11  # set mode: pol 1 pha 1
spi.max_speed_hz = 25000000  # maximum speed of 25MHz
spi.no_cs = True  # disable chip selects

msg = b'\x07'
resp = spi.xfer3(msg, spi_speed_hz, spi_delay_us)
print(f"Sent {msg!r}, received {resp!r}")
spi.close()
