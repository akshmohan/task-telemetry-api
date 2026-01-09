import requests
import time
import random

# Point this to your NodePort from Step #4 in main.tf
API_URL = "http://localhost:30001/task"

tasks = ["Buy milk", "Finish Terraform", "Master Kubernetes", "Deploy to Cloud", "Drink Coffee"]

def run_test(iterations=10):
    print(f"🚀 Starting verification on {API_URL}...")
    for i in range(iterations):
        task = random.choice(tasks)
        try:
            # 1. Test the POST (Writes to Redis)
            res = requests.post(API_URL, json={"task": task})
            
            # 2. Test the GET (Reads from Redis)
            get_res = requests.get(API_URL)
            
            print(f"Iteration {i+1}: Created '{task}' -> Status: {res.status_code}")
            time.sleep(1) # Wait 1 sec so the graph looks better
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_test(15) # Generate 15 data points
    print("\n✅ Done. Now check Grafana for 'task_created_total'!")