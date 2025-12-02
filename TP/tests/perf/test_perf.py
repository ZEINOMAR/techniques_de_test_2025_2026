import time
import pytest
from triangulator import core, binary


@pytest.mark.perf
def test_triangulation_perf_small():
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
    points = [(float(i), float(i * 0.5)) for i in range(5000)]

    start = time.perf_counter()
    data = binary.encode_point_set(points)
    decoded = binary.decode_point_set(data)
    duration = time.perf_counter() - start

    assert duration < 1.0
    assert decoded == points
