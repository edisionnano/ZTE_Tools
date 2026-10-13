import struct
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Thanks to rajkosto for finding the key in the bootloader
KEY = "pkq_lsw20160407".ljust(16, "\0").encode()

data = open(sys.argv[1], "rb").read()
desc = 0x14 + struct.unpack_from(">I", data, 0x10)[0]
rootfs_length = struct.unpack_from(">I", data, desc + 0x40)[0]
rootfs_offset = struct.unpack_from(">I", data, desc + 0x44)[0]
rootfs_end = rootfs_offset + rootfs_length
decryptor = Cipher(algorithms.AES(KEY), modes.ECB()).decryptor()
plain = decryptor.update(data[rootfs_offset:rootfs_end]) + decryptor.finalize()

open(sys.argv[2], "wb").write(data[:rootfs_offset] + plain + data[rootfs_end:])