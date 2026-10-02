from hashlib import md5

MAC_ADDRESS = "20-E8-82-B0-94-22"
D_SN = "ZTEEG8MJ9R03647"
WIRELESS_KEY = "5Qh43g5Xaz"
PASSWORD = "KdfNx75h"
HARDWARE_VERSION = "V1.1.0"

mac_hex = MAC_ADDRESS.replace("-", "").upper()
mac = int(mac_hex, 16)


def rec(tag, idx, data):
    return bytes([tag]) + idx.to_bytes(2, "little") + len(data).to_bytes(3, "little") + data


fields = [rec(1, i, (mac + i).to_bytes(6, "big")) for i in range(4)]
fields += [
    rec(2, 0, D_SN.encode()),
    rec(4, 0, f"WIND_2.4G_{mac_hex[-6:]}".encode()),
    rec(5, 16, WIRELESS_KEY.encode()),
    rec(6, 1, b"admin"),
    rec(7, 1, PASSWORD.encode()),
    rec(3, 0, b"309935"),
    rec(8, 6, HARDWARE_VERSION.encode()),
    rec(8, 7, b"0"),
]

print(md5(b"".join(fields)).hexdigest()[:16])
