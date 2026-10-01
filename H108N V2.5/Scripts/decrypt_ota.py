import lzma, re, struct, sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

data = Path(sys.argv[1]).read_bytes()
ks, ko, _, fs, fo, _ = struct.unpack_from('>6I', data, 0x48)
kernel = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE).decompress(data[ko:ko + ks])

for t in re.findall(rb'H108N\x00{1,8}([0-9a-fA-F]{11})\x00', kernel):
    d = Cipher(algorithms.AES(b'H108N' + t[::-1]), modes.ECB()).decryptor()
    rootfs = d.update(data[fo:fo + fs]) + d.finalize()
    if rootfs[:4] == b'hsqs':
        break

Path(sys.argv[2]).write_bytes(data[:fo] + rootfs + data[fo + fs:])
