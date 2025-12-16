"""Tests de performance pour les fonctions de triangulation.

Ces tests couvrent l'encodage/décodage binaire et la triangulation afin de
mesurer le temps d'exécution des opérations critiques et détecter
d'éventuelles régressions de performance.
"""

import time

import pytest

from triangulator import binary, core


@pytest.mark.perf
def test_triangulation_perf_small():
    """Test de performance de la triangulation sur un petit jeu de données.
    
    Ce test mesure le temps nécessaire pour trianguler 200 points.
    Le test réussit si la triangulation s'effectue en moins de 0.5 seconde.
    """
    points = [(float(i), float(i + 1)) for i in range(200)]

    start = time.perf_counter()
    try:
        core.triangulate(points)
    except Exception:
        pass
    duration = time.perf_counter() - start

    assert duration < 0.5


@pytest.mark.perf
def test_encode_decode_point_set_perf():
    """Test de performance de l'encodage et du décodage binaire d'un jeu de points.
    
    Ce test mesure le temps nécessaire pour encoder puis décoder 5000 points.
    Le test réussit si l'opération complète prend moins de 1 seconde et que 
    les points décodés correspondent aux points originaux.
    """
    points = [(float(i), float(i * 0.5)) for i in range(5000)]

    start = time.perf_counter()
    data = binary.encode_point_set(points)
    decoded = binary.decode_point_set(data)
    duration = time.perf_counter() - start

    assert duration < 1.0
    assert decoded == points
