import lzma, re, subprocess, sys

MAGIC = bytes.fromhex("999999994444444455555555aaaaaaaa")

def u32(d, o):
    return int.from_bytes(d[o:o + 4], "big")

src = sys.argv[1]
dst = sys.argv[2] if len(sys.argv) > 2 else src + ".dec"

data = bytearray(open(src, "rb").read())

pos = data.find(MAGIC)
while pos >= 0:
    ksize, koff = u32(data, pos + 0x70), u32(data, pos + 0x74)
    rsize, roff = u32(data, pos + 0x7C), u32(data, pos + 0x80)

    kernel = lzma.decompress(bytes(data[pos + koff:pos + koff + ksize]), format=lzma.FORMAT_ALONE)
    build_id = re.search(rb"H1600\x00+([0-9A-Fa-f]{11})\x00", kernel).group(1).decode().lower()
    key = ("H1600" + build_id[::-1]).encode().hex()

    start, end = pos + roff, pos + roff + rsize
    data[start:end] = subprocess.run(
        ["openssl", "enc", "-aes-128-ecb", "-d", "-K", key, "-nopad"],
        input=bytes(data[start:end]), stdout=subprocess.PIPE, check=True,
    ).stdout

    pos = data.find(MAGIC, pos + len(MAGIC))

open(dst, "wb").write(data)