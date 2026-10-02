from hashlib import md5

MAC_ADDRESS = "78-96-82-50-E5-2C"
D_SN = "268EG8JG4Q01759"
WIFI_PASSWORD = "S3sqQFXYA2KkgG5z"
ROUTER_PASSWORD = "ChNb9523"
HARDWARE_VERSION = "V1.0.0"

mac_hex = MAC_ADDRESS.replace("-", "").upper()
mac = int(mac_hex, 16)


def rec(tag, idx, data):
    return bytes([tag]) + idx.to_bytes(2, "little") + len(data).to_bytes(3, "little") + data


fields = [rec(1, i, (mac + i).to_bytes(6, "big")) for i in range(10)]
fields += [
    rec(2, 0, D_SN.encode()),
    rec(4, 0, f"COSMOTE-{mac_hex[-6:]}".encode()),
    rec(5, 16, WIFI_PASSWORD.encode()),
    rec(6, 1, b"admin"),
    rec(7, 1, ROUTER_PASSWORD.encode()),
    rec(3, 0, mac_hex[:6].encode()),
    rec(8, 6, HARDWARE_VERSION.encode()),
    rec(8, 7, b"0"),
]

print(md5(b"".join(fields)).hexdigest()[:16])