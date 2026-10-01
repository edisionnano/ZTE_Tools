import struct, sys, zlib, hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def chunks(d):
    p = 60
    while True:
        _, n, more = struct.unpack(">3I", d[p:p+12])
        yield d[p+12:p+12+n]
        p += 12 + n
        if not more:
            return

def decode(data):
    key = hashlib.sha256(b"CHIP_RTL8676_KEY").digest()
    iv = hashlib.sha256(b"CHIP_RTL8676_IV").digest()[:16]
    c = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    inner = c.update(b"".join(chunks(data))) + c.finalize()
    return b"".join(zlib.decompress(x) for x in chunks(inner))

open(sys.argv[2], "wb").write(decode(open(sys.argv[1], "rb").read()))
