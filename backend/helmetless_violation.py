from ultralytics import YOLO
import cv2
import os
import mediapipe as mp
from violation_logger import log_violation
from snapshot_manager import save_snapshot_with_cooldown

model = YOLO("best.pt")
print(model.names)

mp_face = mp.solutions.face_detection
face_detector = mp_face.FaceDetection(min_detection_confidence=0.5)

cap = cv2.VideoCapture("INPUT_VIDEO.mp4")
width, height = int(cap.get(3)), int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

out = cv2.VideoWriter(
    "outputs/helmetless__output.mp4",
    cv2.VideoWriter_fourcc(*'mp4v'),
    fps, (width, height)
)

os.makedirs("outputs", exist_ok=True)
os.makedirs("helmetless_snaps", exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.5)[0]

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        cropped = frame[y1:y2, x1:x2]
        if cropped.size == 0:
            continue

        rgb_crop = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
        face_result = face_detector.process(rgb_crop)
        face_visible = face_result.detections is not None

        if class_name == "helmetless" and face_visible:
            label = "Helmetless"
            color = (0, 128, 128)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # ✅ save only once every 5 seconds
            snap_path = save_snapshot_with_cooldown(
                frame=cropped,
                folder="helmetless_snaps",
                prefix="helmetless",
                cooldown_seconds=5,
                violation_key="helmetless"
            )

            if snap_path:
                log_violation("helmetless", snap_path, track_id="NA", plate="UNKNOWN")

    out.write(frame)

cap.release()
out.release()
face_detector.close()
print("✅ Helmetless output saved: outputs/helmetless__output.mp4")
