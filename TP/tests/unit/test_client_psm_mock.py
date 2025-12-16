"""Tests unitaires du client PointSetManager avec des mocks.

Ces tests simulent différentes réponses HTTP et erreurs sans effectuer
d'appels réseau réels. Ils vérifient le comportement de la fonction
get_pointset_bytes dans divers scénarios.
"""

import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from triangulator import client_psm


def test_psm_success_200():
    """Scénario : réponse HTTP 200 valide simulée.

    Comportement attendu : get_pointset_bytes retourne les octets reçus.
    Exception : aucune exception levée.
    """
    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.read.return_value = b"\x01\x02\x03"
    mock_resp.__enter__.return_value = mock_resp

    with patch("urllib.request.urlopen", return_value=mock_resp):
        data = client_psm.get_pointset_bytes("id-ok")
        assert data == b"\x01\x02\x03"

def test_psm_error_404():
    """Scénario : erreur HTTP 404 simulée (pointset non trouvé).

    Comportement attendu : get_pointset_bytes lève PointSetNotFound.
    """
    err = urllib.error.HTTPError("url", 404, "Not Found", {}, None)
    with patch("urllib.request.urlopen", side_effect=err):
        with pytest.raises(client_psm.PointSetNotFound):
            client_psm.get_pointset_bytes("id-missing")

def test_psm_error_503():
    """Scénario : erreur HTTP 503 simulée (service indisponible).

    Comportement attendu : get_pointset_bytes lève
    PointSetManagerUnavailable.
    """
    err = urllib.error.HTTPError("url", 503, "Unavailable", {}, None)
    with patch("urllib.request.urlopen", side_effect=err):
        with pytest.raises(client_psm.PointSetManagerUnavailable):
            client_psm.get_pointset_bytes("id-down")

def test_psm_connection_error():
    """Scénario : coupure réseau simulée (URLError).

    Comportement attendu : get_pointset_bytes lève
    PointSetManagerUnavailable.
    """
    with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("No route")):
        with pytest.raises(client_psm.PointSetManagerUnavailable):
            client_psm.get_pointset_bytes("id-crash")

def test_psm_unexpected_status_code():
    """Scénario : code HTTP inattendu (204 No Content) simulé.

    Comportement attendu : get_pointset_bytes lève
    PointSetManagerUnavailable.
    """
    mock_resp = MagicMock()
    mock_resp.status = 204
    mock_resp.__enter__.return_value = mock_resp
    
    with patch("urllib.request.urlopen", return_value=mock_resp):
        with pytest.raises(client_psm.PointSetManagerUnavailable):
            client_psm.get_pointset_bytes("id-204")

def test_psm_weird_http_error():
    """Scénario : erreur HTTP inconnue simulée (418 I'm a teapot).

    Comportement attendu : get_pointset_bytes lève
    PointSetManagerUnavailable.
    """
    err = urllib.error.HTTPError("url", 418, "I am a teapot", {}, None)
    with patch("urllib.request.urlopen", side_effect=err):
        with pytest.raises(client_psm.PointSetManagerUnavailable):
            client_psm.get_pointset_bytes("id-teapot")