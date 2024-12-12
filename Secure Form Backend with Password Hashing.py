import os
import uuid
import hashlib
import secrets
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'submissions'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_salt():
    """Generate a secure random salt."""
    return secrets.token_hex(16)

def hash_password(password, salt=None):
    """
    Securely hash a password using SHA-256 with optional salt.
    
    Args:
        password (str): Plain text password
        salt (str, optional): Salt for additional security
    
    Returns:
        tuple: (hashed_password, salt)
    """
    if salt is None:
        salt = generate_salt()
    
    # Combine password and salt, then hash
    salted_password = f"{password}{salt}"
    hashed_password = hashlib.sha256(salted_password.encode('utf-8')).hexdigest()
    
    return hashed_password, salt

def verify_password(stored_password, stored_salt, input_password):
    """
    Verify if the input password matches the stored hashed password.
    
    Args:
        stored_password (str): Previously hashed password
        stored_salt (str): Salt used in original hashing
        input_password (str): Password to verify
    
    Returns:
        bool: True if password matches, False otherwise
    """
    hashed_input, _ = hash_password(input_password, stored_salt)
    return hashed_input == stored_password

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        # Collect form data
        form_data = request.form.to_dict()
        
        # Check if password fields exist and hash them
        password_fields = [
            'password', 
            'admin_password', 
            'form_password'
        ]
        
        for field in password_fields:
            if field in form_data:
                # Hash the password
                hashed_password, salt = hash_password(form_data[field])
                
                # Replace original password with hashed version
                form_data[f'{field}_hash'] = hashed_password
                form_data[f'{field}_salt'] = salt
                del form_data[field]  # Remove plain text password
        
        # Generate unique filename with timestamp and UUID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())
        filename = f'{UPLOAD_FOLDER}/submission_{timestamp}_{unique_id}.xlsx'
        
        # Convert to DataFrame and save to Excel
        df = pd.DataFrame([form_data])
        df.to_excel(filename, index=False)
        
        return jsonify({
            'status': 'success', 
            'message': 'Form submitted securely',
            'filename': filename
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 500

@app.route('/verify-password', methods=['POST'])
def verify_form_password():
    """
    Endpoint to verify passwords securely.
    
    Supports multiple password verification scenarios.
    """
    data = request.json
    
    try:
        # Extract password and verification details
        input_password = data.get('password')
        stored_hash = data.get('stored_hash')
        stored_salt = data.get('stored_salt')
        
        if not all([input_password, stored_hash, stored_salt]):
            return jsonify({
                'status': 'error',
                'message': 'Incomplete verification data'
            }), 400
        
        # Verify password
        is_valid = verify_password(stored_hash, stored_salt, input_password)
        
        return jsonify({
            'status': 'success',
            'valid': is_valid
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)