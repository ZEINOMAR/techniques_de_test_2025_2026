from src.triangulator.api import app

def test_get_triangulation_returns_octet_stream():
    client = app.test_client()
    r = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000")
    assert r.status_code == 200
    assert r.mimetype == "application/octet-stream"
    assert len(r.data) >= 4
