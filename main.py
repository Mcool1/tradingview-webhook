from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"[{datetime.datetime.now()}] Alert received: {data}")
    return jsonify({"status": "received"}), 200
