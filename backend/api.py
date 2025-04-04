from flask import Flask, jsonify, request, session
from flask_cors import CORS
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session handling
CORS(app)  # Enable Cross-Origin Resource Sharing

DB_NAME = "attendance.db"

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
    msg["To"] = ADMIN_EMAIL  # Updated to correct recipient email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, ADMIN_EMAIL, msg.as_string())  # Corrected recipient
        server.quit()
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send OTP: {e}")
        return False


if __name__ == '__main__':
    app.run(debug=True)
