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
    #('pack_data', ctypes.c_bool),
    ('pack_data', ctypes.c_int),
    ('read_setup_time', ctypes.c_int),
    ('read_hold_time', ctypes.c_int),
    ('read_pace_time', ctypes.c_int),
    ('read_strobe_time', ctypes.c_int),
    ('write_setup_time', ctypes.c_int),
    ('write_hold_time', ctypes.c_int),
    ('write_pace_time', ctypes.c_int),
    ('write_strobe_time', ctypes.c_int),
    #('dma_enable', ctypes.c_bool),
    ('dma_enable', ctypes.c_int),
    #('dma_passthrough_enable', ctypes.c_bool),
    ('dma_passthrough_enable', ctypes.c_int),
    ('dma_read_thresh', ctypes.c_int),
    ('dma_write_thresh', ctypes.c_int),
    ('dma_panic_read_thresh', ctypes.c_int),
    ('dma_panic_write_thresh', ctypes.c_int),
]
nbytes = sum([ctypes.sizeof(i[1]) for i in settings])
ba = bytearray([0] * nbytes)
print(fcntl.ioctl(fd, get_settings, ba))
#print(ba)
# convert ba to settings
i = 0
for s in settings:
    n, t = s
    nb = ctypes.sizeof(t)
    bs = ba[i:i+nb]
    if t == ctypes.c_int:
        v = struct.unpack('i', bs)[0]
    elif t == ctypes.c_bool:
        v = struct.unpack('?', bs)[0]
    else:
        raise Exception("unknown type")
    # TODO struct unpacking
    print("{}: {}[{}]".format(n, v, bs))
    i += nb
fcntl.ioctl(fd, address, 0b100000)
# write some data
#os.write(fd, b'\xaa\xaa\x55\x55')
#os.write(fd, b'\x00\x01\x00\x00')
os.write(fd, b'\x01\x00')
# read some data
print(os.read(fd, 4))
os.close(fd)
