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

# set address
settings = [
    ('data_width', ctypes.c_int),
    ('pack_data', ctypes.c_bool),
    ('read_setup_time', ctypes.c_int),
    ('read_hold_time', ctypes.c_int),
    ('read_pace_time', ctypes.c_int),
    ('read_strobe_time', ctypes.c_int),
    ('write_setup_time', ctypes.c_int),
    ('write_hold_time', ctypes.c_int),
    ('write_pace_time', ctypes.c_int),
    ('write_strobe_time', ctypes.c_int),
    ('dma_enable', ctypes.c_bool),
    ('dma_passthrough_enable', ctypes.c_bool),
    ('dma_read_thresh', ctypes.c_int),
    ('dma_write_thresh', ctypes.c_int),
    ('dma_panic_read_thresh', ctypes.c_int),
    ('dma_panic_write_thresh', ctypes.c_int),
]


class Settings(ctypes.Structure):
    _fields_ = settings


s = Settings()
assert fcntl.ioctl(fd, get_settings, s) == 0
print("Current settings:")
for a in dir(s):
    if a[0] == '_':
        continue
    print("\t{} = {}".format(a, getattr(s, a)))

os.close(fd)
