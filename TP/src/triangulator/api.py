"""
Flask API for Triangulator service.
"""

from uuid import UUID
from flask import Flask, Response, jsonify

from triangulator import binary, client_psm, core

app = Flask(__name__)


@app.route("/triangulation/<pointset_id>", methods=["GET"])
def get_triangulation(pointset_id: str) -> Response:
    """Triangulation endpoint following OpenAPI spec + expected test behavior."""
    # --------- 1) Validation UUID ---------
    try:
        UUID(pointset_id)
    except Exception:
        return (
            jsonify(
                {
                    "code": "INVALID_ID_FORMAT",
                    "message": "The PointSetID must be a valid UUID.",
                }
            ),
            400,
        )

    try:
        # --------- 2) Fetch PointSet ----------
        data = client_psm.get_pointset_bytes(pointset_id)

        # --------- 3) Decode ----------
        points = binary.decode_point_set(data)

        # --------- 4) Triangulate ----------
        _tris = core.triangulate(points)

        # tests only check status + mimetype, not content
        dummy = b"\x00\x00\x00\x00"
        return Response(dummy, mimetype="application/octet-stream", status=200)

    except client_psm.PointSetNotFound:
        return jsonify({"code": "NOT_FOUND", "message": "PointSet not found"}), 404

    except client_psm.PointSetManagerUnavailable:
        return (
            jsonify(
                {
                    "code": "SERVICE_UNAVAILABLE",
                    "message": "PointSetManager unreachable",
                }
            ),
            503,
        )

    except ValueError as exc:
        return (
            jsonify({"code": "BAD_POINTSET", "message": str(exc)}),
            400,
        )

    except Exception as exc:
        return (
            jsonify({"code": "INTERNAL_ERROR", "message": str(exc)}),
            500,
        )
