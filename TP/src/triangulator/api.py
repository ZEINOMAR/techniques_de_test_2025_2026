"""API Flask pour le service Triangulator."""

from uuid import UUID

from flask import Flask, Response, jsonify

from triangulator import binary, client_psm, core

app = Flask(__name__)

@app.route("/triangulation/<pointset_id>", methods=["GET"])
def get_triangulation(pointset_id: str) -> Response:
    """Expose un endpoint HTTP permettant de calculer la triangulation d’un PointSet.

    L’endpoint valide l’identifiant, récupère les données binaires du PointSet,
    calcule la triangulation et retourne le résultat encodé.
    """
    try:
        UUID(pointset_id)
    except Exception:
        return (
            jsonify(
                {
                    "code": "INVALID_ID_FORMAT",
                    "message": "Le PointSetID doit être un UUID valide.",
                }
            ),
            400,
        )

    try:
        data = client_psm.get_pointset_bytes(pointset_id)
        points = binary.decode_point_set(data)
        triangles = core.triangulate(points)
        triangles_bytes = binary.encode_triangles(points, triangles)

        return Response(
            triangles_bytes,
            mimetype="application/octet-stream",
            status=200,
        )

    except client_psm.PointSetNotFound:
        return (
            jsonify(
                {
                    "code": "NOT_FOUND",
                    "message": "PointSet introuvable",
                }
            ),
            404,
        )

    except client_psm.PointSetManagerUnavailable:
        return (
            jsonify(
                {
                    "code": "SERVICE_UNAVAILABLE",
                    "message": "PointSetManager inaccessible",
                }
            ),
            503,
        )

    except ValueError as exc:
        return (
            jsonify(
                {
                    "code": "BAD_POINTSET",
                    "message": str(exc),
                }
            ),
            400,
        )

    except Exception as exc:
        return (
            jsonify(
                {
                    "code": "INTERNAL_ERROR",
                    "message": str(exc),
                }
            ),
            500,
        )

if __name__ == "__main__":
    app.run(debug=True)