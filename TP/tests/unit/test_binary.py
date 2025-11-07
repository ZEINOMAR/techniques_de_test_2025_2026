from src.triangulator import binary

def test_encode_decode_point_set_roundtrip():
    pts = [(0.0, 0.0), (1.0, 0.5), (-2.0, 3.0)]
    assert binary.decode_point_set(binary.encode_point_set(pts)) == pts
