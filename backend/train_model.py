import os
import face_recognition
import pickle
import cv2

def train_faces(dataset_dir = "dataset", model_file="encodings.pickle"):
    known_encodings = []
    known_names = []

    for name in os.listdir(dataset_dir):
        person_dir = os.path.join(dataset_dir, name)
        if not os.path.isdir(person_dir):
            continue

        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            image = cv2.imread(img_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            boxes = face_recognition.face_locations(rgb, model='hog')
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(name)

    data = {"encodings": known_encodings, "names": known_names}
    with open(model_file, "wb") as f:
        pickle.dump(data, f)

    print(f"[INFO] Training complete. Encodings saved to {model_file}")

if __name__ == "__main__":
    train_faces()