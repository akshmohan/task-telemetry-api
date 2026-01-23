import boto3
import sys

# Since you are in Trivandrum
REGION = "ap-south-1"

def nuke_s3():
    s3 = boto3.resource('s3', region_name=REGION)
    print("Checking for S3 Buckets...")
    for bucket in s3.buckets.all():
        if "task-telemetry" in bucket.name:
            print(f"⚠️ Found project bucket: {bucket.name}. Emptying and deleting...")
            bucket.objects.all().delete()
            bucket.delete()
            print(f"✅ Deleted {bucket.name}")

def nuke_eks():
    eks = boto3.client('eks', region_name=REGION)
    print("Checking for EKS Clusters...")
    clusters = eks.list_clusters()['clusters']
    for cluster in clusters:
        print(f"☢️  DELETING CLUSTER: {cluster}. This takes ~15 minutes.")
        eks.delete_cluster(name=cluster)

if __name__ == "__main__":
    confirm = input("This will DELETE project resources in REAL AWS. Type 'nuke' to proceed: ")
    if confirm == "nuke":
        nuke_s3()
        nuke_eks()
        print("--- Cleanup Process Initiated ---")
    else:
        print("Aborted.")