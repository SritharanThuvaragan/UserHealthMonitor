import os

# --- Camera Settings ---
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
TARGET_FPS = 20

# --- Detection Thresholds ---
# Eye Aspect Ratio (EAR) threshold for blink/eye strain detection
EAR_THRESHOLD = 0.23
# Number of consecutive frames of low EAR to trigger eye strain warning (at ~20fps, 60 frames is 3 seconds)
EAR_CONSECUTIVE_FRAMES = 60
# Screen distance warning threshold in cm
DISTANCE_WARNING_CM = 50.0
# Minimum average lighting brightness (0-255 scale)
LIGHTING_MIN = 80.0
# Neck angle threshold in degrees for bad posture (tilt relative to vertical)
POSTURE_ANGLE_THRESHOLD = 20.0

# --- Tracking Settings ---
# Continuous screen time allowed before suggesting a break (in minutes)
BREAK_INTERVAL_MIN = 45
# Time required away from screen to count as a break (in minutes)
MIN_BREAK_DURATION_MIN = 2

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, "database", "health_monitor.db")
LOG_FILE = os.path.join(BASE_DIR, "logs", "application.log")
RULES_FILE = os.path.join(BASE_DIR, "recommendations", "recommendation_rules.json")
SOUND_FILE = os.path.join(BASE_DIR, "assets", "sounds", "alert.wav")

# --- UI & Sound Config ---
SOUND_ALERT_ENABLED = True
ALERT_VOLUME = 0.5  # Scale 0.0 to 1.0
UI_REFRESH_RATE_MS = 50  # Refresh camera and dials at 50ms intervals
STATS_UPDATE_INTERVAL_MS = 5000  # Extract features & evaluate models every 5 seconds
