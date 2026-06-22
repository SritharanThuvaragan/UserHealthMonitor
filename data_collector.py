# data_collector.py
"""Simple data collector for UserHealthMonitor.
Records a short 10‑second webcam session, extracts dummy posture/eye features,
and writes them to `dataset/processed/collection.csv`.
Replace dummy extraction with actual MediaPipe pipeline later.
"""
import cv2, time, os, pandas as pd, random

# Ensure output folder exists
output_dir = os.path.join(os.path.dirname(__file__), "dataset", "processed")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "collection.csv")

# Open webcam (default index 0)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Webcam could not be opened")

start = time.time()
records = []
while time.time() - start < 10:  # record for 10 seconds
    ret, frame = cap.read()
    if not ret:
        continue
    # Dummy feature extraction – replace with real MediaPipe calculations
    neck_angle = random.uniform(20, 70)
    shoulder_diff = random.uniform(0, 30)
    eye_aspect = random.uniform(0.2, 0.4)
    distance_cm = random.uniform(30, 70)
    lighting = random.uniform(40, 120)
    timestamp = time.time()
    records.append({
        "timestamp": timestamp,
        "neck_angle": neck_angle,
        "shoulder_diff": shoulder_diff,
        "eye_aspect": eye_aspect,
        "distance_cm": distance_cm,
        "lighting": lighting,
    })
    time.sleep(0.05)

cap.release()

df = pd.DataFrame(records)
df.to_csv(output_path, index=False)
print(f"Collected {len(df)} rows – saved to {output_path}")
