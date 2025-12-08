"""Binary encoder/decoder for PointSet and Triangles data."""

import struct


# ------------------------------------------------------------
#  POINT SET (vertices)
# ------------------------------------------------------------

def encode_point_set(points):
    """
    Encode a list of (x, y) points into the PointSet binary format.

    Format:
        - 4 bytes: unsigned int (N, number of points)
        - N * 8 bytes: each point as (float32, float32)
    """

    data = struct.pack("<I", len(points))  # number of points

    for x, y in points:
        data += struct.pack("<ff", float(x), float(y))  # 2x float32 = 8 bytes

    return data


def decode_point_set(data):
    """
    Decode PointSet binary format into list of (x, y).

    Raises:
        ValueError if buffer too short or invalid length.
    """

    if len(data) < 4:
        raise ValueError("Buffer too short for PointSet header")

    (n_points,) = struct.unpack("<I", data[:4])
    expected_length = 4 + n_points * 8  # each point = 8 bytes

    if len(data) != expected_length:
        raise ValueError("Invalid PointSet binary length")

    points = []
    offset = 4

    for _ in range(n_points):
        x, y = struct.unpack("<ff", data[offset:offset + 8])
        points.append((x, y))
        offset += 8

    return points


# ------------------------------------------------------------
#  TRIANGLES (vertices + triangle indices)
# ------------------------------------------------------------

def encode_triangles(vertices, triangles):
    """
    Encode triangulation result:
    Part 1: vertices in PointSet format (float32)
    Part 2:
        - 4 bytes: unsigned int T (#triangles)
        - T * 12 bytes: each triangle (i, j, k) as 3x uint32
    """

    # Encode vertices using existing function
    data = encode_point_set(vertices)

    # Append number of triangles
    data += struct.pack("<I", len(triangles))

    # Append each triangle indices
    for i, j, k in triangles:
        data += struct.pack("<III", int(i), int(j), int(k))

    return data


def decode_triangles(data):
    """
    Decode binary triangulation buffer into:
        vertices: list[(float, float)]
        triangles: list[(int, int, int)]
    """

    # Decode vertices first
    vertices = decode_point_set(data)
    offset = 4 + len(vertices) * 8  # header + vertices

    if len(data) < offset + 4:
        raise ValueError("Buffer too short for triangles header")

    (n_tris,) = struct.unpack("<I", data[offset:offset + 4])
    offset += 4

    expected_length = offset + n_tris * 12  # each triangle = 12 bytes

    if len(data) != expected_length:
        raise ValueError("Invalid length for triangles section")

    triangles = []

    for _ in range(n_tris):
        i, j, k = struct.unpack("<III", data[offset:offset + 12])
        triangles.append((i, j, k))
        offset += 12

    return vertices, triangles