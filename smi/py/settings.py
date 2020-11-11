import ctypes
import fcntl
import os
import struct


# 0: 8 bit, 1: 16 bit, 2: 9 bit, 3: 18 bit
data_width = 0

fn = '/dev/smi'

fd = os.open(fn, os.O_RDWR)

_io = lambda a, b: a << 8 | b

magic = 0x01

get_settings = _io(magic, 0)
set_settings = _io(magic, 1)
address = _io(magic, 2)

# set address
settings = [
    # 0: 8 bit, 1: 16 bit, 2: 9 bit, 3: 18 bit
    ('data_width', ctypes.c_int),
    # pack multiple smi transfers into 1 32-bit FIFO work?
    ('pack_data', ctypes.c_bool),
    # Timing for reads (writes the same but for WE)
    # 
    # OE ----------+          +--------------------
    #              |          |
    #              +----------+
    # SD -<==============================>-----------
    # SA -<=========================================>-
    #    <-setup->  <-strobe ->  <-hold ->  <- pace ->
    # 
    # pre OE data assert time
    ('read_setup_time', ctypes.c_int),
    # post OE data assert time
    ('read_hold_time', ctypes.c_int),
    # post OE (and hold) address assert time
    ('read_pace_time', ctypes.c_int),
    # OE assert time
    ('read_strobe_time', ctypes.c_int),
    # see above
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


def print_settings(s):
    for a in dir(s):
        if a[0] == '_':
            continue
        print("\t{} = {}".format(a, getattr(s, a)))


s = Settings()
assert fcntl.ioctl(fd, get_settings, s) == 0
print("Current settings:")
print_settings(s)

print(f"Setting data width to {data_width}")
s.data_width = data_width
print(fcntl.ioctl(fd, set_settings, s))

assert fcntl.ioctl(fd, get_settings, s) == 0
print("New settings:")
print_settings(s)

os.close(fd)
