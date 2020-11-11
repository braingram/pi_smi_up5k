Disable i2c, spi, camera [not sure if needed], uart
Enable smi & smi-dev in /boot/config.txt
```
dtparam=spi=off
dtparam=i2c_arm=off
dtparam=i2c0=off
dtparam=i2c1=off
enable_uart=0
dtoverlay=smi
dtoverlay=smi-dev
```

Not sure why some GPIO are still not in alt1 mode, force them after boot

```bash
# gpio 0,1,26,27 still in mode 'IN' [26 and 27 are fine]
sudo rmmod i2c-dev  # maybe blacklist this
gpio mode 30 alt1  # sets gpio 0
gpio mode 31 alt1  # sets gpio 1
```

Run gpio readall to see states of all pins
```bash
gpio readall
```

There should now be a /dev/smi device (with root permissions)


With default settings:
SA5:SA0: normally high (0=low) MSB-LSB, asserts ~8 ns before SOE/SWE falling edge, deasserts 8 ns after SOE/SWE rising
SOE/SE: normally high, goes low on read (data OK on falling edge?)SWE/SRW: normally high, goes low on write (data OK on falling edge), low pulse duration is 24ns
SD15:SD0: ? 0=low 1=high MSB-LSB (when writing to /dev/smi order is LSByte then MSByte)

~16 ns between sequential writes, so bus is default 25 MHz giving throughput of 50 MBs (25 MBs if 8 bit)
