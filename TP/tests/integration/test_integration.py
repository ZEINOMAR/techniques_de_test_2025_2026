"""Tests d'intégration du flux complet Triangulator.

Vérifie l'interaction entre le client PSM, le module binaire et
le cœur de triangulation.
"""

import pytest

from triangulator import binary, client_psm, core


def test_integration_psm_unavailable():
    """Teste la gestion de l'indisponibilité du PointSetManager.

    Vérifie que l'appel à get_pointset_bytes lève une exception
    PointSetManagerUnavailable lorsque le service est indisponible.
    """
    with pytest.raises(client_psm.PointSetManagerUnavailable):
        client_psm.get_pointset_bytes("any-id")


def test_integration_psm_to_binary_success(monkeypatch):
    """Teste la récupération et la décodification réussie d'un PointSet.

    Simule la récupération d'un PointSet encodé en bytes via le client PSM,
    puis vérifie que la décodification binaire restitue correctement les points.
    """
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
    """Teste la gestion d'une donnée binaire corrompue.

    Simule la récupération d'un flux binaire corrompu et vérifie que
    la tentative de décodage lève une exception ValueError.
    """
    corrupt = b"\x03\x00\x00\x00" + b"\x00\x00\x00\x00"

    monkeypatch.setattr(
        "triangulator.client_psm.get_pointset_bytes",
        lambda _id: corrupt
    )

    with pytest.raises(ValueError):
        data = client_psm.get_pointset_bytes("id")
        binary.decode_point_set(data)


def test_integration_full_pointset_to_triangles(monkeypatch):
    """Teste le flux complet de récupération à triangulation.

    Depuis la récupération simulée d'un PointSet encodé, sa décodification
    puis la triangulation, vérifie que le résultat est conforme.
    """
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

    assert sorted(triangles[0]) == [0, 1, 2]


def test_integration_triangulation_failure_propagates(monkeypatch):
    """Vérifie la propagation d'une erreur de triangulation sur un PointSet invalide.

    Simule un PointSet non triangulable (2 points) et vérifie que la triangulation
    lève une exception ValueError.
    """
    pts = [(0.0, 0.0), (1.0, 0.0)]
    encoded = binary.encode_point_set(pts)

    monkeypatch.setattr(
        "triangulator.client_psm.get_pointset_bytes",
        lambda _id: encoded,
    )

    received = client_psm.get_pointset_bytes("any-id")
    decoded = binary.decode_point_set(received)

    with pytest.raises(ValueError):
        core.triangulate(decoded)
