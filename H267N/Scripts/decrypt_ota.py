import lzma, re, struct, sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY_RE = re.compile(rb"H267N[A-Za-z0-9]{11}(?=\x00)")
TOKEN_RE = re.compile(rb"H267N\x00{1,8}([0-9a-fA-F]{11})\x00")

def aes_ecb_decrypt(data, key):
    d = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    return d.update(data) + d.finalize()

def extract(image):
    desc = 0x14 + struct.unpack_from(">I", image, 0x10)[0]
    ksize, koff, _, rsize, roff, _ = struct.unpack_from(">6I", image, desc + 0x34)
    kernel = lzma.decompress(image[koff:koff+ksize], format=lzma.FORMAT_ALONE)
    encrypted = image[roff:roff+rsize]
    candidates  = [m.group() for m in KEY_RE.finditer(kernel)]
    candidates += [b"H267N" + m.group(1)[::-1] for m in TOKEN_RE.finditer(kernel)]
    for key in candidates:
        rootfs = aes_ecb_decrypt(encrypted, key)
        if rootfs[:4] == b"hsqs":
            return rootfs

Path(sys.argv[2]).write_bytes(extract(Path(sys.argv[1]).read_bytes()))
