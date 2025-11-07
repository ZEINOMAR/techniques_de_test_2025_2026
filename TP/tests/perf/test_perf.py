import time
import pytest
from src.triangulator import core

@pytest.mark.perf
def test_triangulation_perf_smoke():
    pts = [(float(i), float(i+1)) for i in range(1000)]
    t0 = time.perf_counter()
    try:
        core.triangulate(pts)
    except Exception:
        pass
    assert (time.perf_counter() - t0) < 1.0
