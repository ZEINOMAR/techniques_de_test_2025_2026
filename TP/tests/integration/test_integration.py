import pytest
from src.triangulator import client_psm

def test_psm_unavailable_stub():
    with pytest.raises(client_psm.PointSetManagerUnavailable):
        client_psm.get_pointset_bytes("any-id")
