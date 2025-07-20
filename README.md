# Driver Drowsiness Detector 🚗😴

This is a real-time drowsiness detection system that monitors a driver's eyes using a webcam and triggers an alarm if the eyes remain closed for too long.

---

## 💡 Features

- Real-time face & eye detection using **MediaPipe**
- Calculates **Eye Aspect Ratio (EAR)**
- Raises alarm when drowsiness is detected
- Alarm automatically stops when eyes open
- Simple interface using OpenCV window

---

## 🧰 Tech Stack

- Python 3.10 / 3.11
- OpenCV
- MediaPipe
- NumPy
- Pygame (for alarm sound)

---

## 🚀 How to Run

### 1. Clone this repo

```bash
git clone https://github.com/Hemantkumarpatra/driver-drowsiness-detector.git
cd driver-drowsiness-detector

### 2. Create Virtual Environment
python -m venv venv
.\venv\Scripts\activate

### 3.Install dependencies
pip install -r requirements.txt

### 4.Run the app
python main.py


🏁 Output
You’ll see:

Live webcam window with eye landmarks

EAR displayed in top-left

Alarm sound when drowsiness is detected

