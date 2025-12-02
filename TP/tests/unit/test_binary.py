import pytest
import math
from triangulator import binary


def test_encode_point_set_basic():
    pts = [(1.0, 2.0), (3.0, 4.0)]
    data = binary.encode_point_set(pts)

    assert data[:4] == b"\x02\x00\x00\x00"
    assert len(data) == 4 + 2 * 8  


def test_encode_decode_roundtrip():
    pts = [(0.0, 0.0), (1.5, -2.25), (3.14, 6.28)]
    encoded = binary.encode_point_set(pts)
    decoded = binary.decode_point_set(encoded)

    for (dx, dy), (x, y) in zip(decoded, pts):
        assert math.isclose(dx, x, rel_tol=1e-6, abs_tol=1e-6)
        assert math.isclose(dy, y, rel_tol=1e-6, abs_tol=1e-6)


def test_decode_invalid_too_short():
    with pytest.raises(ValueError):
        binary.decode_point_set(b"\x01\x00\x00")  


def test_decode_wrong_length():
    corrupted = b"\x02\x00\x00\x00" + b"\x00" * 12  

    with pytest.raises(ValueError):
        binary.decode_point_set(corrupted)


def test_decode_valid_float_values():
    pts = [(1.25, -3.5), (10.0, 0.001)]
    data = binary.encode_point_set(pts)
    decoded = binary.decode_point_set(data)

    for (dx, dy), (x, y) in zip(decoded, pts):
        assert math.isclose(dx, x, rel_tol=1e-6, abs_tol=1e-6)
        assert math.isclose(dy, y, rel_tol=1e-6, abs_tol=1e-6)
