import re
import struct
import sys
import zlib
import lzma
from pathlib import Path

from Crypto.Cipher import AES

KEY_RE = re.compile(rb"H268[A-Za-z0-9]{12}", re.IGNORECASE)
JFFS2_MAGIC = b"\x19\x85"


def jffs2_crc(data):
    return zlib.crc32(data, 0xFFFFFFFF) ^ 0xFFFFFFFF


def valid_jffs2_node(buf, pos):
    if pos + 12 > len(buf) or buf[pos:pos + 2] != JFFS2_MAGIC:
        return None
    _, node_type, total_len, stored_crc = struct.unpack_from(">HHII", buf, pos)
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
    return AES.new(key, AES.MODE_ECB).decrypt(data)

def lzma_candidates(image):
    n = len(image)
    cands = set()

    p = image.find(b"\x00\x00\x00\x00")
    while p >= 0:
        off = p - 9
        if 0 <= off <= n - 13 and image[off] <= 224 and image[off + 4] <= 0x10:
            lo = int.from_bytes(image[off + 5:off + 9], "little")
            if lo == 0 or 0x40000 <= lo <= 0x10000000:
                cands.add(off)
        p = image.find(b"\x00\x00\x00\x00", p + 1)

    p = image.find(b"\xff" * 8)
    while p >= 0:
        off = p - 5
        if 0 <= off <= n - 13 and image[off] <= 224:
            cands.add(off)
        p = image.find(b"\xff" * 8, p + 8)

    return cands


def lzma_blobs(image):
    mv = memoryview(image)
    blobs = []
    for off in sorted(lzma_candidates(image)):
        try:
            blob = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE).decompress(
                mv[off:off + 0x400000], 0x800000
            )
        except lzma.LZMAError:
            continue
        if len(blob) >= 0x80000:
            blobs.append(blob)
    return blobs


def find_keys(image):
    keys = []
    for blob in [image] + lzma_blobs(image):
        for m in KEY_RE.finditer(blob):
            if m.group() not in keys:
                keys.append(m.group())
    return keys


def find_rootfs_offset(image, key):
    mv = memoryview(image)
    n = len(image)
    for phase in range(16):
        ln = (n - phase) // 16 * 16
        plain = decrypt_ecb(mv[phase:phase + ln], key)
        pos = 0
        while (hit := plain.find(JFFS2_MAGIC, pos)) >= 0:
            if verify_node_run(plain, hit):
                return phase + hit
            pos = hit + 1
    return None


def main():
    src = Path(sys.argv[1])
    image = src.read_bytes()
    keys = find_keys(image)
    for key in keys:
        off = find_rootfs_offset(image, key)
        if off is not None:
            ln = (len(image) - off) // 16 * 16
            out = src.with_suffix(".rootfs.jffs2")
            out.write_bytes(decrypt_ecb(image[off:off + ln], key))
            return


if __name__ == "__main__":
    main()