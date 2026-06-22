import cv2
import mediapipe as mp
from utils.logger import logger

class MediaPipeProcessor:
    """
    Initializes and manages the lifetime of MediaPipe FaceMesh and Pose detection solutions.
    Provides methods to extract normalized landmark coordinates from video frames.
    """
    def __init__(self, refine_face_landmarks=True, pose_complexity=1):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_pose = mp.solutions.pose
        
        logger.info("Initializing MediaPipe FaceMesh (max_faces=1) and Pose models...")
        try:
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                static_image_mode=False,
                max_num_faces=1,
                refine_landmarks=refine_face_landmarks,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.pose = self.mp_pose.Pose(
                static_image_mode=False,
                model_complexity=pose_complexity,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            logger.info("MediaPipe FaceMesh and Pose objects initialized successfully.")
        except Exception as e:
            logger.critical(f"Failed to initialize MediaPipe components: {e}")
            raise e

    def process_frame(self, frame):
        """
        Processes a BGR image frame and returns raw MediaPipe results for face and pose.
        """
        if frame is None:
            return None, None
        
        # Convert BGR (OpenCV standard) to RGB (MediaPipe standard)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        face_results = self.face_mesh.process(rgb_frame)
        pose_results = self.pose.process(rgb_frame)
        
        return face_results, pose_results

    def get_face_landmarks(self, face_results):
        """
        Extracts face landmarks coordinates as a list of (x, y, z) tuples.
        Returns:
            list: List of 468 (or 478 refined) normalized (x, y, z) coordinates,
                  or None if no face is detected.
        """
        if face_results and face_results.multi_face_landmarks:
            landmarks = face_results.multi_face_landmarks[0]
            return [(lm.x, lm.y, lm.z) for lm in landmarks.landmark]
        return None

    def get_pose_landmarks(self, pose_results):
        """
        Extracts pose landmarks coordinates as a list of (x, y, z) tuples.
        Returns:
            list: List of 33 normalized (x, y, z) coordinates,
                  or None if no pose is detected.
        """
        if pose_results and pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks
            return [(lm.x, lm.y, lm.z) for lm in landmarks.landmark]
        return None

    def close(self):
        """
        Explicitly releases MediaPipe resources.
        """
        try:
            if hasattr(self, 'face_mesh') and self.face_mesh is not None:
                self.face_mesh.close()
            if hasattr(self, 'pose') and self.pose is not None:
                self.pose.close()
            logger.info("MediaPipe processors closed.")
        except Exception as e:
            logger.warning(f"Error while closing MediaPipe processors: {e}")

    def __del__(self):
        self.close()
