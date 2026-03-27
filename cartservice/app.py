from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Where product-service is reachable (K8s service name later)
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:5002")

# In-memory cart store: username -> {product_id -> qty}
CARTS = {}


@app.get("/health")
def health():
    return {"status": "ok", "service": "cart-service"}, 200


@app.post("/cart/add")
def cart_add():
    data = request.get_json(silent=True) or {}
    user = data.get("user", "guest")
    product_id = int(data.get("product_id", 0))
    qty = int(data.get("qty", 1))

    if product_id <= 0 or qty <= 0:
        return jsonify({"message": "valid product_id and qty required"}), 400

    CARTS.setdefault(user, {})
    CARTS[user][product_id] = CARTS[user].get(product_id, 0) + qty
    return jsonify({"message": "added", "cart": CARTS[user]}), 200


@app.get("/cart/<user>")
def cart_get(user: str):
    return jsonify({"user": user, "items": CARTS.get(user, {})}), 200


@app.get("/cart/<user>/total")
def cart_total(user: str):
    items = CARTS.get(user, {})
    if not items:
        return jsonify({"user": user, "total": 0, "currency": "INR"}), 200

    total = 0
    details = []

    for pid, qty in items.items():
        r = requests.get(f"{PRODUCT_SERVICE_URL}/products/{pid}", timeout=3)
        if r.status_code != 200:
            return jsonify({"message": f"product {pid} not found in product-service"}), 404
        p = r.json()
        line = p["price"] * qty
        total += line
        details.append({"product_id": pid, "name": p["name"], "qty": qty, "unit_price": p["price"], "line_total": line})

    return jsonify({"user": user, "total": total, "currency": "INR", "details": details}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
