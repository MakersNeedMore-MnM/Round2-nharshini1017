import cv2
import sys
import os
import numpy as np
np.float = float

sys.path.append(os.path.join(os.path.dirname(__file__), 'yolox'))

from ultralytics import YOLO
from yolox.tracker.byte_tracker import BYTETracker
from yolox.tracking_utils.timer import Timer
from violation_logger import log_violation
from snapshot_manager import save_snapshot_once_per_id

def run_wrong_way_detection(input_video, output_video):

    class TrackerArgs:
        track_thresh = 0.5
        track_buffer = 30
        match_thresh = 0.8
        min_box_area = 10
        mot20 = False
        frame_rate = 30

    args = TrackerArgs()
    tracker = BYTETracker(args)
    model = YOLO("yolov8n.pt")
    timer = Timer()

    initial_positions = {}
    wrong_way_ids = set()
    trajectory = {}

    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print("❌ Could not open input video.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    os.makedirs("outputs", exist_ok=True)
    os.makedirs("violations/wrong_way", exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    def draw_entry_exit_lines(frame):
        h, w = frame.shape[:2]
        entry_x = int(w * 0.95)
        exit_x = int(w * 0.05)
        cv2.line(frame, (entry_x, 0), (entry_x, h), (0, 255, 0), 2)
        cv2.putText(frame, "ENTRY", (entry_x + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.line(frame, (exit_x, 0), (exit_x, h), (0, 0, 255), 2)
        cv2.putText(frame, "EXIT", (exit_x - 70, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        return entry_x, exit_x

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        draw_entry_exit_lines(frame)

        results = model(frame, verbose=False)[0]
        detections = []
        for result in results.boxes.data.cpu().numpy():
            x1, y1, x2, y2, score, class_id = result
            if int(class_id) in [2, 3, 5, 7]:
                detections.append([x1, y1, x2, y2, score])

        detections_np = np.array(detections) if detections else np.empty((0, 5))

        timer.tic()
        online_targets = tracker.update(detections_np, frame.shape[:2], frame.shape[:2])
        timer.toc()

        for t in online_targets:
            tlwh = t.tlwh
            x1, y1 = int(tlwh[0]), int(tlwh[1])
            x2, y2 = int(tlwh[0] + tlwh[2]), int(tlwh[1] + tlwh[3])
            track_id = int(t.track_id)

            cx = int((x1 + x2) / 2)

            if track_id not in initial_positions:
                initial_positions[track_id] = cx

            dx = cx - initial_positions[track_id]
            is_wrong = dx > 30

            if is_wrong:
                wrong_way_ids.add(track_id)

            if track_id in wrong_way_ids:
                color = (0, 255, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, "WRONG WAY 🚫", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                snap_path = save_snapshot_once_per_id(
                    frame=frame,
                    folder="violations/wrong_way",
                    prefix="wrongway",
                    track_id=track_id,
                    violation_key="wrong_way"
                )

                if snap_path:
                    log_violation("wrong_way", snap_path, track_id=track_id, plate="UNKNOWN")

        out.write(frame)

    cap.release()
    out.release()
    print(f"✅ Wrong-way output saved: {output_video}")

if __name__ == "__main__":
    run_wrong_way_detection("INPUT_VIDEO.mp4", "outputs/wrong_way_output.mp4")
