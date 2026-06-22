import math
from utils.constants import KNOWN_FACE_WIDTH_CM, DEFAULT_FOCAL_LENGTH

def calculate_euclidean_distance(p1, p2):
    """
    Calculates the Euclidean distance between two points (supports 2D or 3D coordinate list/tuple).
    """
    return math.sqrt(sum((x1 - x2) ** 2 for x1, x2 in zip(p1, p2)))

def calculate_angle_3point(a, b, c):
    """
    Calculates the angle abc in degrees, with b as the vertex.
    a, b, c can be 2D or 3D coordinates.
    """
    # Create vectors BA and BC
    ba = [a[i] - b[i] for i in range(len(b))]
    bc = [c[i] - b[i] for i in range(len(b))]
    
    # Dot product and magnitudes
    dot_product = sum(x * y for x, y in zip(ba, bc))
    mag_ba = math.sqrt(sum(x ** 2 for x in ba))
    mag_bc = math.sqrt(sum(x ** 2 for x in bc))
    
    if mag_ba == 0 or mag_bc == 0:
        return 0.0
        
    cos_angle = dot_product / (mag_ba * mag_bc)
    # Clamp value to prevent numerical precision errors outside [-1.0, 1.0]
    cos_angle = max(-1.0, min(1.0, cos_angle))
    
    return math.degrees(math.acos(cos_angle))

def calculate_angle_with_vertical(point, vertex):
    """
    Calculates the tilt angle in degrees of the line (point -> vertex) relative to a vertical axis.
    This is used to compute neck angle (e.g., ear position relative to shoulder vertical axis).
    """
    dx = point[0] - vertex[0]
    dy = point[1] - vertex[1]  # In OpenCV/MediaPipe screen space, y increases downwards.
    
    if dy == 0:
        return 90.0
        
    # Relative angle in radians relative to vertical (dy)
    angle_rad = math.atan2(abs(dx), abs(dy))
    return math.degrees(angle_rad)

def calculate_ear(eye_points):
    """
    Calculates the Eye Aspect Ratio (EAR) given 6 eye landmarks.
    eye_points is a list of 6 coordinates in order: [p1, p2, p3, p4, p5, p6]
    Formula: EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
    """
    if len(eye_points) < 6:
        return 0.0
        
    p1, p2, p3, p4, p5, p6 = eye_points[:6]
    
    # Vertical distances
    dist_2_6 = calculate_euclidean_distance(p2, p6)
    dist_3_5 = calculate_euclidean_distance(p3, p5)
    
    # Horizontal distance
    dist_1_4 = calculate_euclidean_distance(p1, p4)
    
    if dist_1_4 == 0:
        return 0.0
        
    return (dist_2_6 + dist_3_5) / (2.0 * dist_1_4)

def calculate_distance_cm(pixel_width, focal_length=DEFAULT_FOCAL_LENGTH, known_width=KNOWN_FACE_WIDTH_CM):
    """
    Estimates distance from screen in centimeters using pinhole camera geometry.
    Formula: distance = (known_width * focal_length) / pixel_width
    """
    if pixel_width == 0:
        return 0.0
    return (known_width * focal_length) / pixel_width
