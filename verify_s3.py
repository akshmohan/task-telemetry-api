import boto3
from botocore.exceptions import NoCredentialsError

# Connect to LocalStack S3
s3 = boto3.client(
    's3',
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

BUCKET_NAME = "task-telemetry-storage"

def verify():
    print(f"--- Verifying Phase 3 Infrastructure ---")
    try:
        # 1. Check if bucket exists
        buckets = s3.list_buckets()
        bucket_names = [b['Name'] for b in buckets['Buckets']]
        
        if BUCKET_NAME in bucket_names:
            print(f"✅ Found bucket: {BUCKET_NAME}")
            
            # 2. Try to write a small file to it
            s3.put_object(Bucket=BUCKET_NAME, Key="test.txt", Body="Terraform-LocalStack Integration Works!")
            print(f"✅ Successfully wrote test object to {BUCKET_NAME}")
            
            # 3. Clean up
            s3.delete_object(Bucket=BUCKET_NAME, Key="test.txt")
            print(f"✅ Phase 3 Verification Successful!")
        else:
            print(f"❌ Error: Bucket '{BUCKET_NAME}' not found in LocalStack.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("Make sure LocalStack is running: 'localstack start -d'")

if __name__ == "__main__":
    verify()