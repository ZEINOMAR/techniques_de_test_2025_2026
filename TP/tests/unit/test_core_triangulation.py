"""Tests unitaires du module `core`.

Ces tests valident le comportement de base de la fonction de triangulation,
en vérifiant des cas géométriques simples et des situations limites.
"""

from triangulator import core


def test_triangulate_square():
    """Vérifie qu'un carré composé de quatre points est découpé.

    Le carré doit être découpé en deux triangles valides.
    """
    points = [(0.0, 0.0), (10.0, 0.0), (0.0, 10.0), (10.0, 10.0)]
    triangles = core.triangulate(points)

    assert len(triangles) == 2
    for triangle in triangles:
        assert min(triangle) >= 0
        assert max(triangle) < len(points)


def test_triangulate_point_inside():
    """Vérifie le comportement de l'algorithme lorsqu'un point est à l'intérieur.

    Ce cas force la création de triangles internes et permet de couvrir les
    étapes de nettoyage de la triangulation.
    """
    points = [(0.0, 0.0), (10.0, 0.0), (0.0, 10.0), (2.0, 2.0)]
    triangles = core.triangulate(points)

    assert len(triangles) == 3


def test_triangulate_collinear_safe():
    """Vérifie que la triangulation ne lève pas d'exception.

    Ce test couvre le cas où certains points sont alignés.
    """
    points = [(0, 0), (1, 1), (2, 2), (5, 0)]
    core.triangulate(points)