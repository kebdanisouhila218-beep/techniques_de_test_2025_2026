from flask import Flask, request, Response
import requests
from triangulator.pointset import PointSet
from triangulator.triangles import Triangles
from triangulator.triangulator import triangulate

app = Flask(__name__)

@app.route("/triangulate", methods=["POST"])
def triangulate_endpoint():
    # 1. Vérifier que le JSON contient "pointset_id"
    data = request.get_json()
    if not data or "pointset_id" not in data:
        return {"error": "Missing pointset_id"}, 400

    pointset_id = data["pointset_id"]

    # 2. Appeler le PointSetManager (mocké dans les tests)
    try:
        resp = requests.get(f"http://pointset-manager/{pointset_id}")
    except requests.RequestException:
        return {"error": "PointSetManager unreachable"}, 500

    if resp.status_code == 404:
        return {"error": "PointSet not found"}, 404
    if resp.status_code != 200:
        return {"error": "PointSetManager error"}, 500

    # 3. Parser le PointSet
    try:
        pointset = PointSet.from_bytes(resp.content)
    except Exception:
        return {"error": "Invalid PointSet format"}, 400

    # 4. Trianguler
    try:
        triangle_indices = triangulate(pointset.points)
    except ValueError as e:
        return {"error": str(e)}, 400

    # 5. Créer Triangles et renvoyer en binaire
    triangles_obj = Triangles(pointset.points, triangle_indices)
    binary_result = triangles_obj.to_bytes()

    return Response(
        binary_result,
        mimetype="application/octet-stream",
        status=200
    )

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200