import csv
import os
from datetime import datetime

LOG_FILE = "logs/violations.csv"
os.makedirs("logs", exist_ok=True)

def log_violation(violation_type, snapshot_path, track_id=None, plate="UNKNOWN", location="Saranathan Junction, Trichy"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Time", "Violation", "Snapshot", "Track_ID", "Plate", "Location"])
        writer.writerow([now, violation_type, snapshot_path, track_id, plate, location])
