"""Logique cœur du service Triangulator.

Ce module implémente une triangulation de points 2D basée sur
l’algorithme de Bowyer-Watson (triangulation de Delaunay).
Il fournit :
- la triangulation à partir d’une liste de points,
- un pipeline complet binaire (décodage → triangulation → encodage).
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from triangulator.binary import decode_point_set, encode_triangles

Point = Tuple[float, float]
Triangle = Tuple[int, int, int]


def _distance_sq(p1: Point, p2: Point) -> float:
    """Compute the squared Euclidean distance between two points.

    This helper avoids using a square root for performance reasons.
    """
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2


def _circumcircle_contains(
    tri_indices: Triangle,
    point: Point,
    points: List[Point],
) -> bool:
    """Détermine si un point appartient au cercle circonscrit d’un triangle.

    Args:
        tri_indices: Indices des sommets du triangle.
        point: Point à tester.
        points: Liste complète des points.

    Returns:
        True si le point est strictement à l’intérieur du cercle circonscrit,
        False sinon.

    """
    p1 = points[tri_indices[0]]
    p2 = points[tri_indices[1]]
    p3 = points[tri_indices[2]]

    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    
    if abs(d) < 1e-9:
        return False

    ux = (
        (ax**2 + ay**2) * (by - cy)
        + (bx**2 + by**2) * (cy - ay)
        + (cx**2 + cy**2) * (ay - by)
    ) / d
    uy = (
        (ax**2 + ay**2) * (cx - bx)
        + (bx**2 + by**2) * (ax - cx)
        + (cx**2 + cy**2) * (bx - ax)
    ) / d
    
    center = (ux, uy)
    
    radius_sq = _distance_sq(center, p1)
    dist_sq = _distance_sq(center, point)

    return dist_sq < radius_sq


def triangulate(points: Sequence[Point]) -> List[Triangle]:
    """Compute the Delaunay triangulation of a 2D point set.

    Args:
        points: Sequence of (x, y) coordinates.

    Returns:
        List of triangles represented as index triplets.

    Raises:
        ValueError: If fewer than three points are provided.
        
    """
    n = len(points)
    if n < 3:
        raise ValueError("Moins de 3 points: non triangulable.")

    
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    dx = max_x - min_x
    dy = max_y - min_y
    delta_max = max(dx, dy)
    
    mid_x = (min_x + max_x) / 2
    mid_y = (min_y + max_y) / 2

    p_st1 = (mid_x - 20 * delta_max, mid_y - delta_max)
    p_st2 = (mid_x, mid_y + 20 * delta_max)
    p_st3 = (mid_x + 20 * delta_max, mid_y - delta_max)

    local_points = list(points)
    local_points.extend([p_st1, p_st2, p_st3])
    
    st_idx1, st_idx2, st_idx3 = n, n+1, n+2

    triangulation = [(st_idx1, st_idx2, st_idx3)]

    for i in range(n):
        point = local_points[i]
        bad_triangles = []
        
        for tri in triangulation:
            if _circumcircle_contains(tri, point, local_points):
                bad_triangles.append(tri)

        polygon = []
        
        for tri in bad_triangles:
            edges = [
                (tri[0], tri[1]),
                (tri[1], tri[2]),
                (tri[2], tri[0])
            ]
            for edge in edges:
                is_shared = False
                for other_tri in bad_triangles:
                    if tri == other_tri:
                        continue
                    other_edges = [
                        (other_tri[0], other_tri[1]), 
                        (other_tri[1], other_tri[2]), 
                        (other_tri[2], other_tri[0])
                    ]
                    if edge in other_edges or (edge[1], edge[0]) in other_edges:
                        is_shared = True
                        break
                
                if not is_shared:
                    polygon.append(edge)

        for tri in bad_triangles:
            triangulation.remove(tri)

        for edge in polygon:
            triangulation.append((edge[0], edge[1], i))

    final_triangles = []
    for tri in triangulation:
        if tri[0] >= n or tri[1] >= n or tri[2] >= n:
            continue
        final_triangles.append(tri)

    return final_triangles


def triangulate_data(data: bytes) -> bytes:
    """Exécute le pipeline complet de triangulation à partir de données binaires.

    Étapes :
    - décodage du PointSet,
    - calcul de la triangulation,
    - encodage du résultat binaire.

    Args:
        data: Représentation binaire du PointSet.

    Returns:
        Représentation binaire des triangles.

    """
    points = decode_point_set(data)
    triangles = triangulate(points)
    return encode_triangles(points, triangles)