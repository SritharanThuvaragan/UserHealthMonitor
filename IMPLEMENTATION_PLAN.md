# UserHealthMonitor Complete Implementation Plan

**Student:** Sritharan Thuvaragan | **Student No:** 2526995
**Degree:** BSc (Hons) Software Engineering
**Supervisor:** Mr. V.A.M.R. Sinthujan
**Project:** ML-Based User Behaviour Monitoring & Lifestyle Recommendation System
**Plan Version:** Final — June 2026

---

## Project Overview & Confirmed Architecture

**System Architecture Flow (Confirmed)**
```
Camera Input → MediaPipe (Landmarks) → Detection Modules →
Model 1: Posture Classifier → Feature Combiner → Model 2: Behaviour Classifier → Recommendation Engine → Dashboard
```

**Two‑Model Decision — Final Confirmation**
- **Model 1 — Posture Classifier**
- **Model 2 — Behaviour Classifier**

**Purpose**
- Detect good vs. bad posture in real time
- Combine all signals → healthy / unhealthy decision

**Inputs**
- Neck angle, shoulder alignment, spine angle (MediaPipe landmark coords)
- Posture result, face distance, blink rate, lighting score, screen time, break count

**Outputs**
- `good_posture / bad_posture`
- `healthy / unhealthy` → triggers recommendations

---

## Dataset Summary (9 Datasets – Sufficient for All Modules)

| Module | Datasets (source) | Why sufficient |
|--------|-------------------|----------------|
| **Posture Detection** | 1. MultiPosture (Zenodo – CSV) 2. Sitting‑Posture‑Detect (Kaggle – images) 3. Posture‑Correction v4 (Roboflow – 4 666 images) | CSV provides pre‑extracted MediaPipe joint coordinates for lightweight classifiers; images allow training CNN/YOLO models. |
| **Drowsiness & Eye Tracking** | 4. Kaggle *drowsiness‑dataset* (eye & mouth states) 5. Kaggle *driver‑drowsiness‑dataset‑ddd* (41 k facial images) | Provides labeled eye‑state and full‑face fatigue data for both classic EAR‑based and deep‑learning models. |
| **Low‑Light Robustness** | 6. Kaggle *lol‑dataset* (low‑light / normal‑light pairs) 7. GitHub *ExDark* (dark‑environment benchmark) | Enables illumination‑enhancement pipelines & validates detection under extreme lighting. |
| **User Behaviour Analytics** | 8. Kaggle *gym‑members‑exercise‑tracking* 9. Kaggle *posture‑reconstruction* | Tabular & time‑series data for long‑term health‑behavior modeling and recommendation generation. |

---

## Phase‑by‑Phase Implementation Plan

### Phase 1 – Environment Setup & Project Foundation (Weeks 1‑2)
1. Create Python virtual environment (`.venv`). Install dependencies from `requirements.txt`.
2. Create project folder hierarchy (`camera/`, `detection/`, `tracking/`, `features/`, `dataset/`, `ml/`, `recommendation/`).
3. Write `config.py` (camera index, thresholds, constants).
4. Initialise Git repo, add `.gitignore` (exclude `__pycache__`, `*.pkl`, `dataset/raw/`).
5. Implement utility modules (`logger.py`, `constants.py`, `calculations.py`).

### Phase 2 – Camera & MediaPipe Integration (Weeks 3‑4)
- Implement `webcam.py` (open, read, release).
- Implement `face_mesh.py` (MediaPipe FaceMesh & Pose).
- Build a basic live‑feed loop (`main.py`) displaying landmarks.
- Verify FPS > 20; if not, downgrade MediaPipe model complexity.

### Phase 3 – Rule‑Based Detection Modules (Weeks 5‑7)
- `posture_detector.py`: compute neck angle, shoulder alignment, spine angle.
- `eye_strain_detector.py`: compute EAR; flag `< 0.25` for sustained periods.
- `face_distance_detector.py`: estimate distance using known face width.
- `lighting_detector.py`: average frame brightness; `< 80` lux → poor lighting.
- Integration test: run all four modules concurrently, print metrics each second.

### Phase 4 – Dataset Collection & Model 1 Training (Weeks 8‑11)
1. **Download datasets** (MultiPosture CSV, Kaggle image sets, Roboflow manual ZIP, ExDark clone).
2. `data_collector.py`: record 10‑s webcam sessions, extract posture features, label (good/bad).
3. `label_tool.py`: simple GUI/CLI for manual labelling.
4. `analysis.ipynb`: explore class balance, feature distributions.
5. `preprocessing.py`: clean CSV, apply `StandardScaler`, split 80/20.
6. `train.py` (Model 1): `RandomForestClassifier(n_estimators=100)` → save `ml/models/random_forest.pkl`.
7. `evaluate.py` (Model 1): compute accuracy, precision, recall, F1, confusion matrix, ROC‑AUC.

### Phase 5 – Behaviour Dataset & Model 2 Training (Weeks 12‑14)
1. Run full detection pipeline for 20+ sessions (mix healthy/unhealthy).
2. Log six aggregated features per session window: posture_score, face_distance_cm, blink_rate_per_min, lighting_score, screen_time_min, break_count.
3. Save to `behaviour_dataset.csv` (500‑2000 records).
4. Balance dataset (SMOTE if needed).
5. `train.py` (Model 2): RandomForest on 6 features → `ml/models/behaviour_model.pkl` (also experiment with SVM).
6. `evaluate.py` (Model 2): same metrics, plus feature‑importance plot.

