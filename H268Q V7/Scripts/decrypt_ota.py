import lzma
import re
import struct
import sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

data = Path(sys.argv[1]).read_bytes()
ks, ko, _, fs, fo, _ = struct.unpack_from(">6I", data, 0x70)
kernel = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE).decompress(data[ko:ko + ks])

for token in re.findall(rb"H268Q\x00{1,8}([0-9a-fA-F]{11})\x00", kernel):
    key = b"H268Q" + token[::-1]
    d = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    rootfs = d.update(data[fo:fo + fs]) + d.finalize()
    if rootfs[:4] == b"hsqs":
        Path(sys.argv[2]).write_bytes(rootfs)
        break