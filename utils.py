import struct

VERBOSE = False

def set_verbose(v):
    global VERBOSE
    VERBOSE = v

def hexdump_iter(data, address=0):
    for i in range(0, len(data), 16):
        row = data[i:i+16]
        hex_dump = ' '.join('%.2x' % i for i in row).ljust(3*16-1)
        char_dump = ''.join(chr(i) if 0x20 <= i <= 0x7e else '.' for i in row).ljust(16)
        yield '%.8x: %s  %s' % (i + address, hex_dump, char_dump)

def hexdump(data, address=0):
    for line in hexdump_iter(data, address):
        print(line)

def ru32(fp):
    pos = fp.tell()
    data = fp.read(4)
    if VERBOSE:
        hexdump(data, pos)
    return struct.unpack('<I', data)[0]

def ri32(fp):
    pos = fp.tell()
    data = fp.read(4)
    if VERBOSE:
        hexdump(data, pos)
    return struct.unpack('<i', data)[0]

def rblob(fp, elemsize=1, dump=False):
    size = ru32(fp)
    pos = fp.tell()
    data = fp.read(size * elemsize)
    if VERBOSE or dump:
        hexdump(data, pos)
    return data

def riarr(fp, dump=False):
    b = rblob(fp, 4, dump)
    ret = []
    for i in range(0, len(b), 4):
        ret.append(struct.unpack('<i', b[i:i+4])[0])
    return ret

def rstr(fp, encoding='shift-jis'):
    pos = fp.tell()
    data = rblob(fp)
    assert data[-1] == 0
    try:
        return data[:-1].decode(encoding)
    except Exception as e:
        #print('ERRDECODE', e)
        #hexdump(data, pos + 4)
        return data
