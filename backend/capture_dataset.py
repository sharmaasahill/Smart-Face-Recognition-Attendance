import cv2
import os
import sys

def capture_images(name, count=20):
    save_dir = f"dataset/{name}"
    os.makedirs(save_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    img_count = 0
    print(f"[INFO] Starting capture for: {name}")

    while img_count < count:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            img_name = os.path.join(save_dir, f"{img_count}.jpg")
            face = frame[y:y+h, x:x+w]
            cv2.imwrite(img_name, face)
            img_count += 1

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Captured: {img_count}/{count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow("Capturing Faces", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"[INFO] Saved {img_count} images to {save_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] Please provide a username as a command-line argument.")
        sys.exit(1)
    username = sys.argv[1]
    capture_images(username)
