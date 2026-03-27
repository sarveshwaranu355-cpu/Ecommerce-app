from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# In-memory users (demo purpose)
USERS = {
    "sarvesh": {"password": "pass123", "role": "customer"},
    "admin": {"password": "admin123", "role": "admin"}
}

SESSIONS = {}  # token -> username


@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}, 200


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if username in USERS and USERS[username]["password"] == password:
        token = f"token-{username}-{int(time.time())}"
        SESSIONS[token] = username
        return jsonify({"message": "login success", "token": token}), 200

    return jsonify({"message": "invalid credentials"}), 401


@app.get("/me")
def me():
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    username = SESSIONS.get(token)
    if not username:
        return jsonify({"message": "unauthorized"}), 401

    profile = {"username": username, "role": USERS[username]["role"]}
    return jsonify(profile), 200


if __name__ == "__main__":
    # container-friendly host binding
    app.run(host="0.0.0.0", port=5001)
