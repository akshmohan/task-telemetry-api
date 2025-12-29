from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import redis
import os
import socket

app = Flask(__name__)

# This is the "Secret Sauce" for your Prometheus skill. 
# It creates the /metrics endpoint automatically.
metrics = PrometheusMetrics(app)

# We use an Environment Variable for the DB host. 
# This is a core "Twelve-Factor App" principle.
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@app.route('/')
def index():
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)