"""Tests d’API du service Triangulator.

Ces tests valident le contrat HTTP exposé par l’API :
- validation du format des identifiants,
- gestion des erreurs métier et techniques,
- conformité des codes de statut et des réponses JSON/binaire.
"""

import pytest
from flask import Response

from triangulator import client_psm
from triangulator.api import app


@pytest.fixture
def client():
    """Client Flask utilisé pour tester les endpoints de l’API."""
    return app.test_client()


def test_get_triangulation_success(monkeypatch, client):
    """Retourne 200 et un flux binaire lorsque la triangulation réussit."""
    def mock_get_pointset_bytes(pointset_id):
        return b"\x03\x00\x00\x00" + b"\x00\x00\x00\x00" * 6

    monkeypatch.setattr(
        "triangulator.client_psm.get_pointset_bytes",
        mock_get_pointset_bytes
    )

    res = client.get(
        "/triangulation/123e4567-e89b-12d3-a456-426614174000"
    )

    assert res.status_code == 200
    assert res.mimetype == "application/octet-stream"
    assert isinstance(res, Response)
    assert len(res.data) >= 4


def test_get_triangulation_invalid_id(client):
    """Retourne 400 si l’identifiant n’est pas un UUID valide."""
    res = client.get("/triangulation/invalid-id-format")

    assert res.status_code == 400
    assert res.is_json
    assert res.json.get("code") == "INVALID_ID_FORMAT"


def test_get_triangulation_empty_id_path(client):
    """Retourne une erreur si l’identifiant est absent dans l’URL."""
    res = client.get("/triangulation/")
    assert res.status_code in (400, 404)


def test_get_triangulation_bad_uuid_extra_chars(client):
    """Retourne 400 si l’UUID contient des caractères supplémentaires."""
    res = client.get(
        "/triangulation/123e4567-e89b-12d3-a456-426614174000-XYZ"
    )

    assert res.status_code == 400
    assert res.is_json
    assert res.json.get("code") == "INVALID_ID_FORMAT"


def test_get_triangulation_not_found(monkeypatch, client):
    """Retourne 404 si le PointSet n’existe pas."""
    def mock_get_pointset_bytes(pointset_id):
        raise client_psm.PointSetNotFound("PointSet not found")

    monkeypatch.setattr(
        "triangulator.client_psm.get_pointset_bytes",
        mock_get_pointset_bytes
    )

    res = client.get(
        "/triangulation/11111111-1111-1111-1111-111111111111"
    )

    assert res.status_code == 404
    assert res.json["code"] == "NOT_FOUND"


def test_get_triangulation_service_unavailable(monkeypatch, client):
    """Retourne 503 lorsque le PointSetManager est indisponible."""
    def mock_get_pointset_bytes(pointset_id):
        raise client_psm.PointSetManagerUnavailable("PSM down")

    monkeypatch.setattr(
        "triangulator.client_psm.get_pointset_bytes",
        mock_get_pointset_bytes
    )

    res = client.get(
        "/triangulation/22222222-2222-2222-2222-222222222222"
    )

    assert res.status_code == 503
    assert res.json["code"] == "SERVICE_UNAVAILABLE"


def test_get_triangulation_internal_error(monkeypatch, client):
    """Retourne 500 en cas d’erreur interne inattendue."""
    def mock_get_pointset_bytes(pointset_id):
        raise Exception("Unexpected error")

    monkeypatch.setattr(
        "triangulator.client_psm.get_pointset_bytes",
        mock_get_pointset_bytes
    )

    res = client.get(
        "/triangulation/33333333-3333-3333-3333-333333333333"
    )

    assert res.status_code == 500
    assert res.json["code"] == "INTERNAL_ERROR"


def test_get_triangulation_value_error(monkeypatch, client):
    """Retourne 400 si la triangulation échoue pour un PointSet invalide."""
    def mock_raise_error(*args):
        raise ValueError("Erreur de triangulation simulée")

    monkeypatch.setattr(
        "triangulator.client_psm.get_pointset_bytes",
        lambda x: b"fake_data"
    )
    monkeypatch.setattr(
        "triangulator.binary.decode_point_set",
        lambda x: []
    )
    monkeypatch.setattr(
        "triangulator.core.triangulate",
        mock_raise_error
    )

    res = client.get(
        "/triangulation/123e4567-e89b-12d3-a456-426614174000"
    )

    assert res.status_code == 400
    assert res.json["code"] == "BAD_POINTSET"
    assert "Erreur de triangulation" in res.json["message"]