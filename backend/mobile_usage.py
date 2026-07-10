import cv2
import numpy as np
import os
import csv
from math import dist
from collections import deque
from datetime import timedelta
from mediapipe.python.solutions.pose import Pose
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from mediapipe.python.solutions.pose import POSE_CONNECTIONS
from mediapipe.python.solutions.drawing_styles import get_default_pose_landmarks_style
from snapshot_manager import save_snapshot_with_cooldown
from violation_logger import log_violation

VIDEO_PATH = "mobile_input.mp4"
OUTPUT_PATH = "outputs/output_mobile.mp4"
SNAPSHOT_DIR = "mobile_use_snaps"
CSV_LOG = "logs/mobile_violations.csv"

HAND_EAR_DISTANCE = 120
PERSISTENCE_THRESHOLD = 5
SMOOTH_HISTORY = 5

os.makedirs("outputs", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

cap = cv2.VideoCapture(VIDEO_PATH)
w, h = int(cap.get(3)), int(cap.get(4))
fps = cap.get(cv2.CAP_PROP_FPS)

out = cv2.VideoWriter(OUTPUT_PATH, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
pose = Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5)

frame_count = 0
violation_history = deque(maxlen=PERSISTENCE_THRESHOLD)
box_history = deque(maxlen=SMOOTH_HISTORY)

with open(CSV_LOG, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Frame", "Timestamp", "Box_x1", "Box_y1", "Box_x2", "Box_y2", "Snapshot_Path"])

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        timestamp = str(timedelta(seconds=frame_count / fps))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        if result.pose_landmarks:
            lm = result.pose_landmarks.landmark

            def to_xy(pt):
                return int(pt.x * w), int(pt.y * h)

            lh, rh = to_xy(lm[15]), to_xy(lm[16])
            le, re = to_xy(lm[7]), to_xy(lm[8])

            distances = [dist(lh, le), dist(rh, re), dist(lh, re), dist(rh, le)]
            hand_near_ear = any(d < HAND_EAR_DISTANCE for d in distances)

            violation_history.append(hand_near_ear)

            draw_landmarks(frame, result.pose_landmarks, POSE_CONNECTIONS,
                           get_default_pose_landmarks_style())

            if all(violation_history):
                xs = [pt.x for pt in lm]
                ys = [pt.y for pt in lm]
                x1, x2 = int(min(xs) * w), int(max(xs) * w)
                y1, y2 = int(min(ys) * h), int(max(ys) * h)

                box_history.append([x1, y1, x2, y2])
                avg_box = np.mean(box_history, axis=0).astype(int).tolist()

                cv2.rectangle(frame, (avg_box[0], avg_box[1]), (avg_box[2], avg_box[3]), (128, 0, 255), 3)
                cv2.putText(frame, "Confirmed Mobile Use", (avg_box[0], avg_box[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                snap_name = save_snapshot_with_cooldown(
                    frame=frame,
                    folder=SNAPSHOT_DIR,
                    prefix="mobile_use",
                    cooldown_seconds=6,
                    violation_key="mobile_usage"
                )

                if snap_name:
                    writer.writerow([frame_count, timestamp, avg_box[0], avg_box[1], avg_box[2], avg_box[3], snap_name])
                    log_violation("mobile_usage", snap_name, track_id="NA", plate="UNKNOWN")

        out.write(frame)

cap.release()
out.release()
pose.close()

print(f"✅ Mobile usage output saved: {OUTPUT_PATH}")
