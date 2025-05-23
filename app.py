from flask import Flask, jsonify
import os
import time
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Track startup time
START_TIME = time.time()

@app.route('/health')
def health():
    uptime = time.time() - START_TIME
    
    # Return 503 for first 30 seconds
    if uptime < 30:
        app.logger.info(f"Health check during startup (uptime: {uptime:.1f}s)")
        return jsonify({
            'status': 'starting',
            'uptime': f"{uptime:.1f}s"
        }), 503
    
    return jsonify({'status': 'healthy'})

@app.route('/')
def index():
    return jsonify({
        'message': 'Hello from Python Flask!',
        'status': 'running'
    })

# No main block needed - Gunicorn will import app directly