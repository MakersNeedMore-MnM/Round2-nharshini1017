# 🚦 RoadSense AI

### Spatio-Temporal Traffic Violation Detection System Using Edge AI, YOLOv8 and ByteTrack

RoadSense AI is an **AI-powered traffic violation detection system** that analyzes CCTV/IP camera video to automatically identify and record common road-safety violations.

The system combines **YOLOv8 object detection, ByteTrack multi-object tracking, spatial association, temporal validation, MediaPipe-based analysis, and Flask/React technologies** to provide reliable traffic-event detection and digital evidence generation.

---

## 📖 Overview

Traditional CCTV-based traffic monitoring requires continuous human observation. RoadSense AI automates this process by analyzing video streams and identifying traffic violations across multiple frames.

The system maintains vehicle identities, analyzes relationships between riders and vehicles, validates observations over time, and generates evidence for detected violations.

### Detected Violations

* 🪖 Helmetless Riding
* 👥 Triple Riding / Excessive Rider Count
* 📱 Mobile Phone Usage While Riding
* ↩️ Wrong-Way Movement

---

## 🎯 Objectives

* Automatically detect traffic violations from CCTV/IP camera footage.
* Track vehicles across successive video frames.
* Use spatial relationships to associate riders and relevant objects.
* Apply temporal validation to reduce false detections.
* Automatically capture evidence of detected violations.
* Record violation details for later review.
* Provide a web-based dashboard for monitoring detected events.
* Support Edge-AI based traffic monitoring with low dependence on cloud processing.

---

## ✨ Key Features

### 🚨 Traffic Violation Detection

Detects multiple traffic violations from road surveillance video:

* Helmetless riding
* Triple riding
* Mobile-phone usage while riding
* Wrong-way movement

### 🎯 YOLOv8 Object Detection

YOLOv8 is used to detect relevant objects such as:

* Vehicles
* Riders
* Mobile phones
* Other objects required for violation analysis

### 👣 ByteTrack Vehicle Tracking

ByteTrack provides persistent tracking of detected vehicles across successive frames.

Tracking enables:

* Vehicle identity persistence
* Trajectory analysis
* Direction analysis
* Temporal event validation

### 🔗 Spatial Association

The system analyzes spatial relationships between detected objects using techniques such as:

* Bounding-box relationships
* Centroid distance
* Relative position
* Object association
* Predefined regions of interest

### ⏱️ Temporal Validation

Potential violations are validated across multiple frames rather than relying on a single frame.

The validation process can consider:

* Consecutive observations
* Persistence of an event
* Majority observations
* Spatial consistency

### 📸 Evidence Generation

When a violation is confirmed, RoadSense AI can capture and store relevant evidence.

Evidence records can include:

* Violation type
* Timestamp
* Track ID
* Vehicle information
* Location
* Evidence snapshot

### 📊 Web Dashboard

A React-based dashboard provides visualization of detected violations and their associated evidence.

---

# 🧠 System Architecture

```text
              CCTV / IP Camera
                     │
                     ▼
                RTSP Stream
                     │
                     ▼
             ┌───────────────┐
             │ Edge-AI Core  │
             └───────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ YOLOv8 Detection│
            └─────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ ByteTrack       │
            │ Vehicle Tracking│
            └─────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Spatial         │
            │ Association     │
            └─────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │ Temporal        │
            │ Validation      │
            └─────────────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Helmetless   Triple     Mobile
       Riding      Riding     Phone
          │          │          │
          └──────────┼──────────┘
                     │
                     ▼
              Wrong-Way Analysis
                     │
                     ▼
             Violation Event
                     │
                     ▼
             Evidence Capture
                     │
                     ▼
              Event Logging
                     │
                     ▼
             React Dashboard
```

---

# ⚙️ System Workflow

```text
1. CCTV / IP Camera
        ↓
2. RTSP Video Stream
        ↓
3. Frame Processing
        ↓
4. YOLOv8 Object Detection
        ↓
5. ByteTrack Vehicle Tracking
        ↓
6. Spatial Association
        ↓
7. Temporal Validation
        ↓
8. Violation Classification
        ↓
9. Evidence Capture
        ↓
10. Event Logging
        ↓
11. Dashboard Visualization
```

