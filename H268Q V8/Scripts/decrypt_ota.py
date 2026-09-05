import re
import struct
import sys
import zlib
from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

TOKEN_RE = re.compile(rb"H268Q[A-Za-z0-9]{11}")
JFFS2_MAGIC = b"\x85\x19"


def jffs2_crc(data):
    return (zlib.crc32(data, 0xFFFFFFFF) ^ 0xFFFFFFFF) & 0xFFFFFFFF


def valid_jffs2_node(buf, pos):
    if pos + 12 > len(buf) or buf[pos:pos + 2] != JFFS2_MAGIC:
        return None
    _, node_type, total_len, stored_crc = struct.unpack_from("<HHII", buf, pos)
    if not (node_type & 0x2000) or not (12 <= total_len <= 16 * 1024 * 1024):
        return None
    if jffs2_crc(buf[pos:pos + 8]) != stored_crc:
        return None
    return total_len


def verify_node_run(buf, start, minimum=3):
    pos = start
    for _ in range(minimum):
        total_len = valid_jffs2_node(buf, pos)
        if total_len is None:
            return False
        pos = (pos + total_len + 3) & ~3
    return True


def decrypt_ecb(data, key):
    dec = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    return dec.update(data) + dec.finalize()


def find_rootfs_offset(image, key):
    for phase in range(16):
        n = (len(image) - phase) // 16 * 16
        plain = decrypt_ecb(image[phase:phase + n], key)
        pos = 0
        while (hit := plain.find(JFFS2_MAGIC, pos)) >= 0:
            if verify_node_run(plain, hit):
                return phase + hit
            pos = hit + 1


def extract_rootfs(firmware_path):
    firmware_path = Path(firmware_path)
    image = firmware_path.read_bytes()
    key = TOKEN_RE.search(image).group()
    offset = find_rootfs_offset(image, key)
    n = (len(image) - offset) // 16 * 16
    rootfs = decrypt_ecb(image[offset:offset + n], key)
    out = firmware_path.with_suffix(".rootfs.jffs2")
    out.write_bytes(rootfs)
    return out


if __name__ == "__main__":
    extract_rootfs(sys.argv[1])
