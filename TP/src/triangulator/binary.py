"""Encodeur et décodeur binaire pour les structures PointSet et Triangles."""

import struct


def encode_point_set(points):
    """Encode une liste de points 2D dans le format binaire PointSet.

    Format :
    - 4 octets : nombre de points (entier non signé)
    - N × 8 octets : coordonnées (x, y) de chaque point en flottants

    Args:
        points (list[tuple[float, float]]): Liste des points (x, y).

    Returns:
        bytes: Données binaires représentant le PointSet.

    """
    data = struct.pack("<I", len(points))

    for x, y in points:
        data += struct.pack("<ff", float(x), float(y))

    return data


def decode_point_set(data):
    """Décode des données binaires PointSet en une liste de points 2D.

    Args:
        data (bytes): Données binaires au format PointSet.

    Returns:
        list[tuple[float, float]]: Liste des points décodés.

    Raises:
        ValueError: Si le buffer est trop court ou incohérent.

    """
    if len(data) < 4:
        raise ValueError("Buffer trop court pour un PointSet")

    (n_points,) = struct.unpack("<I", data[:4])
    expected_length = 4 + n_points * 8

    if len(data) != expected_length:
        raise ValueError("Longueur binaire invalide pour un PointSet")

    points = []
    offset = 4

    for _ in range(n_points):
        x, y = struct.unpack("<ff", data[offset:offset + 8])
        points.append((x, y))
        offset += 8

    return points


def encode_triangles(vertices, triangles):
    """Encode les sommets et les triangles d'une triangulation en binaire.

    Format :
    - PointSet des sommets
    - 4 octets : nombre de triangles
    - T × 12 octets : indices (i, j, k) des sommets

    Args:
        vertices (list[tuple[float, float]]): Sommets 2D.
        triangles (list[tuple[int, int, int]]): Indices des triangles.

    Returns:
        bytes: Données binaires de la triangulation.

    """
    data = encode_point_set(vertices)
    data += struct.pack("<I", len(triangles))

    for i, j, k in triangles:
        data += struct.pack("<III", int(i), int(j), int(k))

    return data


def decode_triangles(data):
    """Décode des données binaires de triangulation.

    Args:
        data (bytes): Données binaires contenant sommets et triangles.

    Returns:
        tuple:
            - vertices (list[tuple[float, float]])
            - triangles (list[tuple[int, int, int]])

    Raises:
        ValueError: Si le buffer est invalide ou incomplet.

    """
    if len(data) < 4:
        raise ValueError("Buffer trop court pour une triangulation")

    (n_points,) = struct.unpack("<I", data[:4])
    pointset_size = 4 + n_points * 8

    if len(data) < pointset_size:
        raise ValueError("Données insuffisantes pour les sommets")

    vertices = decode_point_set(data[:pointset_size])
    offset = pointset_size

    if len(data) < offset + 4:
        raise ValueError("Données insuffisantes pour l'en-tête des triangles")

    (n_triangles,) = struct.unpack("<I", data[offset:offset + 4])
    offset += 4

    expected_length = offset + n_triangles * 12

    if len(data) != expected_length:
        raise ValueError("Longueur invalide pour les triangles")

    triangles = []

    for _ in range(n_triangles):
        i, j, k = struct.unpack("<III", data[offset:offset + 12])
        triangles.append((i, j, k))
        offset += 12

    return vertices, triangles