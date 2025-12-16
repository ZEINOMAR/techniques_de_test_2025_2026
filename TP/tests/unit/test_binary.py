"""Tests unitaires du module de sérialisation binaire (PointSet et Triangles)."""

import math

import pytest

from triangulator import binary


def test_encode_point_set_basic():
    """Vérifie que l'encodage d'un ensemble de points produit le bon format binaire."""
    pts = [(1.0, 2.0), (3.0, 4.0)]
    data = binary.encode_point_set(pts)

    assert data[:4] == b"\x02\x00\x00\x00"
    assert len(data) == 4 + 2 * 8  


def test_encode_decode_roundtrip():
    """Vérifie l'encodage puis le décodage d'un ensemble de points.

    Les valeurs décodées doivent correspondre aux valeurs initiales,
    à une tolérance flottante près.
    """
    pts = [(0.0, 0.0), (1.5, -2.25), (3.14, 6.28)]
    encoded = binary.encode_point_set(pts)
    decoded = binary.decode_point_set(encoded)

    for (dx, dy), (x, y) in zip(decoded, pts):
        assert math.isclose(dx, x, rel_tol=1e-6, abs_tol=1e-6)
        assert math.isclose(dy, y, rel_tol=1e-6, abs_tol=1e-6)


def test_decode_invalid_too_short():
    """Vérifie que le décodage échoue si le buffer est trop court.

    Le buffer ne contient pas suffisamment d'octets pour lire la taille.
    """
    with pytest.raises(ValueError):
        binary.decode_point_set(b"\x01\x00\x00")  


def test_decode_wrong_length():
    """Vérifie que le décodage détecte une longueur incohérente."""
    corrupted = b"\x02\x00\x00\x00" + b"\x00" * 12  

    with pytest.raises(ValueError):
        binary.decode_point_set(corrupted)


def test_decode_valid_float_values():
    """Vérifie que la décodage restitue correctement les valeurs flottantes encodées."""
    pts = [(1.25, -3.5), (10.0, 0.001)]
    data = binary.encode_point_set(pts)
    decoded = binary.decode_point_set(data)

    for (dx, dy), (x, y) in zip(decoded, pts):
        assert math.isclose(dx, x, rel_tol=1e-6, abs_tol=1e-6)
        assert math.isclose(dy, y, rel_tol=1e-6, abs_tol=1e-6)


def test_encode_decode_triangles_roundtrip():
    """Vérifie qu'on peut encoder puis décoder des triangles sans perte de données."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]
    
    data = binary.encode_triangles(points, triangles)
    
    decoded_pts, decoded_tris = binary.decode_triangles(data)
    
    assert decoded_tris == triangles
    assert len(decoded_pts) == 3
    assert decoded_pts[0] == (0.0, 0.0)


def test_decode_triangles_invalid_length():
    """Vérifie la robustesse du décodage face à un buffer tronqué."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]
    data = binary.encode_triangles(points, triangles)
    
    corrupted_data = data[:-1] 
    
    with pytest.raises(ValueError):
        binary.decode_triangles(corrupted_data)


def test_decode_triangles_header_too_short():
    """Teste l'échec du décodage si l'en-tête est incomplet."""
    with pytest.raises(ValueError):
        from triangulator import binary
        binary.decode_triangles(b"\x00\x00")


def test_decode_triangles_body_too_short_for_points():
    """Teste l'échec du décodage si les points annoncés sont incomplets."""
    from triangulator import binary
    data = b"\x01\x00\x00\x00" + b"\x00\x00"
    with pytest.raises(ValueError):
        binary.decode_triangles(data)


def test_decode_triangles_corrupt_triangle_section():
    """Teste que le décodage détecte un buffer tronqué dans la section des triangles."""
    from triangulator import binary
    points = [(0.0, 0.0)]
    triangles = [(0, 0, 0)]
    data = binary.encode_triangles(points, triangles)
    
    corrupt_data = data[:-1]
    
    with pytest.raises(ValueError):
        binary.decode_triangles(corrupt_data)


def test_decode_triangles_extra_bytes():
    """Teste le rejet de données supplémentaires en fin de buffer."""
    from triangulator import binary
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]
    data = binary.encode_triangles(points, triangles)
    
    corrupted_data = data + b"\x00"
    
    with pytest.raises(ValueError, match="Longueur invalide"):
        binary.decode_triangles(corrupted_data)