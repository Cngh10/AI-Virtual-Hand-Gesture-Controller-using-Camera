#!/usr/bin/env python3
"""
Working Hand Gesture Controller
A simplified but functional hand gesture recognition system
"""

import cv2
import numpy as np
import pyautogui
import time
import math
from collections import deque

class WorkingHandGestureController:
    def __init__(self):
        # Initialize camera with better error handling
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("❌ Error: Could not open camera")
            return
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        # Screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Gesture tracking
        self.last_gesture = None
        self.gesture_cooldown = 0
        self.cooldown_time = 1.0  # seconds
        
        # Mouse control
        self.mouse_sensitivity = 2.0
        self.last_mouse_pos = None
        
        # Gesture definitions
        self.gestures = {
            'open_palm': 'Idle',
            'fist': 'Stop',
            'thumbs_up': 'Confirm',
            'two_fingers': 'Play',
            'three_fingers': 'Volume Up',
            'four_fingers': 'Volume Down',
            'pinch': 'Drag',
            'point': 'Move Mouse'
        }
        
        # Action mappings
        self.action_mappings = {
            'open_palm': self.idle_action,
            'fist': self.stop_action,
            'thumbs_up': self.confirm_action,
            'two_fingers': self.play_action,
            'three_fingers': self.volume_up_action,
            'four_fingers': self.volume_down_action,
            'pinch': self.drag_action,
            'point': self.move_mouse_action
        }
        
        # Improved hand detection parameters
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        
        print("✅ Hand Gesture Controller initialized successfully!")
    
    def detect_hand_simple(self, frame):
        """Simple hand detection using color-based segmentation"""
        try:
            # Convert to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create mask for skin color
            mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)
            
            # Apply morphological operations
            kernel = np.ones((3, 3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find the largest contour (likely the hand)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Filter by minimum area
                if cv2.contourArea(largest_contour) < 1000:
                    return None, 0, None
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Calculate hand center
                hand_center = (x + w//2, y + h//2)
                
                # Calculate hand area for gesture estimation
                area = cv2.contourArea(largest_contour)
                
                # Draw rectangle around hand
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, hand_center, 5, (0, 0, 255), -1)
                
                return hand_center, area, largest_contour
            else:
                return None, 0, None
        except Exception as e:
            print(f"Error in hand detection: {e}")
            return None, 0, None
    
    def estimate_gesture_simple(self, hand_center, area, contour):
        """Simple gesture estimation based on hand area and position"""
        if hand_center is None:
            return None
        
        # Normalize area (this is a very rough estimation)
        normalized_area = area / 10000  # Adjust this threshold based on testing
        
        # Simple gesture classification based on area
        if normalized_area > 2.0:
            return 'open_palm'
        elif normalized_area > 1.5:
            return 'two_fingers'
        elif normalized_area > 1.0:
            return 'three_fingers'
        elif normalized_area > 0.5:
            return 'point'
        else:
            return 'fist'
    
    def idle_action(self):
        """Idle action - no specific action"""
        pass
    
    def stop_action(self):
        """Stop action - pause media or stop current action"""
        pyautogui.press('space')
        print("Action: Stop")
    
    def confirm_action(self):
        """Confirm action - click or enter"""
        pyautogui.click()
        print("Action: Confirm")
    
    def play_action(self):
        """Play action - start media or play"""
        pyautogui.press('space')
        print("Action: Play")
    
    def volume_up_action(self):
        """Volume up action"""
        pyautogui.press('volumeup')
        print("Action: Volume Up")
    
    def volume_down_action(self):
        """Volume down action"""
        pyautogui.press('volumedown')
        print("Action: Volume Down")
    
    def drag_action(self):
        """Drag action - hold mouse button"""
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()
        print("Action: Drag")
    
    def move_mouse_action(self, hand_pos):
        """Move mouse based on hand position"""
        if hand_pos:
            # Map hand position to screen coordinates
            screen_x = int(hand_pos[0] * self.screen_width / 1280)
            screen_y = int(hand_pos[1] * self.screen_height / 720)
            
            # Apply smoothing
            if self.last_mouse_pos:
                screen_x = int(0.7 * screen_x + 0.3 * self.last_mouse_pos[0])
                screen_y = int(0.7 * screen_y + 0.3 * self.last_mouse_pos[1])
            
            pyautogui.moveTo(screen_x, screen_y)
            self.last_mouse_pos = (screen_x, screen_y)
    
    def process_frame(self, frame):
        """Process a single frame and detect gestures"""
        try:
            # Detect hand using simple method
            hand_center, area, contour = self.detect_hand_simple(frame)
            
            # Estimate gesture
            gesture = self.estimate_gesture_simple(hand_center, area, contour)
            
            # Add debug information
            if hand_center:
                cv2.putText(frame, f"Hand Area: {area:.0f}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame, f"Normalized: {area/10000:.2f}", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            else:
                cv2.putText(frame, "No hand detected", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            return frame, gesture, hand_center
        except Exception as e:
            print(f"Error processing frame: {e}")
            return frame, None, None
    
    def run(self):
        """Main application loop"""
        if not self.cap.isOpened():
            print("❌ Camera not available!")
            return
        
        print("🤖 Working Hand Gesture Controller")
        print("Press 'q' to quit")
        print("\nGesture Guide:")
        print("- Large hand area: Open Palm (Idle)")
        print("- Medium hand area: Two Fingers (Play)")
        print("- Small hand area: Point (Move Mouse)")
        print("- Very small area: Fist (Stop)")
        print("\n💡 Tips:")
        print("- Ensure good lighting")
        print("- Keep your hand clearly visible")
        print("- Make gestures slowly and deliberately")
        
        frame_count = 0
        start_time = time.time()
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to read frame from camera")
                    break
                
                frame_count += 1
                
                # Process frame
                frame, gesture, hand_pos = self.process_frame(frame)
                
                # Handle gestures
                if gesture and gesture != self.last_gesture:
                    self.last_gesture = gesture
                    self.gesture_cooldown = time.time()
                    
                    print(f"🎯 Detected: {self.gestures.get(gesture, 'Unknown')}")
                    
                    # Execute action
                    if gesture in self.action_mappings:
                        if gesture == 'point':
                            self.action_mappings[gesture](hand_pos)
                        else:
                            self.action_mappings[gesture]()
                
                # Handle mouse movement for point gesture
                if gesture == 'point' and hand_pos:
                    self.move_mouse_action(hand_pos)
                
                # Display gesture info on camera frame
                if gesture:
                    cv2.putText(frame, f"Gesture: {self.gestures.get(gesture, 'Unknown')}", 
                              (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Action: {self.gestures.get(gesture, 'None')}", 
                              (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                
                # Add FPS counter
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time if elapsed_time > 0 else 0
                cv2.putText(frame, f"FPS: {fps:.1f}", (10, frame.shape[0] - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                # Display frame
                cv2.imshow('Working Hand Gesture Controller', frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Cleanup completed")

if __name__ == "__main__":
    controller = WorkingHandGestureController()
    controller.run() 