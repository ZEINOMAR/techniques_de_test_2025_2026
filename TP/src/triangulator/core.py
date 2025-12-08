"""Core triangulation logic for the Triangulator service.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from triangulator.binary import decode_point_set, encode_triangles

Point = Tuple[float, float]
Triangle = Tuple[int, int, int]


def triangulate(points: Sequence[Point]) -> List[Triangle]:
    """Renvoie une triangulation simplifiée et déterministe.

    Args:
        points: Liste de points (x, y).
    Returns:
        Liste de triangles, chaque triangle est un tuple d'indices dans `points`.
    Raises:
        ValueError: Si moins de 3 points sont fournis.
    """

    if len(points) < 3:
        raise ValueError("Moins de 3 points: non triangulable.")
    return [(0, 1, 2)]


def triangulate_data(data: bytes) -> bytes:
    """Pipeline complet : decode -> triangulate -> encode."""

    points = decode_point_set(data)
    triangles = triangulate(points)
    return encode_triangles(points, triangles)