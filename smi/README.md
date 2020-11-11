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
