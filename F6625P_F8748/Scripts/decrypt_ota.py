import struct, pathlib, sys, hashlib
from Crypto.Cipher import AES

raw = pathlib.Path(sys.argv[1]).read_bytes()
start = struct.unpack_from('<I', raw, 0x14c)[0]
end   = struct.unpack_from('<I', raw, 0x158)[0]
key   = hashlib.sha256(b'PONGV9.020200309').digest()[8:24]
pathlib.Path(sys.argv[2]).write_bytes(AES.new(key, AES.MODE_ECB).decrypt(raw[start:end]))