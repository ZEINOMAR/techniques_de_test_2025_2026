import struct

def encode_point_set(points):
    data = struct.pack("<I", len(points))
    for x, y in points:
        data += struct.pack("<ff", float(x), float(y))
    return data

def decode_point_set(data):
    if len(data) < 4:
        raise ValueError("Buffer trop court")
    n = struct.unpack("<I", data[:4])[0]
    expected = 4 + n*8
    if len(data) != expected:
        raise ValueError("Longueur invalide")
    out = []
    off = 4
    for _ in range(n):
        x, y = struct.unpack("<ff", data[off:off+8])
        out.append((x, y))
        off += 8
    return out
