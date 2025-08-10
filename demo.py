#!/usr/bin/env python3
"""
Demo script for Hand Gesture Controller
This script demonstrates the capabilities of the hand gesture recognition system
"""

import cv2
import mediapipe as mp
import numpy as np
import time
from simple_gesture_controller import SimpleHandGestureController

class GestureDemo:
    def __init__(self):
        self.controller = SimpleHandGestureController()
        self.demo_mode = True
        self.gesture_count = {}
        self.start_time = time.time()
        
    def run_demo(self):
        """Run the demo with enhanced visualization and statistics"""
        print(" Hand Gesture Controller Demo")
        print("=" * 50)
        print("This demo will show you how to use hand gestures to control your computer.")
        print("Make sure you have good lighting and your hand is clearly visible.")
        print("\nGesture Guide:")
        for gesture, info in self.controller.gestures.items():
            print(f"  • {info}: {gesture}")
        print("\nPress 'q' to quit, 'h' for help, 's' for statistics")
        
        try:
            while True:
                ret, frame = self.controller.cap.read()
                if not ret:
                    break
                
                # Process frame
                frame, gesture, hand_pos = self.controller.process_frame(frame)
                
                # Update gesture statistics
                if gesture:
                    self.gesture_count[gesture] = self.gesture_count.get(gesture, 0) + 1
                
                # Handle gestures in demo mode (no actual system control)
                if gesture and gesture != self.controller.last_gesture:
                    self.controller.last_gesture = gesture
                    print(f"🎯 Detected: {self.controller.gestures.get(gesture, 'Unknown')}")
                
                # Add demo-specific overlays
                self.add_demo_overlays(frame, gesture)
                
                # Display frame
                cv2.imshow('Hand Gesture Controller Demo', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('h'):
                    self.show_help()
                elif key == ord('s'):
                    self.show_statistics()
        
        finally:
            self.controller.cleanup()
            self.show_final_statistics()
    
    def add_demo_overlays(self, frame, gesture):
        """Add demo-specific visual overlays"""
        height, width = frame.shape[:2]
        
        # Add demo banner
        cv2.putText(frame, "DEMO MODE - No system control", 
                   (10, height - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Add gesture info
        if gesture:
            gesture_name = self.controller.gestures.get(gesture, 'Unknown')
            cv2.putText(frame, f"Gesture: {gesture_name}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Add action preview
            action = self.get_action_for_gesture(gesture)
            cv2.putText(frame, f"Action: {action}", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        # Add instructions
        cv2.putText(frame, "Press 'h' for help, 's' for stats", 
                   (10, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def get_action_for_gesture(self, gesture):
        """Get the action that would be performed for a gesture"""
        action_map = {
            'open_palm': 'Idle',
            'fist': 'Stop/Pause',
            'thumbs_up': 'Confirm/Click',
            'two_fingers': 'Play',
            'three_fingers': 'Volume Up',
            'four_fingers': 'Volume Down',
            'point': 'Move Mouse',
            'pinch': 'Drag & Drop'
        }
        return action_map.get(gesture, 'None')
    
    def show_help(self):
        """Display help information"""
        print("\n" + "="*50)
        print("HELP - Hand Gesture Controller")
        print("="*50)
        print("Gesture Guide:")
        print("🖐️  Open Palm (5 fingers): Idle/Ready state")
        print("✊ Fist (0 fingers): Stop/Pause media")
        print("👍 Thumbs Up: Confirm/Click")
        print("✌️  Two Fingers: Play media")
        print("🤟 Three Fingers: Volume Up")
        print("🖖 Four Fingers: Volume Down")
        print("👆 Point (index finger): Move mouse cursor")
        print("🤏 Pinch (thumb + index): Drag & Drop")
        print("\nTips for best performance:")
        print("• Ensure good lighting")
        print("• Keep hand clearly visible")
        print("• Make gestures slowly and deliberately")
        print("• Position hand 20-50cm from camera")
        print("• Avoid rapid hand movements")
        print("="*50)
    
    def show_statistics(self):
        """Display current gesture statistics"""
        print("\n" + "="*50)
        print("GESTURE STATISTICS")
        print("="*50)
        runtime = time.time() - self.start_time
        print(f"Runtime: {runtime:.1f} seconds")
        print(f"Total gestures detected: {sum(self.gesture_count.values())}")
        print("\nGesture breakdown:")
        for gesture, count in sorted(self.gesture_count.items(), key=lambda x: x[1], reverse=True):
            gesture_name = self.controller.gestures.get(gesture, 'Unknown')
            percentage = (count / sum(self.gesture_count.values()) * 100) if self.gesture_count else 0
            print(f"  {gesture_name}: {count} times ({percentage:.1f}%)")
        print("="*50)
    
    def show_final_statistics(self):
        """Display final statistics when demo ends"""
        print("\n" + "="*50)
        print("DEMO COMPLETE - Final Statistics")
        print("="*50)
        runtime = time.time() - self.start_time
        print(f"Total runtime: {runtime:.1f} seconds")
        print(f"Total gestures detected: {sum(self.gesture_count.values())}")
        
        if self.gesture_count:
            print("\nMost used gestures:")
            sorted_gestures = sorted(self.gesture_count.items(), key=lambda x: x[1], reverse=True)
            for i, (gesture, count) in enumerate(sorted_gestures[:3]):
                gesture_name = self.controller.gestures.get(gesture, 'Unknown')
                print(f"  {i+1}. {gesture_name}: {count} times")
        
        print("\nTo use the full system with actual control:")
        print("  python simple_gesture_controller.py")
        print("="*50)

def run_calibration():
    """Run a quick camera calibration"""
    print("📷 Camera Calibration")
    print("Position your hand in the camera view and make different gestures.")
    print("This will help ensure optimal detection.")
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        model_complexity=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
        max_num_hands=1
    )
    mp_drawing = mp.solutions.drawing_utils
    
    start_time = time.time()
    detection_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                detection_count += 1
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )
                
                cv2.putText(frame, "Hand Detected!", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "No Hand Detected", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            runtime = time.time() - start_time
            cv2.putText(frame, f"Runtime: {runtime:.1f}s", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Detections: {detection_count}", (10, 100), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Camera Calibration', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()
        
        print(f"Calibration complete!")
        print(f"Runtime: {runtime:.1f} seconds")
        print(f"Hand detections: {detection_count}")
        if detection_count > 0:
            print("✅ Camera is working well!")
        else:
            print("⚠️  No hand detections. Check lighting and camera position.")

if __name__ == "__main__":
    print("🤖 Hand Gesture Controller Demo")
    print("Choose an option:")
    print("1. Run demo (no system control)")
    print("2. Run calibration")
    print("3. Run full controller")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        demo = GestureDemo()
        demo.run_demo()
    elif choice == "2":
        run_calibration()
    elif choice == "3":
        print("Starting full controller...")
        controller = SimpleHandGestureController()
        controller.run()
    else:
        print("Invalid choice. Running demo...")
        demo = GestureDemo()
        demo.run_demo() 
