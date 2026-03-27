from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory catalog (demo purpose)
PRODUCTS = [
    {"id": 1, "name": "TV", "price": 715000},
    {"id": 2, "name": "Speaker",  "price": 325000},
    {"id": 3, "name": "Camera", "price": 238000},
]


@app.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}, 200


@app.get("/products")
def list_products():
    return jsonify(PRODUCTS), 200


@app.get("/products/<int:pid>")
def get_product(pid: int):
    for p in PRODUCTS:
        if p["id"] == pid:
            return jsonify(p), 200
    return jsonify({"message": "product not found"}), 404


@app.post("/products")
def add_product():
    # simple demo add
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    price = data.get("price")
    if not name or price is None:
        return jsonify({"message": "name and price required"}), 400

    new_id = max([p["id"] for p in PRODUCTS]) + 1 if PRODUCTS else 1
    PRODUCTS.append({"id": new_id, "name": name, "price": int(price)})
    return jsonify({"message": "created", "id": new_id}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
