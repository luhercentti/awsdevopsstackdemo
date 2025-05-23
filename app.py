# requirements.txt - Add these production dependencies
flask==2.3.3
gunicorn==21.2.0
gevent==23.7.0

# app.py - Updated Flask application
from flask import Flask, jsonify
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    logger.info("Index endpoint accessed")
    return jsonify({
        'message': 'Hello from Python Flask!',
        'status': 'running'
    })

@app.route('/health')
def health():
    logger.info("Health check endpoint accessed")
    return jsonify({
        'status': 'healthy'
    }), 200

@app.route('/readiness')
def readiness():
    """Additional readiness check for Kubernetes-style health checks"""
    return jsonify({
        'status': 'ready'
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    # Only for local development - production uses Gunicorn
    app.run(host='0.0.0.0', port=port, debug=False)