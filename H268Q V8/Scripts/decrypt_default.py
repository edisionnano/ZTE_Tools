import hashlib, struct, sys, zlib
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY = hashlib.sha256(b'H268QV8key').digest()
IV = hashlib.sha256(b'H268QV8IV').digest()[:16]

src = Path(sys.argv[1])
dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name(src.name + '.decrypted.xml')
blob = src.read_bytes()
plain_len, cipher_len = struct.unpack('>II', blob[0x3C:0x44])
ct = blob[0x48:0x48 + cipher_len]
d = Cipher(algorithms.AES(KEY), modes.CBC(IV)).decryptor()
inner = (d.update(ct) + d.finalize())[:plain_len]
out = bytearray()
pos = 0x3C
while pos:
    _, comp_len, nxt = struct.unpack('>III', inner[pos:pos + 12])
    out.extend(zlib.decompress(inner[pos + 12:pos + 12 + comp_len]))
    pos = nxt
dst.write_bytes(out)