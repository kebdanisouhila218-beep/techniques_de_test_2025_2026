from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/triangulate', methods=['POST'])
def triangulate():
    """
    Endpoint simulé pour la triangulation.
    À ce stade, la logique n’est pas encore implémentée.
    """
    return jsonify({"error": "Not implemented"}), 501

if __name__ == '__main__':
    app.run(debug=True)
