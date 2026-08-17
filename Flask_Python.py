#pip install flask
# app.py
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

def compute():
    # Your Python logic goes here
    return {"message": "Hello from Python!", "value": 42}

@app.get("/api/result")
def result():
    return jsonify(compute())

@app.get("/")
def index():
    # Tiny HTML page that calls the API and shows the result
    return render_template_string("""
<!doctype html><meta charset="utf-8">
<h1>Python → Browser Demo</h1>
<div id="out">Loading…</div>
<script>
  fetch('/api/result')
    .then(r => r.json())
    .then(d => { document.getElementById('out').textContent = d.message + " | value=" + d.value; })
    .catch(err => { document.getElementById('out').textContent = "Error: " + err; });
</script>
""")

if __name__ == "__main__":
    app.run(debug=True)

