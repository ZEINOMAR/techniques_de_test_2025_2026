"""Client HTTP pour le PointSetManager.

Ce module gère la communication avec le service PointSetManager afin
de récupérer des ensembles de points (PointSet) au format binaire.
Il repose uniquement sur la bibliothèque standard afin de limiter
les dépendances externes.
"""

import os
import urllib.error
import urllib.request

PSM_HOST = os.getenv("PSM_HOST", "http://localhost:5001")


class PointSetNotFound(Exception):
    """Exception levée lorsque le PointSet demandé n’existe pas (404)."""


class PointSetManagerUnavailable(Exception):
    """Exception levée lorsque le PointSetManager est indisponible (5xx ou réseau)."""


def get_pointset_bytes(pointset_id: str) -> bytes:
    """Récupère les données binaires d’un PointSet depuis le PointSetManager.

    Args:
        pointset_id (str): Identifiant UUID du PointSet à récupérer.

    Returns:
        bytes: Représentation binaire du PointSet.

    Raises:
        PointSetNotFound: Si le PointSet n’existe pas.
        PointSetManagerUnavailable: Si le service est indisponible ou inaccessible.

    """
    url = f"{PSM_HOST}/pointset/{pointset_id}"

    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                return response.read()
            raise PointSetManagerUnavailable(f"Statut inattendu : {response.status}")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise PointSetNotFound(f"PointSet {pointset_id} introuvable.")
        if e.code == 503:
            raise PointSetManagerUnavailable("PointSetManager indisponible.")
        raise PointSetManagerUnavailable(f"Erreur PointSetManager : {e.code}")

    except urllib.error.URLError:
        raise PointSetManagerUnavailable("Impossible de contacter le PointSetManager.")