### Phase 6 – Tracking, Recommendations & Database (Weeks 15‑17)
- `session_tracker.py`: total session duration (`datetime`).
- `break_tracker.py`: detect breaks (no face > 2 min) and count per hour.
- `health_score_tracker.py`: compute daily score (weights: posture 35 % + eye 20 % + distance 20 % + lighting 10 % + break 15 %).
- `recommendation_rules.json`: rule‑based messages (e.g., bad posture → "Sit up straight").
- `recommendation_engine.py`: load rules, combine with model outputs, prioritize top‑3 recommendations.
- `database.py` + `models.py`: SQLite tables (`sessions`, `behaviours`).

### Phase 7 – Dashboard & Alert System (Weeks 18‑20)
- `notification.py`: Tkinter messagebox / custom Toplevel for alerts.
- `sound_alert.py`: pygame beep for high‑priority alerts.
- `app_window.py`: main Tkinter GUI with tabs (Live View, Statistics, History).
- `camera_view.py`: live webcam feed overlaying coloured status indicators (green = good, red = bad).
- `health_panel.py`: live display of posture, distance, lighting, eye strain, session time, health score.
- `statistics_view.py`: Matplotlib charts (daily health score, posture‑time pie chart).
- Reusable UI components (`cards.py`, `buttons.py`, `alerts.py`).

### Phase 8 – Testing & Evaluation (Weeks 21‑24)
- Unit tests (`test_camera.py`, `test_detection.py`).
- Integration test: end‑to‑end pipeline → DB → dashboard.
- Performance test: ensure > 20 FPS, log CPU/memory.
- User testing: 5 participants, 2 sessions each, questionnaire.
- Final accuracy evaluation on held‑out test sets (report precision, recall, F1 for both models).

### Phase 9 – Dissertation Writing & Submission (Weeks 25‑31)
1. **Introduction** – background, problem statement, aims, scope.
2. **Literature Review** – 5 key papers, theoretical frameworks (HBM, TAM).
3. **Methodology** – design‑science approach, data collection, ethical considerations.
4. **Implementation** – architecture, module explanations, code snippets, dataset preparation, model training.
5. **Evaluation** – quantitative results, user‑testing feedback, performance benchmarks, comparison with existing solutions.
6. **Conclusion** – achievements, limitations, future work (affective computing, edge AI).
7. **Final Submission** – proofread, push code to GitHub, create README, package PDF, submit to university portal.

---

## Timeline Summary (31 Weeks)
| Phase | Weeks | Key Deliverable |
|------|-------|-----------------|
| 1 – Environment Setup | 1‑2 | Project structure, config, utils |
| 2 – Camera & MediaPipe | 3‑4 | Live landmark feed |
| 3 – Detection Modules | 5‑7 | Posture, EAR, distance, lighting working |
| 4 – Datasets & Model 1 | 8‑11 | Posture classifier > 85 % accuracy |
| 5 – Behaviour & Model 2 | 12‑14 | Behaviour classifier > 80 % accuracy |
| 6 – Tracking, Recs, DB | 15‑17 | Health score, recommendations, SQLite |
| 7 – Dashboard & Alerts | 18‑20 | Full GUI with live view & charts |
| 8 – Testing & Evaluation | 21‑24 | Unit/integration tests, user study, final metrics |
| 9 – Dissertation | 25‑31 | Complete dissertation, final repo submission |

---

## File Structure (final)
```
UserHealthMonitor/
│   README.md
│   requirements.txt
│   setup_datasets.ps1
│   .venv/                # virtual env
├── camera/
├── detection/
│   ├── webcam.py
│   ├── face_mesh.py
│   ├── posture_detector.py
│   ├── eye_strain_detector.py
│   ├── face_distance_detector.py
│   └── lighting_detector.py
├── tracking/
│   ├── session_tracker.py
│   └── break_tracker.py
├── features/
├── dataset/
│   ├── raw/   # downloaded datasets
│   └── processed/
│       ├── dataset.csv
│       └── behaviour.csv
├── ml/
│   ├── training/
│   │   ├── preprocessing.py
│   │   ├── train.py
│   │   └── evaluate.py
│   └── models/
│       ├── random_forest.pkl          # Model 1
│       ├── behaviour_model.pkl        # Model 2
│       └── scaler.pkl
├── recommendation/
│   ├── recommendation_rules.json
│   └── recommendation_engine.py
├── database/
│   └── models.py
├── docs/
│   └── implementation_notes.md
└── app/
    ├── app_window.py
    ├── camera_view.py
    ├── health_panel.py
    ├── statistics_view.py
    ├── notification.py
    ├── sound_alert.py
    └── utils/   # reusable UI components
```

---

### Final Deliverables Checklist
- [x] Functional desktop application (Tkinter GUI) with live feed and health metrics.
- [x] Posture detection (MediaPipe + angle calculations).
- [x] Eye‑strain detection (EAR).
- [x] Face‑to‑screen distance estimator.
- [x] Lighting condition detector.
- [x] Screen‑time monitoring.
- [x] Model 1 – Posture classifier (Random Forest > 85 % acc).
- [x] Model 2 – Behaviour classifier (Random Forest > 80 % acc).
- [x] Rule‑based recommendation engine.
- [x] Daily health‑score dashboard.
- [x] SQLite database for sessions & historic data.
- [x] Unit & integration tests (pytest).
- [x] User testing with 5 participants + questionnaire.
- [x] Evaluation results (accuracy, F1, confusion matrix).
- [x] GitHub repository with comprehensive README.
- [x] Final dissertation (PDF) submitted to university.

---

*Prepared by:* **Sritharan Thuvaragan** (Student No. 2526995) – *BSc (Hons) Software Engineering*.
*Supervisor:* **Mr. V.A.M.R. Sinthujan**.
*Date:* June 2026.
