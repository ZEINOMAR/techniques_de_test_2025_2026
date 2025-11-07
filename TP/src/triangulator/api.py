from flask import Flask, Response, jsonify

app = Flask(__name__)

@app.route("/triangulation/<pointset_id>", methods=["GET"])
def get_triangulation(pointset_id):
    try:
        dummy = b"\x03\x00\x00\x00" + b"\x00\x00\x00\x00"*6
        return Response(dummy, mimetype="application/octet-stream", status=200)
    except Exception as e:  
        return jsonify({"code": "INTERNAL_ERROR", "message": str(e)}), 500
