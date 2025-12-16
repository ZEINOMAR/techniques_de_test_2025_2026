"""Utilitaires communs pour la gestion des erreurs de l’API.

Ce module fournit des fonctions simples permettant de construire
des réponses d’erreur homogènes, conformes au contrat OpenAPI
(code + message).
"""

def make_error(code: str, message: str):
    """Construire une structure d’erreur standardisée pour les réponses API.

    :param code: Code d’erreur interne (ex: NOT_FOUND, SERVICE_UNAVAILABLE).
    :param message: Message lisible décrivant l’erreur.
    :return: Dictionnaire contenant le code et le message d’erreur.
    """
    return {"code": code, "message": message}
