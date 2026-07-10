import os
import time
from datetime import datetime
import cv2

_last_saved_time = {}
_saved_track_ids = {}

def save_snapshot_with_cooldown(frame, folder, prefix,
                               cooldown_seconds=5,
                               violation_key="default",
                               ext=".jpg"):
    os.makedirs(folder, exist_ok=True)
    now = time.time()

    if violation_key not in _last_saved_time:
        _last_saved_time[violation_key] = 0

    if (now - _last_saved_time[violation_key]) < cooldown_seconds:
        return None

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{ts}{ext}"
    snap_path = os.path.join(folder, filename)

    cv2.imwrite(snap_path, frame)
    _last_saved_time[violation_key] = now
    return snap_path


def save_snapshot_once_per_id(frame, folder, prefix,
                             track_id,
                             violation_key="default",
                             ext=".jpg"):
    os.makedirs(folder, exist_ok=True)

    if violation_key not in _saved_track_ids:
        _saved_track_ids[violation_key] = set()

    if track_id in _saved_track_ids[violation_key]:
        return None

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_ID{track_id}_{ts}{ext}"
    snap_path = os.path.join(folder, filename)

    cv2.imwrite(snap_path, frame)
    _saved_track_ids[violation_key].add(track_id)
    return snap_path
