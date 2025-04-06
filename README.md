<h1 align="center">🎓 Smart Face Recognition Attendance System 🎥</h1>

<p align="center">
  Real-time face recognition + liveness detection 🔐 with a slick React dashboard 🧑‍💻  
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-blue" />
  <img src="https://img.shields.io/badge/Real--Time-Zero%20Lag-green" />
  <img src="https://img.shields.io/badge/Liveness%20Detection-Enabled-brightgreen" />
  <img src="https://img.shields.io/badge/Secure-Admin%20Auth-orange" />
</p>

---

## 🚀 Key Features

✅ **Real-Time Face Recognition**  
✅ **Zero-Lag Liveness Detection** (blink, head, mouth)  
✅ **Anti-Spoofing Techniques**  
✅ **Admin Login + JWT Secured**  
✅ **Attendance Logging (SQLite)**  
✅ **Interactive React Dashboard**  
✅ **Face Image Management** (Delete Users)  
✅ **Fully Optimized Using OpenCV**  

---

## 🧠 Liveness Detection - How It Works

The system ensures **real presence** using:

🔹 **Blink Detection**  
🔹 **Head Movement Detection** (left/right & up/down)  
🔹 **Mouth Movement Tracking**

Only after successful checks, attendance is marked as:  
✅ `Liveness: Real` (No spoofing possible!)

---

## 📊 Web Dashboard (React + Tailwind)

👨‍💼 **Admin Features**:
- 🔐 Login securely
- 🕒 View all attendance entries
- 🧍‍♂️ See face thumbnails
- 🗑️ Delete specific registered users

Responsive, modern, and super intuitive.

---

## 📸 How To Run the Project

> Backend, Live Recognition & Dashboard — all in sync!

1. **Start Backend (Flask API)**  
   ```bash
   python backend/api.py
   ```

2. **Start Live Face Recognition System**  
   ```bash
   python backend/live_face_recognition.py
   ```

3. **Run the React Dashboard**  
   ```bash
   cd attendance-dashboard
   npm install
   npm start
   ```

Open `http://localhost:3000` to explore the dashboard 💻

---

## ⚙️ System Flow (Behind the Scenes)

```mermaid
graph TD;
    A[Webcam Initialized] --> B[Face Detected using OpenCV];
    B --> C[Landmarks Identified using face_recognition];
    C --> D[Liveness Detection (Blink, Head, Mouth)];
    D --> E[Encoding Matched with Known Faces];
    E --> F[Attendance Marked if Liveness = Real];
    F --> G[Data Stored in SQLite];
    G --> H[Dashboard Fetches & Displays Data via REST API];
    H --> I[Admin Manages Users and Logs];
```

---

## 🧩 Tech Stack

| Layer     | Technologies |
|-----------|--------------|
| 🎨 Frontend | React.js, Tailwind CSS, Axios, React Router |
| 🔙 Backend | Flask, Flask-CORS, Flask-JWT, SQLite3 |
| 🧠 AI/ML   | OpenCV, face_recognition, dlib landmarks, numpy |
| 💾 Database | SQLite (with SQLAlchemy ORM) |
| 🛡️ Security | JWT Tokens, Bcrypt Password Hashing |

---

## 📁 Data Handling

- 📂 `known_faces/` - stores face images  
- 🧠 `encodings.pickle` - stores face encodings  
- 📄 `attendance.db` - logs timestamped attendance  
- 🧼 Deletes removed users from both disk & memory

---

## 🛡️ Security

- 🔐 JWT Token Authentication for Admin
- 🔒 Bcrypt Password Hashing
- 🔜 2FA (Two-Factor Authentication) – Coming Soon!

---

## 📌 Roadmap

- [x] Zero-lag liveness detection with anti-spoofing
- [x] Admin dashboard to view/delete users & logs
- [x] JWT-secured admin login system
- [ ] Export Logs to CSV/PDF
- [ ] Cloud Deployment (with webcam access)
- [ ] Email/SMS Alerts on Attendance
- [ ] Multi-user admin access
- [ ] Graphs for attendance trends
- [ ] Webcam feed preview on dashboard

---

## 👨‍🎓 About the Developer

**Sahil Sharma**  
Final Year B.Tech Student  
🎯 Passionate about AI, ML, and Secure System Design

---

## ⭐️ Show Some Love!

If you like this project, leave a ⭐ on [GitHub](#)  
Or drop a message — I'd love to hear your feedback!

---