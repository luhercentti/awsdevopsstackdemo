from flask import Flask, jsonify
import os
import time
import threading
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Global readiness state
READY = False
START_TIME = time.time()

@app.before_first_request
def mark_ready():
    global READY
    if not READY:
        app.logger.info("Application now ready to serve traffic")
        READY = True

@app.route('/health')
def health():
    uptime = time.time() - START_TIME
    
    # Return 503 for first 2 minutes
    if uptime < 120:
        app.logger.info(f"Health check during startup (uptime: {uptime:.1f}s)")
        return jsonify({
            'status': 'starting',
            'uptime': f"{uptime:.1f}s"
        }), 503
    
    # After 2 minutes, check real readiness
    if not READY:
        return jsonify({'status': 'not-ready'}), 503
    
    return jsonify({'status': 'healthy'})

def run_production_server():
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

if __name__ == '__main__':
    # Start in background to allow immediate health checks
    server_thread = threading.Thread(target=run_production_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Immediate health check availability
    app.logger.info("Application starting...")
    app.run(host='0.0.0.0', port=8080, use_reloader=False)