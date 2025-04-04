import sqlite3
import os
import datetime

# Define database and log file paths
DB_PATH = "../models/attendance.db"
CSV_PATH = "../attendance_log.csv"

def initialize_database():
    """Creates the attendance table if it doesn't exist."""
    if not os.path.exists("../models"):
        os.makedirs("../models")  # Ensure models directory exists

    conn = sqlite3.connect(DB_PATH)
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
    print("✅ Database initialized successfully.")

def log_attendance(name):
    """Logs attendance in both CSV and SQLite database."""
    now = datetime.datetime.now()
    date, time = now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")

    # Log to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
    conn.commit()
    conn.close()
    
    # Log to CSV file
    with open(CSV_PATH, "a") as log:
        log.write(f"{name},{date},{time}\n")

    print(f"✅ Attendance logged: {name} at {date} {time}")

if __name__ == "__main__":
    initialize_database()  # Run this once to ensure table exists
