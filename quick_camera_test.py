#!/usr/bin/env python3
import cv2
import time

print("Testing camera access...")
cap = cv2.VideoCapture(0)

if cap.isOpened():
    print("Camera opened successfully!")
    ret, frame = cap.read()
    if ret:
        print(f"Frame captured! Size: {frame.shape}")
        cv2.imshow('Camera Test', frame)
        cv2.waitKey(3000)  # Show for 3 seconds
        cv2.destroyAllWindows()
        print("Camera test successful!")
    else:
        print("Failed to capture frame")
    cap.release()
else:
    print("Failed to open camera")
