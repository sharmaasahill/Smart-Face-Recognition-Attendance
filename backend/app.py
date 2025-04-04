from flask import Flask, request, jsonify
import face_recognition
import os
import datetime
from database import log_attendance

app = Flask(__name__)

# Load known faces
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get backend folder path
KNOWN_FACES_DIR = os.path.join(BASE_DIR, "../dataset/")  # Absolute path
known_face_encodings = []
known_face_names = []

for filename in os.listdir(KNOWN_FACES_DIR):
    image_path = os.path.join(KNOWN_FACES_DIR, filename)
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)
    if encoding:
        known_face_encodings.append(encoding[0])
        known_face_names.append(os.path.splitext(filename)[0])
        
@app.route('/')
def home():
    return "Smart Face Recognition Attendance System is Running!"


@app.route('/recognize', methods=['POST'])
def recognize_face():
    file = request.files['image']
    image = face_recognition.load_image_file(file)
    unknown_encoding = face_recognition.face_encodings(image)

    if not unknown_encoding:
        return jsonify({"message": "No face detected"}), 400

    matches = face_recognition.compare_faces(known_face_encodings, unknown_encoding[0])
    name = "Unknown"

    if True in matches:
        matched_index = matches.index(True)
        name = known_face_names[matched_index]
        log_attendance(name)  # Store attendance in the database

    return jsonify({"name": name})

if __name__ == '__main__':
    app.run(debug=True)
