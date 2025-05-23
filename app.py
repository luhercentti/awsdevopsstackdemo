from flask import Flask, jsonify
import os
import time

app = Flask(__name__)
READY = False

@app.before_first_request
def mark_ready():
    global READY
    READY = True

@app.route('/health')
def health():
    if not READY:
        # Return 503 during initialization
        return jsonify({'status': 'starting'}), 503
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Use Waitress production server
    from waitress import serve
    print("Starting application server...")
    serve(app, host="0.0.0.0", port=8080)