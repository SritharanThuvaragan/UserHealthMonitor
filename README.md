# UserHealthMonitor

**ML-Based User Behaviour Monitoring & Lifestyle Recommendation System**

> BSc (Hons) Software Engineering — Sritharan Thuvaragan (2526995)
> Supervisor: Mr. V.A.M.R. Sinthujan

---

## Overview

A desktop application that uses webcam input and MediaPipe to monitor user health in real time — detecting posture, eye strain, face-to-screen distance, and lighting conditions. Two ML models classify posture and overall behaviour, feeding into a recommendation engine displayed on a Tkinter dashboard.

**Architecture:**
```
Camera → MediaPipe (Landmarks) → Detection Modules →
  Model 1: Posture Classifier → Feature Combiner →
  Model 2: Behaviour Classifier → Recommendation Engine → Dashboard
```

---

## Progress Tracker

### ✅ Phase 1 — Environment Setup & Project Foundation
- [x] Python virtual environment (`.venv`)
- [x] Project folder hierarchy created
- [x] `config.py` — camera index, thresholds, constants
- [x] Git repo initialised with `.gitignore`
- [x] `utils/logger.py` — logging utility
- [x] `utils/constants.py` — project-wide constants
- [x] `utils/calculations.py` — angle & distance math helpers
- [x] `utils/helpers.py` — general helper functions
- [x] `requirements.txt`

### ✅ Phase 2 — Camera & MediaPipe Integration
- [x] `camera/webcam.py` — open, read, release webcam feed
- [x] `detection/face_mesh.py` — MediaPipe FaceMesh & Pose initialisation
- [x] `main.py` — live-feed loop displaying landmarks

### 🔶 Phase 3 — Rule-Based Detection Modules *(In Progress)*
- [ ] `detection/posture_detector.py` — neck angle, shoulder alignment, spine angle
- [ ] `detection/eye_strain_detector.py` — EAR (Eye Aspect Ratio) computation
- [ ] `detection/face_distance_detector.py` — distance estimation using face width
- [ ] `detection/lighting_detector.py` — frame brightness analysis

### 🔶 Phase 4 — Dataset Collection & Model 1 Training *(In Progress)*
- [x] Datasets downloaded (9 datasets across posture, drowsiness, lighting, behaviour)
- [x] `setup_datasets.ps1` — automated dataset download script
- [x] `check_datasets.py` — dataset verification utility
- [x] `data_collector.py` — record webcam sessions & extract features
- [x] `ml/training/preprocessing.py` — full preprocessing pipeline (clean, scale, split)
- [x] `ml/training/preprocess_all.py` — wrapper to run full pipeline
- [x] `ml/training/train.py` — RandomForest training script
- [ ] `dataset/label_tool.py` — manual labelling GUI/CLI
- [ ] `dataset/analysis.ipynb` — data exploration & class balance analysis
- [ ] `ml/training/evaluate.py` — accuracy, precision, recall, F1, confusion matrix, ROC-AUC

### ⬜ Phase 5 — Behaviour Dataset & Model 2 Training
- [ ] Collect 20+ detection sessions (healthy/unhealthy mix)
- [ ] Log 6 aggregated features per session window
- [ ] Build `behaviour_dataset.csv` (500–2000 records)
- [ ] Balance dataset (SMOTE if needed)
- [ ] Train Model 2 (RandomForest / SVM on 6 features)
- [ ] Evaluate Model 2 (metrics + feature-importance plot)

### ⬜ Phase 6 — Tracking, Recommendations & Database
- [ ] `tracking/session_tracker.py` — total session duration
- [ ] `tracking/break_tracker.py` — detect breaks (no face > 2 min)
- [ ] `tracking/health_score_tracker.py` — daily weighted health score
- [ ] `recommendations/recommendation_engine.py` — rule-based + model-driven recommendations
- [ ] `database/models.py` — SQLite table definitions
- [ ] `database/database.py` — DB connection & CRUD operations

### ⬜ Phase 7 — Dashboard & Alert System
- [ ] `dashboard/app_window.py` — main Tkinter GUI (tabs: Live View, Statistics, History)
- [ ] `dashboard/camera_view.py` — live webcam feed with coloured status overlays
- [ ] `dashboard/health_panel.py` — live posture, distance, lighting, eye strain, health score
- [ ] `dashboard/statistics_view.py` — Matplotlib charts (daily score, posture pie chart)
- [ ] `dashboard/components/` — reusable UI components (cards, buttons, alerts)
- [ ] `alerts/notification.py` — Tkinter alert popups
- [ ] `alerts/sound_alert.py` — pygame audio alerts

### ⬜ Phase 8 — Testing & Evaluation
- [ ] `tests/test_camera.py` — camera module unit tests
- [ ] `tests/test_detection.py` — detection module unit tests
- [ ] `tests/test_database.py` — database unit tests
- [ ] `tests/test_ml.py` — ML pipeline unit tests
- [ ] Integration test: end-to-end pipeline → DB → dashboard
- [ ] Performance test: ensure > 20 FPS, log CPU/memory
- [ ] User testing: 5 participants, 2 sessions each + questionnaire

### ⬜ Phase 9 — Dissertation & Submission
- [ ] Introduction, Literature Review, Methodology chapters
- [ ] Implementation & Evaluation chapters
- [ ] Final proofreading & submission

---

## Upcoming Steps (What to Do Next)

### 🔜 Immediate — Complete Detection Modules (Phase 3)
1. **Implement `posture_detector.py`** — compute neck angle, shoulder alignment, and spine angle from MediaPipe Pose landmarks.
2. **Implement `eye_strain_detector.py`** — compute Eye Aspect Ratio (EAR); flag prolonged values < 0.25 as strain.
3. **Implement `face_distance_detector.py`** — estimate face-to-screen distance using known inter-pupil width.
4. **Implement `lighting_detector.py`** — compute average frame brightness; flag < 80 lux as poor lighting.
5. **Integration test** — run all four detectors concurrently in `main.py`, print live metrics.

### 🔜 Next — Model Training & Evaluation (Phase 4 remaining)
1. Build `label_tool.py` for manual data labelling.
2. Create `analysis.ipynb` to explore class distributions and feature correlations.
3. Implement `evaluate.py` with full classification metrics and visualisations.
4. Train and validate Model 1 (target: > 85% accuracy).

---

## Directory Structure
```
UserHealthMonitor/
├── alerts/                  # Alert notifications & sounds
├── assets/sounds/           # Audio files for alerts
├── camera/                  # Webcam capture module
├── dashboard/               # Tkinter GUI (app, views, components)
├── data_collector.py        # Record webcam sessions & extract features
├── database/                # SQLite models & operations
├── dataset/                 # Raw & processed data (git-ignored)
├── detection/               # MediaPipe-based detection modules
├── docs/                    # Documentation & architecture diagrams
├── features/                # Feature extraction & normalisation
├── ml/                      # ML training, evaluation & prediction
├── recommendations/         # Recommendation engine
├── tests/                   # Unit & integration tests
├── tracking/                # Session, break & health score tracking
├── utils/                   # Shared utilities (logger, constants, math)
├── config.py                # Global configuration
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── setup_datasets.ps1       # Dataset download automation
```

## Setup

```bash
# Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Download datasets
.\setup_datasets.ps1

# Run preprocessing
python ml/training/preprocess_all.py

# Train a model
python ml/training/train.py posture   # or behaviour
```

## Version Control

This repository is tracked with Git. The `dataset/` folder is excluded via `.gitignore` to avoid pushing large data files.
