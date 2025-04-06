import cv2
import dlib
import face_recognition
import numpy as np
import sqlite3
import csv
import os
import time
import pickle
from datetime import datetime

# Database Setup
DB_NAME = "attendance.db"

def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''') 
    
    conn.commit()
    conn.close()
    print("[INFO] Database initialized successfully.")

def mark_attendance(name, is_real=True): 
    now = datetime.now()
    date_today = now.strftime("%Y-%m-%d")
    time_now = now.strftime("%H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if the person has already been marked today
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE name = ? AND date = ?", (name, date_today))
    duplicate_count = cursor.fetchone()[0]  

    is_duplicate = "Yes" if duplicate_count > 0 else ""  

    # Insert into database
    cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date_today, time_now))
    conn.commit()

    # Save to CSV
    csv_filename = "attendance.csv"
    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        
        if not file_exists:
            writer.writerow(["Name", "Date", "Time", "Duplicate", "Liveness"])  

        writer.writerow([name, date_today, time_now, is_duplicate, "Real" if is_real else "Fake"])  

    conn.close()
    print(f"[INFO] Attendance marked for {name} at {time_now} | Liveness: {'Real' if is_real else 'Fake'}")

# Initialize database
initialize_database()

# Load dlib's face detector and shape predictor
print("[INFO] Loading face detection model...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

# Load known face encodings from trained data
print("[INFO] Loading known face encodings...")
encodings_file = "encodings.pickle"
if not os.path.exists(encodings_file):
    print("[ERROR] Encodings not found. Please run train_model.py first.")
    exit()

with open(encodings_file, "rb") as f:
    data = pickle.load(f)
    known_faces = data["encodings"]
    known_names = data["names"]

print(f"[INFO] Loaded {len(known_names)} known faces.")

# Function to calculate Eye Aspect Ratio (EAR) for blinking detection
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])  
    B = np.linalg.norm(eye[2] - eye[4])  
    C = np.linalg.norm(eye[0] - eye[3])  
    return (A + B) / (2.0 * C)

# Initialize webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("[ERROR] Could not open webcam.")
    exit()

print("[INFO] Webcam initialized. Press 'q' to exit.")

blink_threshold = 0.2  
blink_count = 0      
blink_start_time = None  
blink_detected = False  

prev_nose_x, prev_nose_y = None, None
recognized_faces = set()
attendance_log = set()  

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("[ERROR] Failed to grab frame")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for rect, (top, right, bottom, left), face_encoding in zip(faces, face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"

        shape = predictor(gray, rect)
        landmarks = np.array([[p.x, p.y] for p in shape.parts()])
        left_eye = landmarks[36:42]
        right_eye = landmarks[42:48]
        left_EAR = eye_aspect_ratio(left_eye)
        right_EAR = eye_aspect_ratio(right_eye)
        avg_EAR = (left_EAR + right_EAR) / 2.0

        liveness_status = "Fake"  

        current_time = time.time()

        if avg_EAR < blink_threshold:
            if blink_start_time is None:
                blink_start_time = current_time  
            blink_count += 1
        else:
            if blink_start_time and (current_time - blink_start_time) <= 3:
                blink_detected = True  
                print("[INFO] Blink detected! Liveness confirmed.")
            blink_count = 0  
            blink_start_time = None  

        if blink_detected:
            liveness_status = "Real"

        nose_x, nose_y = landmarks[30]

        if prev_nose_x is not None and prev_nose_y is not None:
            dx = abs(nose_x - prev_nose_x)
            dy = abs(nose_y - prev_nose_y)

            movement = "Stable"
            if dx > 10:
                movement = "Head Moved Left/Right"
            elif dy > 10:
                movement = "Head Moved Up/Down"

            if movement != "Stable":
                print(f"[INFO] {movement} detected.")

        prev_nose_x, prev_nose_y = nose_x, nose_y

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

            if liveness_status == "Real":
                mark_attendance(name, is_real=True)
                attendance_log.add(f"{name} - {datetime.now().strftime('%H:%M:%S')}")
        else:
            if liveness_status == "Real":
                mark_attendance("Unknown", is_real=True)
                attendance_log.add(f"Unknown - {datetime.now().strftime('%H:%M:%S')}")

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} - {liveness_status}", (left, bottom + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    y_offset = 50
    for log in attendance_log:
        cv2.putText(frame, log, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        y_offset += 30  

    cv2.imshow("Face Recognition & Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Exiting system...")
        break

video_capture.release()
cv2.destroyAllWindows()
