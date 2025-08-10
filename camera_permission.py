#!/usr/bin/env python3
"""
Camera Permission Fix for macOS
"""

import cv2
import sys
import subprocess
import platform

def check_macos_camera_permissions():
    """Check and provide guidance for macOS camera permissions"""
    if platform.system() != "Darwin":
        print("This script is for macOS camera permission issues.")
        return False
    
    print("🔧 macOS Camera Permission Fix")
    print("=" * 40)
    
    print("\n📋 Steps to fix camera permissions:")
    print("1. Go to System Preferences > Security & Privacy > Privacy")
    print("2. Select 'Camera' from the left sidebar")
    print("3. Make sure your terminal/IDE is allowed to access the camera")
    print("4. If not listed, click the '+' button and add your terminal/IDE")
    print("5. Restart your terminal/IDE after granting permissions")
    
    print("\n🔍 Checking current camera access...")
    
    # Try to access camera
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(" Camera is accessible!")
            cap.release()
            return True
        else:
            print(" Camera opened but can't read frames")
            cap.release()
    else:
        print(" Camera not accessible")
    
    return False

def try_different_camera_indices():
    """Try different camera indices"""
    print("\n🔍 Trying different camera indices...")
    
    for i in range(5):
        print(f"Trying camera index {i}...")
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ Camera {i} works! Frame size: {frame.shape}")
                cap.release()
                return i
            else:
                print(f"❌ Camera {i} opened but no frames")
                cap.release()
        else:
            print(f"❌ Camera {i} not accessible")
    
    return None

def create_camera_test_script():
    """Create a simple camera test script"""
    test_script = '''#!/usr/bin/env python3
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
'''
    
    with open("quick_camera_test.py", "w") as f:
        f.write(test_script)
    
    print("✅ Created quick_camera_test.py")

def main():
    """Main function"""
    print("🎥 Camera Permission Troubleshooter")
    print("=" * 40)
    
    # Check if we're on macOS
    if platform.system() == "Darwin":
        print("Detected macOS - checking camera permissions...")
        
        if check_macos_camera_permissions():
            print("\n✅ Camera permissions appear to be working!")
        else:
            print("\n❌ Camera permissions need to be fixed.")
            print("Please follow the steps above to grant camera access.")
        
        # Try different camera indices
        working_index = try_different_camera_indices()
        if working_index is not None:
            print(f"\n✅ Found working camera at index {working_index}")
            print("You can modify your scripts to use this camera index.")
        else:
            print("\n❌ No working camera found.")
    
    # Create test script
    create_camera_test_script()
    
    print("\n📝 Next steps:")
    print("1. Run: python quick_camera_test.py")
    print("2. If that works, try: python simple_gesture_controller_no_mediapipe.py")
    print("3. If still having issues, check System Preferences > Security & Privacy > Camera")

if __name__ == "__main__":
    main() 
