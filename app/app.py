from flask import Flask, jsonify
import redis
import os
import socket
# This is the industry-standard library
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# 1. Define your custom metric
# We call it 'http_requests_total' so Prometheus knows what to look for
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@app.route('/')
def index():
    # 2. Increment the counter every time someone hits this route
    REQUEST_COUNT.inc()
    
    try:
        hits = cache.incr('hits')
        return jsonify({
            "status": "online",
            "message": "Task Telemetry API is live",
            "hits": hits,
            "container_id": socket.gethostname()
        })
    except redis.exceptions.ConnectionError:
        return jsonify({
            "status": "degraded",
            "error": "Redis unreachable",
            "container_id": socket.gethostname()
        }), 500

# 3. Create the /metrics endpoint manually
@app.route('/metrics')
def metrics():
    # generate_latest() turns our Counter into the text format Prometheus needs
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)