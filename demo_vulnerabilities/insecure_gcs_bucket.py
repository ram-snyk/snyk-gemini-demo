"""
✅ SECURE CODE - FOR LIVE DEMO ONLY ✅

This file demonstrates creating a private Google Cloud Storage (GCS) bucket,
which is a security best practice.

USE THIS DURING THE LIVE DEMO to show:
1. How to fix insecure GCS bucket configurations.
2. Best practices for creating GCS buckets.
"""

from google.cloud import storage

def create_private_gcs_bucket(bucket_name):
    """
    Creates a new GCS bucket with security best practices.
    """
    storage_client = storage.Client()

    # ✅ SECURE: Enforce uniform bucket-level access
    # This ensures that access control is consistent across the bucket.
    bucket = storage_client.bucket(bucket_name)
    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.create()


    print(f"Bucket {bucket.name} created with uniform bucket-level access.")
    print("This is a secure configuration.")

    return bucket

if __name__ == '__main__':
    # This is for demonstration purposes. In a real application,
    # the bucket name should not be hardcoded.
    # Replace 'your-unique-bucket-name' with a globally unique bucket name.
    # For the demo, we can use a placeholder.
    demo_bucket_name = "gemini-demo-private-bucket-12345"
    print("✅ This script creates a private GCS bucket with security best practices.")
    try:
        create_private_gcs_bucket(demo_bucket_name)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("This might be due to permissions or the bucket name already existing.")
