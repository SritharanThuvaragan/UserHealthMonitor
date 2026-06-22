import cv2
import time
from camera.webcam import WebcamCapture
from detection.face_mesh import MediaPipeProcessor
from utils.logger import logger
from utils.calculations import calculate_angle_with_vertical, calculate_distance_cm, calculate_euclidean_distance
from utils.constants import (
    FACE_WIDTH_LEFT_IDX, FACE_WIDTH_RIGHT_IDX, 
    LEFT_SHOULDER_IDX, RIGHT_SHOULDER_IDX, 
    LEFT_EAR_IDX, NOSE_IDX
)

def main():
    logger.info("Starting Camera and MediaPipe integration verification script...")
    
    # Initialize components
    webcam = WebcamCapture()
    processor = MediaPipeProcessor()
    
    if not webcam.start():
        logger.error("Could not start webcam. Exiting test.")
        return
        
    cv2.namedWindow("UserHealthMonitor Test Feed", cv2.WINDOW_AUTOSIZE)
    
    prev_time = time.time()
    frame_count = 0
    fps = 0.0
    
    logger.info("Press 'q' on the OpenCV window to stop the verification loop.")
    
    try:
        while True:
            success, frame = webcam.read()
            if not success or frame is None:
                continue
                
            frame_count += 1
            curr_time = time.time()
            
            # Calculate FPS every 1 second
            if curr_time - prev_time >= 1.0:
                fps = frame_count / (curr_time - prev_time)
                frame_count = 0
                prev_time = curr_time
                logger.info(f"Performance Check: Current FPS: {fps:.2f}")
                
            # Process frame using MediaPipe
            face_results, pose_results = processor.process_frame(frame)
            
            face_lms = processor.get_face_landmarks(face_results)
            pose_lms = processor.get_pose_landmarks(pose_results)
            
            h, w, _ = frame.shape
            
            # Draw Face landmarks and display estimated face distance
            if face_lms:
                # Draw a subset of face landmarks to visualize mesh tracking
                for i in range(0, len(face_lms), 15):
                    pt = face_lms[i]
                    cx, cy = int(pt[0] * w), int(pt[1] * h)
                    cv2.circle(frame, (cx, cy), 1, (0, 255, 255), -1)
                    
                # Get landmarks to calculate face width in pixels
                pt_left = face_lms[FACE_WIDTH_LEFT_IDX]
                pt_right = face_lms[FACE_WIDTH_RIGHT_IDX]
                
                # Convert normalized coordinates to screen pixel values
                pixel_width = calculate_euclidean_distance(
                    (pt_left[0] * w, pt_left[1] * h),
                    (pt_right[0] * w, pt_right[1] * h)
                )
                
                distance_cm = calculate_distance_cm(pixel_width)
                color = (0, 255, 0) if distance_cm >= 50.0 else (0, 0, 255)
                cv2.putText(frame, f"Distance: {distance_cm:.1f} cm", (20, 70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                            
            # Draw key Pose landmarks and display estimated neck angle
            if pose_lms:
                # Draw key points (shoulders, ear, nose)
                joints = [LEFT_SHOULDER_IDX, RIGHT_SHOULDER_IDX, LEFT_EAR_IDX, NOSE_IDX]
                for idx in joints:
                    pt = pose_lms[idx]
                    cx, cy = int(pt[0] * w), int(pt[1] * h)
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
                    
                # Neck Angle computation (left ear to left shoulder relative to vertical axis)
                left_ear = pose_lms[LEFT_EAR_IDX]
                left_shoulder = pose_lms[LEFT_SHOULDER_IDX]
                
                ear_pixels = (left_ear[0] * w, left_ear[1] * h)
                shoulder_pixels = (left_shoulder[0] * w, left_shoulder[1] * h)
                
                neck_angle = calculate_angle_with_vertical(ear_pixels, shoulder_pixels)
                cv2.putText(frame, f"Neck Angle: {neck_angle:.1f} deg", (20, 110), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                            
            # Overlay Frame Statistics
            cv2.putText(frame, f"FPS: {fps:.2f}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'q' to exit", (w - 180, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # Display results
            cv2.imshow("UserHealthMonitor Test Feed", frame)
            
            # Check for termination key
            if cv2.waitKey(5) & 0xFF == ord('q'):
                logger.info("User requested exit from live loop.")
                break
    except KeyboardInterrupt:
        logger.info("Verification loop terminated via keyboard interrupt.")
    finally:
        # Cleanup
        webcam.release()
        processor.close()
        cv2.destroyAllWindows()
        logger.info("Camera and MediaPipe modules released successfully.")

if __name__ == "__main__":
    main()
