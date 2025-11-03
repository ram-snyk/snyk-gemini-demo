"""
Main Application - SECURE VERSION
This is the production code with proper security practices.
"""

from flask import Flask, request, jsonify, abort
import subprocess
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# SECURE: Load secrets from environment
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0.0'})

@app.route('/api/ping', methods=['POST'])
def ping():
    """
    SECURE: Ping endpoint with proper validation
    """
    data = request.get_json()
    host = data.get('host', 'localhost')
    
    # SECURE: Strict validation of hostname
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        abort(400, 'Invalid hostname format')
    
    # SECURE: Prevent internal network access
    if any(x in host.lower() for x in ['localhost', '127.', '192.168.', '10.', '172.']):
        abort(400, 'Cannot ping internal addresses')
    
    try:
        # SECURE: Use list instead of shell=True to prevent command injection
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '1', host],
            capture_output=True,
            text=True,
            timeout=2
        )
        
        return jsonify({
            'host': host,
            'reachable': result.returncode == 0,
            'output': result.stdout[:200]
        })
    except subprocess.TimeoutExpired:
        abort(408, 'Ping timeout')
    except Exception as e:
        abort(500, f'Ping failed: {str(e)}')

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    """Example endpoint with secure parameter handling"""
    # Using type hints (int) provides basic validation
    if user_id < 1:
        abort(400, 'Invalid user ID')
    
    # In production, this would query a database securely
    return jsonify({
        'id': user_id,
        'username': f'user_{user_id}'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
