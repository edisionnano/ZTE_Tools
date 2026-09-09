import struct
import sys
import zlib

HEADER_LEN = 0x48
TOTAL_SIZE_OFF = 0x08


def decode(data):
    total_size = struct.unpack(">I", data[TOTAL_SIZE_OFF:TOTAL_SIZE_OFF + 4])[0]
    out = b""
    pos = HEADER_LEN
    chunk_no = 0
    while len(out) < total_size and pos < len(data):
        if chunk_no > 0:
            pos += 12
        d = zlib.decompressobj()
        piece = d.decompress(data[pos:])
        piece += d.flush()
        consumed = len(data[pos:]) - len(d.unused_data)
        out += piece
        pos += consumed
        chunk_no += 1
    return out


with open(sys.argv[1], "rb") as f:
    data = f.read()
with open(sys.argv[2], "wb") as f:
    f.write(decode(data))