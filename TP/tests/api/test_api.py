import pytest
from flask import Response
from triangulator.api import app
from triangulator import client_psm


@pytest.fixture
def client():
    return app.test_client()


def test_get_triangulation_success(monkeypatch, client):
    def mock_get_pointset_bytes(pointset_id):
        return b"\x03\x00\x00\x00" + b"\x00\x00\x00\x00" * 6

    monkeypatch.setattr("triangulator.client_psm.get_pointset_bytes", mock_get_pointset_bytes)
    res = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000")

    assert res.status_code == 200
    assert res.mimetype == "application/octet-stream"
    assert isinstance(res, Response)
    assert len(res.data) >= 4


def test_get_triangulation_invalid_id(client):
    res = client.get("/triangulation/invalid-id-format")
    assert res.status_code == 400
    assert res.is_json
    assert res.json.get("code") == "INVALID_ID_FORMAT"


def test_get_triangulation_empty_id_path(client):
    res = client.get("/triangulation/")
    assert res.status_code in (400, 404)


def test_get_triangulation_bad_uuid_extra_chars(client):
    res = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000-XYZ")
    assert res.status_code == 400
    assert res.is_json
    assert res.json.get("code") == "INVALID_ID_FORMAT"


def test_get_triangulation_not_found(monkeypatch, client):
    def mock_get_pointset_bytes(pointset_id):
        raise client_psm.PointSetNotFound("PointSet not found")

    monkeypatch.setattr("triangulator.client_psm.get_pointset_bytes", mock_get_pointset_bytes)
    res = client.get("/triangulation/11111111-1111-1111-1111-111111111111")

    assert res.status_code == 404
    assert res.json["code"] == "NOT_FOUND"


def test_get_triangulation_service_unavailable(monkeypatch, client):
    def mock_get_pointset_bytes(pointset_id):
        raise client_psm.PointSetManagerUnavailable("PSM down")

    monkeypatch.setattr("triangulator.client_psm.get_pointset_bytes", mock_get_pointset_bytes)
    res = client.get("/triangulation/22222222-2222-2222-2222-222222222222")

    assert res.status_code == 503
    assert res.json["code"] == "SERVICE_UNAVAILABLE"


def test_get_triangulation_internal_error(monkeypatch, client):
    def mock_get_pointset_bytes(pointset_id):
        raise Exception("Unexpected error")

    monkeypatch.setattr("triangulator.client_psm.get_pointset_bytes", mock_get_pointset_bytes)
    res = client.get("/triangulation/33333333-3333-3333-3333-333333333333")

    assert res.status_code == 500
    assert res.json["code"] == "INTERNAL_ERROR"