---

# 🚨 Violation Detection

## 🪖 Helmetless Riding

The system analyzes detected riders and their relationship with the corresponding vehicle to identify riders without helmets.

Detection is validated across video frames before generating an event.

---

## 👥 Triple Riding

The system associates multiple riders with a two-wheeler and determines whether the rider count exceeds the configured threshold.

```text
Vehicle
   ↓
Rider Detection
   ↓
Rider Association
   ↓
Rider Count
   ↓
Excessive Rider Event
```

---

## 📱 Mobile Phone Usage

Mobile-phone usage while riding is identified using object and spatial/pose relationships.

The system analyzes the relationship between the rider, hand/head region, and detected mobile phone across successive frames.

---

## ↩️ Wrong-Way Movement

Wrong-way movement is identified using persistent vehicle tracking and trajectory analysis.

```text
Vehicle Detection
       ↓
Persistent Track
       ↓
Vehicle Trajectory
       ↓
Movement Direction
       ↓
Compare With Configured Direction
       ↓
Wrong-Way Event
```

---

# 🛠️ Technology Stack

| Category                | Technology         |
| ----------------------- | ------------------ |
| Object Detection        | YOLOv8             |
| Multi-Object Tracking   | ByteTrack          |
| Pose / Spatial Analysis | MediaPipe          |
| Computer Vision         | OpenCV             |
| Backend                 | Flask              |
| Frontend                | React.js           |
| OCR / Plate Processing  | EasyOCR            |
| Video Input             | RTSP               |
| Programming             | Python, JavaScript |
| Deployment Approach     | Edge AI            |

---

# 📂 Project Structure

```text
Spatio-Temporal-Traffic-Violation-Detection/
│
├── assets/
│   └── demo video/
│       ├── output_mobile.mp4
│       └── output_video.mp4
│
├── backend/
│   ├── models/
│   ├── output/
│   ├── logs/
│   ├── backend.py
│   ├── main.py
│   ├── helmetless_violation.py
│   ├── mobile_usage.py
│   ├── triple_riding.py
│   ├── wrong_way.py
│   ├── snapshot_manager.py
│   └── violation_logger.py
│
├── docs/
│   └── traffic violation report.pdf
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── Dashboard.jsx
│   │   ├── index.js
│   │   └── main.css
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
├── LICENSE
└── README.md
```

---

# 📸 Evidence and Logging

Each detected violation can be recorded with associated metadata such as:

```text
Timestamp
Violation Type
Track ID
Number Plate
Location
Evidence Snapshot
```

This provides a structured record of detected traffic events for monitoring and review.

---

# 🌐 Edge-AI Approach

RoadSense AI is designed around an **Edge-first processing architecture**.

```text
CCTV / IP Camera
        ↓
     RTSP
        ↓
   Edge Device
        ↓
  AI Processing
        ↓
Violation Detection
        ↓
Local Evidence
        ↓
Dashboard
```

Processing video closer to the camera can reduce the need to continuously transmit raw video to a remote server and can support low-latency traffic monitoring.

---

# 📊 Dashboard

The web dashboard provides a centralized interface for viewing detected traffic violations.

It can display:

* Total violations
* Violation categories
* Detection timestamps
* Location
* Track information
* Evidence snapshots
* Violation records

---

# 🚀 Future Scope

* Automatic Number Plate Recognition enhancement
* Automated evidence management
* E-challan integration
* Red-light violation detection
* Overspeeding detection
* Multi-camera vehicle tracking
* Advanced traffic analytics
* Large-scale Edge deployment
* Integration with intelligent transportation systems

---

# 🌆 Applications

RoadSense AI can be used for:

* 🚦 Traffic Enforcement
* 🛣️ Road Safety Monitoring
* 🏙️ Smart City Traffic Monitoring
* 📹 Intelligent CCTV Surveillance
* 🚔 Automated Traffic Violation Detection
* 🚘 Intelligent Transportation Systems

---

# 👩‍💻 Authors

**Harshini N**
**Hrithi Shree S S**

Department of Electronics and Communication Engineering
**Saranathan College of Engineering, Trichy**

---

# 📄 License

This project is licensed under the **MIT License**.


