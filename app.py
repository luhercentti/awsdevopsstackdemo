from flask import Flask, jsonify
import time
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

START_TIME = time.time()
READY = False

@app.before_first_request
def mark_ready():
    global READY
    if not READY:
        READY = True
        app.logger.info("Application is now ready to serve requests")

@app.route('/health')
def health():
    uptime = time.time() - START_TIME
    
    # Return 503 for first 45 seconds
    if uptime < 45:
        app.logger.info(f"Health check during startup (uptime: {uptime:.1f}s)")
        return jsonify({
            'status': 'starting',
            'uptime': f"{uptime:.1f}s"
        }), 503
    
    # After 45 seconds, check real readiness
    if not READY:
        return jsonify({'status': 'not-ready'}), 503
    
    return jsonify({'status': 'healthy'})

@app.route('/')
def index():
    return jsonify({
        'message': 'Hello from Python Flask!',
        'status': 'running'
    })