from flask import Flask, jsonify, request  # Added 'request' here
import redis
import os
import socket
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Updated Metric name to match what we usually look for in Grafana
TASK_CREATED = Counter('task_created_total', 'Total Tasks Created')
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
cache = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@app.route('/')
def index():
    REQUEST_COUNT.inc()
    hits = cache.incr('hits')
    return jsonify({"status": "online", "hits": hits})

# ADD THIS ROUTE:
@app.route('/task', methods=['GET', 'POST'])
def handle_task():
    REQUEST_COUNT.inc()
    if request.method == 'POST':
        TASK_CREATED.inc() # This is what Grafana will graph!
        data = request.json
        task_name = data.get("task", "unknown")
        cache.lpush("task_list", task_name)
        return jsonify({"message": "Task created", "task": task_name}), 201
    
    tasks = cache.lrange("task_list", 0, -1)
    return jsonify({"tasks": tasks}), 200

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)