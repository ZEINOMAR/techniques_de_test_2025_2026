"""Flask API for Triangulator service."""

from flask import Flask, Response, jsonify
from .client_psm import (
    get_pointset_bytes,
    PointSetNotFound,
    PointSetManagerUnavailable,
)
from .binary import decode_point_set
from .core import triangulate

app = Flask(__name__)


@app.route("/triangulation/<pointset_id>", methods=["GET"])
def get_triangulation(pointset_id):
    """Triangulation endpoint (behavior implemented in final version)."""
    try:
        data = get_pointset_bytes(pointset_id)

        points = decode_point_set(data)

        
        triangles = triangulate(points)

        return Response(b"", mimetype="application/octet-stream", status=200)

    except ValueError:
        return jsonify({"code": "BAD_POINTSET", "message": "Invalid data"}), 500

    except PointSetNotFound:
        return jsonify({"code": "NOT_FOUND", "message": "PointSet not found"}), 404

    except PointSetManagerUnavailable:
        return jsonify({"code": "PSM_UNAVAILABLE", "message": "PSM unreachable"}), 503

    except Exception as exc:
        return jsonify({"code": "INTERNAL_ERROR", "message": str(exc)}), 500
