from flask import Flask, request, jsonify
import os
import random
import time

app = Flask(__name__)

# Toggle behavior via env to simulate failures / latency scenario
FAIL_RATE = float(os.getenv("PAYMENT_FAIL_RATE", "0.10"))   # 10% failures
MIN_DELAY = float(os.getenv("PAYMENT_MIN_DELAY", "0.2"))    # seconds
MAX_DELAY = float(os.getenv("PAYMENT_MAX_DELAY", "1.2"))    # seconds


@app.get("/health")
def health():
    return {"status": "ok", "service": "payment-service"}, 200


@app.post("/pay")
def pay():
    data = request.get_json(silent=True) or {}
    user = data.get("user", "guest")
    amount = float(data.get("amount", 0))

    if amount <= 0:
        return jsonify({"message": "amount must be > 0"}), 400

    # simulate latency issue scenario (checkout/payment)
    time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

    # simulate payment failure scenario
    if random.random() < FAIL_RATE:
        return jsonify({"status": "FAILED", "message": "payment gateway error", "user": user}), 502

    txn = f"TXN-{int(time.time())}-{random.randint(1000,9999)}"
    return jsonify({"status": "SUCCESS", "transaction_id": txn, "user": user, "amount": amount}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
