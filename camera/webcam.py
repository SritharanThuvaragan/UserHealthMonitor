import cv2
from utils.logger import logger
import config

class WebcamCapture:
    """
    Handles camera interaction using OpenCV, providing methods to open, read,
    and release the camera resources.
    """
    def __init__(self, camera_index=None):
        self.camera_index = camera_index if camera_index is not None else config.CAMERA_INDEX
        self.cap = None
        logger.info(f"WebcamCapture initialized with camera_index={self.camera_index}")

    def start(self):
        """
        Attempts to open the camera interface.
        Returns:
            bool: True if camera opened successfully, False otherwise.
        """
        if self.is_opened():
            logger.warning("Webcam already started.")
            return True

        logger.info(f"Opening camera index {self.camera_index}...")
        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            logger.error(f"Failed to open webcam at index {self.camera_index}.")
            self.cap = None
            return False

        # Set resolution from config
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        
        # Log actual resolution obtained
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        logger.info(f"Webcam started successfully. Resolution set to: {width}x{height}")
        return True

    def read(self):
        """
        Reads a single frame from the camera.
        Returns:
            tuple: (success (bool), frame (numpy.ndarray or None))
        """
        if not self.is_opened():
            logger.error("Attempted to read frame, but camera is not open.")
            return False, None

        success, frame = self.cap.read()
        if not success:
            logger.warning("Failed to capture frame from webcam.")
            return False, None

        return True, frame

    def release(self):
        """
        Releases the VideoCapture resource.
        """
        if self.cap is not None:
            logger.info("Releasing webcam VideoCapture resource...")
            self.cap.release()
            self.cap = None
            logger.info("Webcam resource released.")

    def is_opened(self):
        """
        Returns True if cap exists and is opened, otherwise False.
        """
        return self.cap is not None and self.cap.isOpened()

    def __del__(self):
        self.release()
