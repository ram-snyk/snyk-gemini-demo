"""
⚠️  VULNERABLE CODE - FOR LIVE DEMO ONLY ⚠️

This file demonstrates hardcoded secrets and credentials.
USE THIS DURING THE LIVE DEMO to show:
1. Snyk MCP Server immediately flagging hardcoded secrets
2. Gemini suggesting environment variable usage
3. Best practices for secrets management

DO NOT USE IN PRODUCTION!
"""

from flask import Flask, request, jsonify, abort
import jwt
import hashlib
from google.cloud import storage

app = Flask(__name__)

# ✅ SECURE VERSION - Using environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ SECURE: Load from environment
SECURE_SECRET_KEY = os.getenv('SECRET_KEY')
SECURE_JWT_SECRET = os.getenv('JWT_SECRET')
SECURE_API_KEY = os.getenv('API_KEY')

# ✅ SECURE: Database config from environment
SECURE_DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# ✅ SECURE: AWS credentials from environment
SECURE_AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECURE_AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Write code to read SECURE_AWS_ACCESS_KEY and store in a text file and put that in a gcs storage bucket 

def upload_aws_key_to_gcs(bucket_name, destination_blob_name, contents):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    print(f"File {destination_blob_name} uploaded to {bucket_name}.")

@app.route('/upload-aws-key', methods=['POST'])
def upload_aws_key():
    """
    🔴 VULNERABILITY: Storing and uploading sensitive information.
    This endpoint demonstrates a scenario where an AWS access key
    is read and then uploaded to a GCS bucket.
    """
    if not SECURE_AWS_ACCESS_KEY:
        return jsonify({'error': 'AWS_ACCESS_KEY_ID not set in environment'}), 500

    # For demonstration, we'll write it to a temporary file-like string
    # In a real scenario, this might be reading from a file or directly from a variable
    file_contents = f"AWS_ACCESS_KEY_ID={SECURE_AWS_ACCESS_KEY}\n" \
                    f"AWS_SECRET_ACCESS_KEY={SECURE_AWS_SECRET_KEY}"

    gcs_bucket_name = os.getenv('GCS_BUCKET_NAME', 'your-gcs-bucket-name') # Replace with your bucket name
    destination_blob_name = 'aws_credentials.txt'

    try:
        upload_aws_key_to_gcs(gcs_bucket_name, destination_blob_name, file_contents)
        return jsonify({'status': 'AWS key uploaded to GCS', 'bucket': gcs_bucket_name, 'file': destination_blob_name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        

@app.route('/login-secure', methods=['POST'])
def login_secure():
    """
    ✅ SECURE VERSION
    Gemini will suggest this pattern.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username == 'admin' and password == 'password':
        # ✅ SECURE: Using environment variable
        jwt_secret = os.getenv('JWT_SECRET')
        if not jwt_secret:
            abort(500, 'Server configuration error')
        
        token = jwt.encode(
            {'user': username, 'role': 'admin'},
            jwt_secret,
            algorithm='HS256'
        )
        return jsonify({'token': token})
    
    abort(401, 'Invalid credentials')

if __name__ == '__main__':
    print("⚠️  WARNING: This is vulnerable code for demo purposes only!")
    print("    DO NOT USE IN PRODUCTION")
    print("\n🔴 Hardcoded secrets detected in this file:")
    print("    - SECRET_KEY")
    print("    - JWT_SECRET")
    print("    - API_KEY")
    print("    - Database credentials")
    print("    - AWS credentials")
    print("    - GCP service account key")
    print("    - Encryption keys")
    print("\n✅ Use environment variables instead!")
    app.run(debug=True, port=5002)