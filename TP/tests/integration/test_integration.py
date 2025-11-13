import pytest
from src.triangulator import client_psm, binary


def test_integration_psm_unavailable():
    with pytest.raises(client_psm.PointSetManagerUnavailable):
        client_psm.get_pointset_bytes("any-id")


def test_integration_psm_to_binary_success(monkeypatch):
    pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    encoded = binary.encode_point_set(pts)

    monkeypatch.setattr(
        "src.triangulator.client_psm.get_pointset_bytes",
        lambda _id: encoded
    )

    received = client_psm.get_pointset_bytes("fake-id")
    decoded = binary.decode_point_set(received)

    assert decoded == pts


def test_integration_binary_failure(monkeypatch):
    corrupt = b"\x03\x00\x00\x00" + b"\x00\x00\x00\x00"  

    monkeypatch.setattr(
        "src.triangulator.client_psm.get_pointset_bytes",
        lambda _id: corrupt
    )

    with pytest.raises(ValueError):
        data = client_psm.get_pointset_bytes("id")
        binary.decode_point_set(data)
