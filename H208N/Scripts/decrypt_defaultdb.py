import sys, struct, zlib
from io import BytesIO
from hashlib import sha256
from Crypto.Cipher import AES

data = open(sys.argv[1], 'rb').read()

dec_size = int.from_bytes(data[0x3c:0x40], 'big')
chunk_size = int.from_bytes(data[0x40:0x44], 'big')
ct = data[0x48:0x48 + chunk_size]

key = sha256(b"H108N_V2.5_16X32_key").digest()
iv = sha256(b"H108N_V2.5_16X32_IV").digest()[:16]

buf = BytesIO(AES.new(key, AES.MODE_CBC, iv).decrypt(ct)[:dec_size])
buf.seek(60)

out = BytesIO()
while True:
    hdr = buf.read(12)
    if len(hdr) < 12:
        break
    d_len, c_len, more = struct.unpack(">3I", hdr)
    out.write(zlib.decompress(buf.read(c_len)))
    if more == 0:
        break

open(sys.argv[2], 'wb').write(out.getvalue())