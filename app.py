from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import psycopg2
from db_config import DB_CONFIG
import os

app = Flask(__name__)
CORS(app)

# Serve static files
@app.route('/')
def index():
    return send_from_directory('.', 'login.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# Login API endpoint
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        # Connect to database
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Check credentials
        cursor.execute(
            "SELECT id, username, email, full_name FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute(
                "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s",
                (user[0],)
            )
            connection.commit()
            
            cursor.close()
            connection.close()
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'full_name': user[3]
                },
                'redirectUrl': '/dashboard.html'
            }), 200
        else:
            cursor.close()
            connection.close()
            
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({
            'success': False,
            'message': 'Server error occurred'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
