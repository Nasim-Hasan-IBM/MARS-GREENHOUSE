# pip install flask flask-cors
from flask import Flask, request, jsonify
from flask_cors import CORS  # allow cross-origin requests in dev
app = Flask(__name__)
CORS(app)  # remove or restrict in production

def compute(x: int):
    # Your Python logic
    return {"x": x, "square": x * x, "message": f"{x} squared is {x*x}"}

@app.post("/api/compute")
def compute_endpoint():
    data = request.get_json(force=True) or {}
    x = int(data.get("x", 0))
    return jsonify(compute(x))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)