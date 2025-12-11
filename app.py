from flask import Flask, jsonify
import os
import socket
import random

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/metrics")
def metrics():
    # Fake metrics so you can tell a DevOps story in interviews
    data = {
        "impressions": random.randint(1000, 5050),
        "clicks": random.randint(100, 800),
        "conversions": random.randint(10, 100),
        "host": socket.gethostname()
    }
    return jsonify(data), 200

@app.route("/")
def root():
    return "Campaign Metrics API is running", 200

if __name__ == "__main__":
    # Azure Container Apps expects port 5050
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port)
