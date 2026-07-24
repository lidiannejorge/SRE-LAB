from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "service": "api",
        "hostname": socket.gethostname(),
        "time": datetime.datetime.now().isoformat()
    })

@app.route("/users")
def users():
    return jsonify([
        {
            "id": 1,
            "name": "Lidiane"
        },
        {
            "id": 2,
            "name": "SRE Engineer"
        }
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
