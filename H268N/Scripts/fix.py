import struct, sys

W = bytearray(128)
W[0:16] = bytes.fromhex('999999994444444455555555aaaaaaaa')
W[0x1b] = 0x04
W[0x3f] = 0x40
W[0x41] = 0x02
W[0x47] = 0x80

inner = open(sys.argv[1], 'rb').read()
struct.pack_into('>I', W, 0x48, len(inner))
open(sys.argv[2], 'wb').write(bytes(W) + inner)