from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = {"raw": request.data.decode('utf-8')}

        print(f"[{datetime.datetime.now()}] Alert received: {data}")
        return jsonify({"status": "received"}), 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 400
