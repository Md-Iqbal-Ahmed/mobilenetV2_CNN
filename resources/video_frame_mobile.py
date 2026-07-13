import cv2
import numpy as np
from tensorflow.keras.models import load_model

model_path = "C:/Users/user/Downloads/Test/fine_tuned_model_mobile.h5"
model = load_model(model_path)

labels = ['angry', 'happy', 'sad', 'neutral']

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
print("Webcam started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        
        roi_color = frame[y:y+h, x:x+w]
        roi_resized = cv2.resize(roi_color, (224, 224))             
        roi_normalized = roi_resized / 255.0                        
        roi_reshaped = np.reshape(roi_normalized, (1, 224, 224, 3)) 

        predictions = model.predict(roi_reshaped, verbose=0)
        pred_index = np.argmax(predictions)
        label = labels[pred_index] if pred_index < len(labels) else "unknown"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Facial Expression Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Webcam stopped.")
