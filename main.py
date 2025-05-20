this is my main.py script in github
from flask import Flask, request, jsonify
import datetime

app = Flask(**name**)

@app.route('/webhook', methods=\['POST'])
def webhook():
try:
\# Try parsing JSON only once
data = request.get\_json(force=False, silent=False)
if data is None:
raise ValueError("Invalid or missing JSON in request body.")

```
    print(f"[{datetime.datetime.now()}] Alert received: {data}")
    return jsonify({"status": "received"}), 200

except Exception as e:
    # Log raw request body to help debugging
    raw_data = request.data.decode('utf-8', errors='replace')
    print(f"[{datetime.datetime.now()}] Webhook error: {e}, Raw data: {raw_data}")
    return jsonify({"error": str(e), "raw": raw_data}), 400
```
