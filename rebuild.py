import subprocess
import sys

def run(cmd):
    print(f">> {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Command failed. Stopping.")
        sys.exit(1)

# 1. Build the image with the NEW name 'flask-telemetry'
run("docker build -t flask-telemetry:latest ./app")

# 2. Load it into Kind
run("kind load docker-image flask-telemetry:latest")

# 3. Apply all K8s changes (including the PVC and updated Deployment)
run("kubectl apply -f k8s/")

# 4. Force restart the Flask pods to use the new image
run("kubectl rollout restart deployment flask-deployment")

print("\n✅ Successfully updated your cluster!")