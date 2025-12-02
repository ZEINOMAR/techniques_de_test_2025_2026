import pytest
from triangulator import core


def test_triangulation_three_points_returns_one_triangle():
    pts = [(0, 0), (1, 0), (0, 1)]
    triangles = core.triangulate(pts)

    assert len(triangles) == 1
    assert triangles[0] == (0, 1, 2)


def test_triangulation_less_than_three_points_raises():
    with pytest.raises(ValueError):
        core.triangulate([(0, 0), (1, 0)])


def test_triangulation_ignores_point_positions_for_now():
    pts = [(10, 10), (-5, 3), (9, -12), (0, 0)]
    triangles = core.triangulate(pts)

    assert len(triangles) == 1
    assert triangles[0] == (0, 1, 2)
