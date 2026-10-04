import struct, sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

d = open(sys.argv[1], "rb").read()
size, off = struct.unpack_from(">2I", d, 0x7c)
size -= size % 16
aes = Cipher(algorithms.AES(b"H288AV1112312312"), modes.ECB()).decryptor()
open(sys.argv[2], "wb").write(d[:off] + aes.update(d[off:off + size]) + d[off + size:])