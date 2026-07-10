import os
import subprocess
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ===============================
# PATH SETUP
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGS_DIR = os.path.join(BASE_DIR, "logs")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

HELMET_SNAPS = os.path.join(BASE_DIR, "helmetless__snaps")
MOBILE_SNAPS = os.path.join(BASE_DIR, "mobile_use_snaps")
TRIPLE_SNAPS = os.path.join(BASE_DIR, "snapshots", "triple_riding")
WRONGWAY_SNAPS = os.path.join(BASE_DIR, "violations", "wrong_way")

CSV_PATH = os.path.join(LOGS_DIR, "violations.csv")
INPUT_VIDEO_PATH = os.path.join(BASE_DIR, "INPUT_VIDEO.mp4")

# Create folders if not exist
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# ===============================
# HOME ROUTE
# ===============================

@app.route("/")
def home():
    return "✅ Backend running fine!"

# ===============================
# UPLOAD VIDEO
# ===============================

@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file found"}), 400

    file = request.files["file"]
    file.save(INPUT_VIDEO_PATH)

    return jsonify({"message": "Video uploaded successfully"})

# ===============================
# RUN DETECTION
# ===============================

@app.route("/run", methods=["POST"])
def run_detection():
    try:
        subprocess.run(["python", "main.py"], cwd=BASE_DIR, check=True)
        return jsonify({"message": "Detection completed successfully"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

# ===============================
# GET VIOLATIONS (FIXED NaN ISSUE)
# ===============================

@app.route("/api/violations", methods=["GET"])
def get_violations():

    if not os.path.exists(CSV_PATH):
        return jsonify([])

    df = pd.read_csv(CSV_PATH)

    # 🔥 VERY IMPORTANT FIX
    # Replace NaN with empty string (valid JSON)
    df = df.fillna("")

    records = df.to_dict(orient="records")

    return jsonify(records)

# ===============================
# DOWNLOAD CSV
# ===============================

@app.route("/download/csv", methods=["GET"])
def download_csv():

    if not os.path.exists(CSV_PATH):
        return jsonify({"error": "CSV not found"}), 404

    return send_file(CSV_PATH, as_attachment=True)

# ===============================
# SERVE OUTPUT VIDEOS
# ===============================

@app.route("/videos/<path:filename>")
def serve_videos(filename):
    return send_from_directory(OUTPUTS_DIR, filename)

# ===============================
# SERVE SNAPSHOTS
# ===============================

@app.route("/snapshots/<path:filename>")
def serve_snapshots(filename):

    # Fix Windows backslash issue
    filename = filename.replace("\\", "/")

    folders = [HELMET_SNAPS, MOBILE_SNAPS, TRIPLE_SNAPS, WRONGWAY_SNAPS]

    for folder in folders:
        file_path = os.path.join(folder, filename)
        if os.path.exists(file_path):
            return send_from_directory(folder, filename)

    return jsonify({"error": "Snapshot not found"}), 404


# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":
    print("🚀 Flask Backend Running on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)