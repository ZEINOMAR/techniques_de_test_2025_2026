import pytest
from triangulator import client_psm, binary, core


def test_integration_psm_unavailable():
    with pytest.raises(client_psm.PointSetManagerUnavailable):
        client_psm.get_pointset_bytes("any-id")


def test_integration_psm_to_binary_success(monkeypatch):
    pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    encoded = binary.encode_point_set(pts)

    monkeypatch.setattr(
        "triangulator.client_psm.get_pointset_bytes",
        lambda _id: encoded
    )

    received = client_psm.get_pointset_bytes("fake-id")
    decoded = binary.decode_point_set(received)

    assert decoded == pts


def test_integration_binary_failure(monkeypatch):
    corrupt = b"\x03\x00\x00\x00" + b"\x00\x00\x00\x00"  

    monkeypatch.setattr(
        "triangulator.client_psm.get_pointset_bytes",
        lambda _id: corrupt
    )

    with pytest.raises(ValueError):
        data = client_psm.get_pointset_bytes("id")
        binary.decode_point_set(data)


def test_integration_full_pointset_to_triangles(monkeypatch):
    """Flux complet: PSM stub -> encode/decode -> triangulation."""
    pts = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    encoded = binary.encode_point_set(pts)

    monkeypatch.setattr(
        "triangulator.client_psm.get_pointset_bytes",
        lambda _id: encoded,
    )

    received = client_psm.get_pointset_bytes("any-id")
    decoded = binary.decode_point_set(received)
    triangles = core.triangulate(decoded)

    assert decoded == pts
    assert len(triangles) == 1
    assert triangles[0] == (0, 1, 2)


def test_integration_triangulation_failure_propagates(monkeypatch):
    """Vérifie que l'erreur de triangulation est propagée sur un PointSet invalide."""
    pts = [(0.0, 0.0), (1.0, 0.0)]  # seulement 2 points -> non triangulable
    encoded = binary.encode_point_set(pts)

    monkeypatch.setattr(
        "triangulator.client_psm.get_pointset_bytes",
        lambda _id: encoded,
    )

    received = client_psm.get_pointset_bytes("any-id")
    decoded = binary.decode_point_set(received)

    with pytest.raises(ValueError):
        core.triangulate(decoded)
