import subprocess
import sys

def run(cmd, desc):
    print(f"🚀 {desc}...")
    process = subprocess.run(cmd, shell=True)
    if process.returncode != 0:
        print(f"❌ FAILED: {desc}")
        sys.exit(1)

# --- CI TESTING PHASE ---
run("flake8 app/app.py --count --select=E9,F63,F7,F82 --show-source --statistics", "Linting Code")
run("python3 test_app.py", "Running Unit Tests")

# --- DEPLOYMENT PHASE ---
run("docker build -t flask-telemetry:latest ./app", "Building Docker image")
run("kind load docker-image flask-telemetry:latest", "Loading image into Kind")
run("kubectl apply -f k8s/", "Applying Kubernetes manifests")
run("kubectl rollout restart deployment/flask-deployment", "Restarting deployment")

print("\n✅ Tests Passed & Deployment Successful!")