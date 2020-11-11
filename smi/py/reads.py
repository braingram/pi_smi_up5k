import ctypes
import fcntl
import os
import struct


fn = '/dev/smi'

fd = os.open(fn, os.O_RDWR)

_io = lambda a, b: a << (4 * 2) | b

magic = 0x01

get_settings = _io(magic, 0)
set_settings = _io(magic, 1)
address = _io(magic, 2)

fcntl.ioctl(fd, address, 0b100000)
# write some data
#os.write(fd, b'\xaa\xaa\x55\x55')
#os.write(fd, b'\x00\x01\x00\x00')
os.write(fd, b'\x01\x02')
# read some data
print("Read: {}".format(os.read(fd, 4)))
os.close(fd)
