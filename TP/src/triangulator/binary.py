"""Binary encoder/decoder for PointSet data."""

import struct


def encode_point_set(points):
    """Encode a list of (x, y) into binary format."""
    data = struct.pack("<I", len(points))
    for x, y in points:
        data += struct.pack("<ff", float(x), float(y))
    return data


def decode_point_set(data):
    """Decode binary PointSet into Python list of tuples."""
    if len(data) < 4:
        raise ValueError("Buffer too short")

    n = struct.unpack("<I", data[:4])[0]
    expected_length = 4 + n * 8

    if len(data) != expected_length:
        raise ValueError("Invalid length")

    points = []
    offset = 4
    for _ in range(n):
        x, y = struct.unpack("<ff", data[offset:offset + 8])
        points.append((x, y))
        offset += 8

    return points
