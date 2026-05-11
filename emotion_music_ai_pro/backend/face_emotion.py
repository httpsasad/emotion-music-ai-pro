import cv2
import numpy as np

def detect_emotion_from_face():
    # Load OpenCV pre-trained classifiers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    cap = cv2.VideoCapture(0)
    # Give camera time to warm up for better quality
    for _ in range(5):
        cap.read()
    
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return "relaxed"

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return "relaxed"

    # Analyze the first face found
    (x, y, w, h) = faces[0]
    roi_gray = gray[y:y+h, x:x+w]
    
    # SMILE DETECTION (FOR HAPPY/ROMANTIC)
    smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
    
    # EYE DETECTION (FOR INTENSITY/SADNESS)
    eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)

    # PRO LOGIC MAPPING
    if len(smiles) > 0:
        return "happy"
    
    if len(eyes) < 2:
        # Narrowing eyes often looks 'Intense' or 'Angry' - mapping to badmoshi
        return "badmoshi"
    
    # Check for vertical positioning of eyes (basic droop check)
    if len(eyes) >= 2:
        eye_y_avg = np.mean([e[1] for e in eyes])
        if eye_y_avg > (h * 0.4): # Eyes are lower than usual
            return "sad"

    return "relaxed"
