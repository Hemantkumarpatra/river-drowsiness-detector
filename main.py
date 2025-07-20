import cv2
import mediapipe as mp
import numpy as np
import pygame

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Load alarm sound
ALARM_SOUND = "alarm.wav"
alarm_playing = False

# FaceMesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def calculate_ear(eye_points):
    A = euclidean(eye_points[1], eye_points[5])
    B = euclidean(eye_points[2], eye_points[4])
    C = euclidean(eye_points[0], eye_points[3])
    return (A + B) / (2.0 * C)

# Drowsiness detection thresholds
EAR_THRESHOLD = 0.20
CLOSED_FRAMES = 15
frame_count = 0

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        landmarks = result.multi_face_landmarks[0].landmark
        left_eye = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in LEFT_EYE]
        right_eye = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in RIGHT_EYE]

        left_ear = calculate_ear(left_eye)
        right_ear = calculate_ear(right_eye)
        avg_ear = (left_ear + right_ear) / 2.0

        # Draw eye points
        for x, y in left_eye + right_eye:
            cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)

        cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if avg_ear < EAR_THRESHOLD:
            frame_count += 1
            if frame_count >= CLOSED_FRAMES and not alarm_playing:
                print("🔔 Drowsiness detected! Playing alarm.")
                pygame.mixer.music.load(ALARM_SOUND)
                pygame.mixer.music.play(-1)
                alarm_playing = True
        else:
            frame_count = 0
            if alarm_playing:
                print("✅ Eyes opened. Stopping alarm.")
                pygame.mixer.music.stop()
                alarm_playing = False

    cv2.imshow("Driver Drowsiness Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
