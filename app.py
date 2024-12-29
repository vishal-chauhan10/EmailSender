from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename
from send_emails import send_emails
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app, 
     resources={r"/*": {"origins": "*"}},  # Allow all origins during development
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

app.secret_key = 'dev-key-for-testing-only'

# Admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# Upload folder configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        return response

    print("Received login request")  # Debug log
    print("Request data:", request.get_json())  # Debug log

    try:
        data = request.get_json()
        if not data:
            print("No JSON data received")  # Debug log
            return jsonify({
                'success': False,
                'message': 'No data received'
            }), 400

        username = data.get('username')
        password = data.get('password')
        
        print(f"Login attempt - Username: {username}, Password: {password}")

        if username == "admin" and password == "admin123":
            session['logged_in'] = True
            print("Login successful")
            return jsonify({
                'success': True,
                'message': 'Login successful'
            })
        else:
            print("Invalid credentials")
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            })
            
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'logged_in' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'message': 'No file selected'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Create upload folder if it doesn't exist
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            file.save(filepath)
            
            # Read and validate CSV
            try:
                df = pd.read_csv(filepath)
                if 'Email' not in df.columns:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    return jsonify({'message': 'CSV must contain an Email column'}), 400
                
                # Store file path in session
                session['csv_file'] = filepath
                recipients = df['Email'].tolist()
                session['recipients'] = recipients
                
                return jsonify({
                    'message': 'File uploaded successfully',
                    'recipients': recipients
                }), 200
            
            except Exception as e:
                if os.path.exists(filepath):
                    os.remove(filepath)
                return jsonify({'message': f'Error processing CSV: {str(e)}'}), 500
    
    # For GET request, return current recipients if any
    recipients = session.get('recipients', [])
    return jsonify({'recipients': recipients})

@app.route('/send-emails', methods=['POST'])
def send_emails_route():
    if 'logged_in' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    
    if 'csv_file' not in session:
        return jsonify({'message': 'Please upload a CSV file first'}), 400
    
    try:
        send_emails(session['csv_file'])
        
        # Clean up
        if os.path.exists(session['csv_file']):
            os.remove(session['csv_file'])
        session.pop('csv_file', None)
        session.pop('recipients', None)
        
        return jsonify({'message': 'Emails sent successfully'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Error sending emails: {str(e)}'}), 500

@app.errorhandler(Exception)
def handle_error(error):
    print(f"Error: {str(error)}")
    response = {
        "status": "error",
        "message": str(error)
    }
    return jsonify(response), getattr(error, 'code', 500)

if __name__ == '__main__':
    # Enable debug mode and specify host to allow external connections
    app.run(debug=True, host='0.0.0.0', port=5001) 