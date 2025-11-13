"""Client for PointSetManager (stub for now)."""

class PointSetNotFound(Exception):
    """Raised when PSM reports missing PointSet."""


class PointSetManagerUnavailable(Exception):
    """Raised when PSM is unreachable."""


def get_pointset_bytes(pointset_id: str) -> bytes:
    """Stub: will be replaced by real HTTP fetch in final version."""
    raise PointSetManagerUnavailable("PSM unavailable")
