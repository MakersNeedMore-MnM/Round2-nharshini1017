import cv2
import os
import argparse
from ultralytics import YOLO
from violation_logger import log_violation
from snapshot_manager import save_snapshot_with_cooldown

def calculate_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    return interArea / float(boxAArea + boxBArea - interArea + 1e-5)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, default='outputs/triple_riding_output.mp4')
    args = parser.parse_args()

    os.makedirs("outputs", exist_ok=True)
    os.makedirs("snapshots/triple_riding", exist_ok=True)

    model = YOLO("yolov8n.pt")
    PERSON_CLASS_ID = 0
    MOTORBIKE_CLASS_ID = 3

    cap = cv2.VideoCapture(args.input)
    frame_id = 0
    violation_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_id += 1
        results = model(frame, verbose=False)
        detections = results[0].boxes

        people = []
        bikes = []

        for box in detections:
            cls = int(box.cls.item())
            xyxy = box.xyxy.cpu().numpy()[0]
            if cls == PERSON_CLASS_ID:
                people.append(xyxy)
            elif cls == MOTORBIKE_CLASS_ID:
                bikes.append(xyxy)

        for i, bike_box in enumerate(bikes):
            nearby_people = []
            for person_box in people:
                iou = calculate_iou(person_box, bike_box)
                if iou > 0.05:
                    nearby_people.append(person_box)

            if len(nearby_people) >= 3:
                violation_count += 1
                annotated = frame.copy()

                cv2.rectangle(annotated, (int(bike_box[0]), int(bike_box[1])),
                              (int(bike_box[2]), int(bike_box[3])), (0, 255, 0), 2)
                cv2.putText(annotated, "Triple Riding Detected",
                            (int(bike_box[0]), int(bike_box[1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                for person_box in nearby_people:
                    cv2.rectangle(annotated, (int(person_box[0]), int(person_box[1])),
                                  (int(person_box[2]), int(person_box[3])), (0, 0, 255), 2)

                # ✅ save only once every 7 seconds
                snap_path = save_snapshot_with_cooldown(
                    frame=annotated,
                    folder="snapshots/triple_riding",
                    prefix="triple",
                    cooldown_seconds=7,
                    violation_key="triple_riding"
                )

                if snap_path:
                    log_violation("triple_riding", snap_path, track_id="NA", plate="UNKNOWN")

    cap.release()
    print(f"✅ Triple Riding complete. Total: {violation_count}")

if __name__ == "__main__":
    main()
