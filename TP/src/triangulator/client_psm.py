"""
Client for PointSetManager (stub for now).
"""

class PointSetNotFound(Exception):
    """Raised when PSM reports missing PointSet."""


class PointSetManagerUnavailable(Exception):
    """Raised when PSM is unreachable."""


def get_pointset_bytes(pointset_id: str) -> bytes:
    """Fetch PointSet binary data from PointSetManager by its ID.   
    This is a stub implementation that always raises PointSetManagerUnavailable.
    Args:
        pointset_id: The UUID of the PointSet to fetch.
    Returns:
        The binary data of the PointSet.
    Raises:
        PointSetNotFound: If the PointSet does not exist.
        PointSetManagerUnavailable: If the PSM service is unreachable.
    """
    raise PointSetManagerUnavailable("PSM indisponible (stub).")