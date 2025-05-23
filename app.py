from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'message': 'Hello from Python Flask!',
        'status': 'running'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)