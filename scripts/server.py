import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pdf_process import process_pdf
import bcrypt
from cryptography.fernet import Fernet

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '../data'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Generate an encryption key for the user password
key = Fernet.generate_key()
cipher = Fernet(key)

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": []}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_admin(username, password):
    users_data = load_users()
    for user in users_data.get("users", []):
        if user["username"] == username:
            return bcrypt.checkpw(password.encode('utf-8'),cipher.decrypt(user["password"].encode('utf-8')).decode('utf-8').encode('utf-8'))
    return False

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if is_admin(username, password):
        return jsonify({"status":"success", "message":"Admin user is logged in"}), 200
    else:
        return jsonify({"status":"error", "message":"Login failed"}), 401

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        #process the pdf
        processed_text = process_pdf(file_path)
        if processed_text is None:
            return jsonify({"status":"error", "message":"Could not process the pdf."}), 400

        return jsonify({"status": "success", "message": "File uploaded and processed", "text": processed_text}), 200
    return jsonify({"status": "error", "message": "Invalid file type"}), 400

#Register admin
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    users_data = load_users()
    for user in users_data.get("users", []):
        if user["username"] == username:
            return jsonify({"message": "User exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    encrypted_password = cipher.encrypt(hashed_password.decode('utf-8').encode('utf-8')).decode('utf-8')

    users_data["users"].append({"username": username, "password": encrypted_password})
    save_users(users_data)
    return jsonify({'message': 'Admin registered successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)