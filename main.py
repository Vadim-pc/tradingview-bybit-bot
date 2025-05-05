from flask import Flask, request, jsonify
import time, hmac, hashlib, requests

app = Flask(__name__)

API_KEY = "ТВОЙ_API_KEY"
API_SECRET = "ТВОЙ_API_SECRET"
SYMBOL = "BTCUSDT"

def create_signature(params, secret):
    query_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
    return hmac.new(secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def place_order(side):
    url = "https://api.bybit.com/v2/private/order/create"
    timestamp = str(int(time.time() * 1000))
    params = {
        "api_key": API_KEY,
        "symbol": SYMBOL,
        "side": side.upper(),
        "order_type": "Market",
        "qty": "0.01",
        "time_in_force": "GoodTillCancel",
        "timestamp": timestamp,
    }
    params["sign"] = create_signature(params, API_SECRET)
    response = requests.post(url, data=params)
    return response.json()

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    side = data.get("side", "").lower()
    if side not in ["buy", "sell"]:
        return jsonify({"error": "Invalid signal"}), 400
    result = place_order(side)
    return jsonify(result)

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

