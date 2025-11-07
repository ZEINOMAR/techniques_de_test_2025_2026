import pytest
from src.triangulator import core

def test_triangulation_three_points_returns_one_triangle():
    pts = [(0,0), (1,0), (0,1)]
    tris = core.triangulate(pts)
    assert len(tris) == 1

def test_triangulation_less_than_three_points_raises():
    with pytest.raises(ValueError):
        core.triangulate([(0,0), (1,0)])
