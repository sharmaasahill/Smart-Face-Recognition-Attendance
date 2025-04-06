from flask import Flask, jsonify, request, session
from flask_cors import CORS
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import os
import shutil

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session handling
CORS(app)  # Enable Cross-Origin Resource Sharing

DB_NAME = "attendance.db"
DATASET_DIR = "dataset"

# Temporary storage for OTPs
otp_storage = {}

# Email Configuration
EMAIL_ADDRESS = "i.sahilkrsharma@gmail.com"
EMAIL_PASSWORD = "kcpj idcc mfhu jydy"
ADMIN_EMAIL = "i.sahilkrsharma@gmail.com"


@app.route("/")
def home():
    return "Welcome to Smart Face Recognition Attendance API"


# Fetch all attendance logs
@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, date, time FROM attendance ORDER BY date DESC, time DESC")
    rows = cursor.fetchall()
    conn.close()

    attendance_list = [{"id": row[0], "name": row[1], "date": row[2], "time": row[3]} for row in rows]
    return jsonify(attendance_list)


# Delete an attendance entry by ID
@app.route('/api/attendance/<int:attendance_id>', methods=['DELETE'])
def delete_attendance(attendance_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance WHERE id = ?", (attendance_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Attendance record deleted successfully"}), 200


# Generate OTP and send via email
@app.route("/api/generate-otp", methods=["POST"])
def generate_otp():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
    otp_storage[username] = otp  # Store OTP temporarily

    if send_otp_email(username, otp):
        return jsonify({"message": "OTP sent successfully!"})
    else:
        return jsonify({"error": "Failed to send OTP"}), 500


# Verify OTP
@app.route("/api/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    username = data.get("username")
    entered_otp = data.get("otp")

    if username in otp_storage and otp_storage[username] == entered_otp:
        del otp_storage[username]  # Remove OTP after verification
        return jsonify({"message": "OTP verified successfully!"})
    else:
        return jsonify({"error": "Invalid OTP"}), 401


# Send OTP via Email
def send_otp_email(username, otp):
    """Send OTP via email."""
    subject = "Your Admin Login OTP"
    body = f"Your One-Time Password (OTP) is: {otp}\n\nUse this to log in."

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, ADMIN_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send OTP: {e}")
        return False


# Register new user: Capture dataset + Train model
@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"success": False, "message": "Name is required"}), 400

    try:
        print(f"[INFO] Registering new user: {name}")

        # Run dataset capture
        subprocess.run(["python", "backend/capture_dataset.py", name], check=True)

        # Retrain model
        subprocess.run(["python", "backend/train_model.py"], check=True)

        return jsonify({"success": True, "message": f"User '{name}' registered successfully!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


# =============================
# NEW FEATURE: Manage Users
# =============================

# List all registered users (folders in dataset/)
@app.route("/api/users", methods=["GET"])
def list_users():
    try:
        users = [d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))]
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": f"Failed to list users: {str(e)}"}), 500


# Delete a registered user (delete dataset folder & retrain)
@app.route("/api/users/<username>", methods=["DELETE"])
def delete_user(username):
    try:
        user_folder = os.path.join(DATASET_DIR, username)

        if not os.path.exists(user_folder):
            return jsonify({"error": "User not found"}), 404

        # Delete folder
        shutil.rmtree(user_folder)

        # Retrain model
        subprocess.run(["python", "backend/train_model.py"], check=True)

        return jsonify({"message": f"User '{username}' deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to delete user: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
