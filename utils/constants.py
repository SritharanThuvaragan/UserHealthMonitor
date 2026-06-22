# --- MediaPipe Pose Landmark Indices ---
NOSE_IDX = 0
LEFT_EYE_INNER_IDX = 1
LEFT_EYE_IDX = 2
LEFT_EYE_OUTER_IDX = 3
RIGHT_EYE_INNER_IDX = 4
RIGHT_EYE_IDX = 5
RIGHT_EYE_OUTER_IDX = 6
LEFT_EAR_IDX = 7
RIGHT_EAR_IDX = 8
LEFT_SHOULDER_IDX = 11
RIGHT_SHOULDER_IDX = 12
LEFT_ELBOW_IDX = 13
RIGHT_ELBOW_IDX = 14
LEFT_WRIST_IDX = 15
RIGHT_WRIST_IDX = 16
LEFT_HIP_IDX = 23
RIGHT_HIP_IDX = 24

# --- MediaPipe FaceMesh Eye Landmark Indices ---
# Eye landmarks are selected in pairs (p1-p4 horizontal, p2-p6 vertical, p3-p5 vertical)
# For calculations: (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
# Left Eye indices in FaceMesh
LEFT_EYE_LANDMARKS = [362, 385, 387, 263, 373, 380]  # [p1, p2, p3, p4, p5, p6]
# Right Eye indices in FaceMesh
RIGHT_EYE_LANDMARKS = [33, 160, 158, 133, 153, 144]   # [p1, p2, p3, p4, p5, p6]

# --- MediaPipe FaceMesh Distance Landmark Indices ---
# Landmarks 234 and 454 represent the leftmost and rightmost points of the face width
FACE_WIDTH_LEFT_IDX = 234
FACE_WIDTH_RIGHT_IDX = 454

# --- Distance Calculation Defaults ---
# Average human face width is approximately 14.0 cm
KNOWN_FACE_WIDTH_CM = 14.0
# Calibrated focal length for standard webcams (standard 640x480 resolution)
# focal_length = (pixel_width * distance_cm) / face_width_cm
# At 60cm distance, if pixel width is ~116: (116 * 60) / 14 = 497.14 -> 500 is a standard default.
DEFAULT_FOCAL_LENGTH = 500.0
