import struct
import sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY = b'H108Necba16149bf'

def main():
    data = Path(sys.argv[1]).read_bytes()
    _, _, _, fs, fo, _ = struct.unpack_from('>6I', data, 0x48)
    fs_packed = data[fo:fo + fs]
    if fs_packed[:4] != b'hsqs':
        cipher = Cipher(algorithms.AES(KEY), modes.ECB()).decryptor()
        fs_packed = cipher.update(fs_packed) + cipher.finalize()
    Path(sys.argv[2]).write_bytes(data[:fo] + fs_packed + data[fo + fs:])

if __name__ == '__main__':
    main()