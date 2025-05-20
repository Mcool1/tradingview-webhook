from flask import Flask, request, jsonify
import datetime
from ib_insync import IB, Future, MarketOrder

app = Flask(__name__)

# Toggle live vs simulated mode
LIVE_TRADING = False  # Set to True to place real IBKR orders

# IBKR ngrok URL (update this to your actual tunnel address)
IBKR_HOST = 'your-ngrok-subdomain.ngrok.io'  # ⚠️ Replace this

def place_ibkr_order(action, symbol, price):
    order_action = 'BUY' if action.lower() == 'buy' else 'SELL'

    if not LIVE_TRADING:
        print(f"[SIMULATED ORDER] {order_action} {symbol} @ {price}")
        return {
            "status": "simulated",
            "action": order_action,
            "symbol": symbol,
            "price": price
        }

    ib = IB()
    try:
        ib.connect(IBKR_HOST, 7497, clientId=1)
        contract = Future(symbol=symbol, exchange='GLOBEX', currency='USD')
        ib.qualifyContracts(contract)

        order = MarketOrder(order_action, 1)
        trade = ib.placeOrder(contract, order)
        ib.sleep(2)

        return {
            "status": trade.orderStatus.status,
            "filled": trade.orderStatus.filled,
            "action": order_action,
            "symbol": symbol
        }

    finally:
        ib.disconnect()

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=False, silent=False)
        if data is None:
            raise ValueError("Invalid or missing JSON.")

        print(f"[{datetime.datetime.now()}] Webhook received: {data}")

        action = data.get("action")
        symbol = data.get("symbol")
        price = data.get("price")

        if not all([action, symbol, price]):
            raise ValueError("Missing required fields: action, symbol, price.")

        result = place_ibkr_order(action, symbol, price)
        return jsonify({"status": "ok", "result": result}), 200

    except Exception as e:
        raw_data = request.data.decode('utf-8', errors='replace')
        print(f"[{datetime.datetime.now()}] Webhook error: {e}, Raw: {raw_data}")
        return jsonify({"error": str(e), "raw": raw_data}), 400

@app.route('/test', methods=['POST'])
def test_webhook():
    data = request.get_json(force=True)
    print(f"[{datetime.datetime.now()}] TEST webhook received: {data}")

    action = data.get("action")
    symbol = data.get("symbol")
    price = data.get("price")

    if not all([action, symbol, price]):
        return jsonify({"error": "Missing fields"}), 400

    result = place_ibkr_order(action, symbol, price)
    return jsonify({"status": "ok", "details": result})
