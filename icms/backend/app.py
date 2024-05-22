from flask import Flask, request, jsonify,send_file
from creatives import generate_creatives
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def response_json(status, data, status_code):
    return jsonify({"status": status, "data": data}), status_code

@app.route("/creatives", methods=["POST"])
def generate_creative():
    payload = request.get_json()
    creatives_result = generate_creatives(payload)
    if creatives_result.get("status") == "Error":
        return response_json("Error", creatives_result["error"], 404)
    return response_json("Success", creatives_result, 200)

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), "output", filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return response_json("Error", "File not found", 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
