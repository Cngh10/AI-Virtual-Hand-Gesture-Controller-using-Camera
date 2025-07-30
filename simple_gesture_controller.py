import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import math
from collections import deque

class SimpleHandGestureController:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize hands detection
        self.hands = self.mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
            max_num_hands=1
        )
        
        # Initialize camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
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
    
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def get_finger_tips(self, hand_landmarks):
        """Extract finger tip coordinates"""
        tips = []
        tip_ids = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky
        
        for tip_id in tip_ids:
            tip = hand_landmarks.landmark[tip_id]
            tips.append((tip.x, tip.y))
        
        return tips
    
    def get_finger_bases(self, hand_landmarks):
        """Extract finger base coordinates"""
        bases = []
        base_ids = [2, 5, 9, 13, 17]  # thumb, index, middle, ring, pinky
        
        for base_id in base_ids:
            base = hand_landmarks.landmark[base_id]
            bases.append((base.x, base.y))
        
        return bases
    
    def is_finger_extended(self, tip, base, palm_center):
        """Check if a finger is extended"""
        tip_to_palm = self.calculate_distance(tip, palm_center)
        base_to_palm = self.calculate_distance(base, palm_center)
        return tip_to_palm > base_to_palm * 1.2
    
    def recognize_gesture(self, hand_landmarks):
        """Recognize hand gesture based on finger positions"""
        if not hand_landmarks:
            return None
        
        # Get finger tips and bases
        tips = self.get_finger_tips(hand_landmarks)
        bases = self.get_finger_bases(hand_landmarks)
        
        # Get palm center (wrist)
        wrist = hand_landmarks.landmark[0]
        palm_center = (wrist.x, wrist.y)
        
        # Check finger extensions
        extended_fingers = []
        for i, (tip, base) in enumerate(zip(tips, bases)):
            if self.is_finger_extended(tip, base, palm_center):
                extended_fingers.append(i)
        
        # Gesture recognition logic
        if len(extended_fingers) == 5:
            return 'open_palm'
        elif len(extended_fingers) == 0:
            return 'fist'
        elif len(extended_fingers) == 1 and 0 in extended_fingers:  # thumb only
            return 'thumbs_up'
        elif len(extended_fingers) == 2 and 1 in extended_fingers and 2 in extended_fingers:
            return 'two_fingers'
        elif len(extended_fingers) == 3 and 1 in extended_fingers and 2 in extended_fingers and 3 in extended_fingers:
            return 'three_fingers'
        elif len(extended_fingers) == 4 and 1 in extended_fingers and 2 in extended_fingers and 3 in extended_fingers and 4 in extended_fingers:
            return 'four_fingers'
        elif len(extended_fingers) == 1 and 1 in extended_fingers:  # index finger only
            return 'point'
        
        # Check for pinch gesture (thumb and index finger close)
        thumb_tip = tips[0]
        index_tip = tips[1]
        if self.calculate_distance(thumb_tip, index_tip) < 0.05:
            return 'pinch'
        
        return None
    
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
            screen_x = int(hand_pos[0] * self.screen_width)
            screen_y = int(hand_pos[1] * self.screen_height)
            
            # Apply smoothing
            if self.last_mouse_pos:
                screen_x = int(0.7 * screen_x + 0.3 * self.last_mouse_pos[0])
                screen_y = int(0.7 * screen_y + 0.3 * self.last_mouse_pos[1])
            
            pyautogui.moveTo(screen_x, screen_y)
            self.last_mouse_pos = (screen_x, screen_y)
    
    def process_frame(self, frame):
        """Process a single frame and detect gestures"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        gesture = None
        hand_pos = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Recognize gesture
                gesture = self.recognize_gesture(hand_landmarks)
                
                # Get hand position (wrist)
                wrist = hand_landmarks.landmark[0]
                hand_pos = (wrist.x, wrist.y)
        
        return frame, gesture, hand_pos
    
    def run(self):
        """Main application loop"""
        print("Simple Hand Gesture Controller Started!")
        print("Press 'q' to quit")
        print("\nGesture Guide:")
        print("- Open Palm (5 fingers): Idle")
        print("- Fist (0 fingers): Stop/Pause")
        print("- Thumbs Up: Confirm/Click")
        print("- Two Fingers: Play")
        print("- Three Fingers: Volume Up")
        print("- Four Fingers: Volume Down")
        print("- Point (index finger): Move Mouse")
        print("- Pinch (thumb + index): Drag")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                # Process frame
                frame, gesture, hand_pos = self.process_frame(frame)
                
                # Handle gestures
                if gesture and gesture != self.last_gesture:
                    self.last_gesture = gesture
                    self.gesture_cooldown = time.time()
                    
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
                              (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Action: {self.gestures.get(gesture, 'None')}", 
                              (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                
                # Display frame
                cv2.imshow('Simple Hand Gesture Controller', frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        self.hands.close()

if __name__ == "__main__":
    controller = SimpleHandGestureController()
    controller.run() 