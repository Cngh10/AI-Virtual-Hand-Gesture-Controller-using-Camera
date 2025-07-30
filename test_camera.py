#!/usr/bin/env python3
"""
Simple camera test script
"""

import cv2
import sys

def test_camera():
    """Test camera access"""
    print("Testing camera access...")
    
    # Try different camera indices
    for i in range(3):
        print(f"Trying camera index {i}...")
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            print(f"✅ Camera {i} is accessible!")
            
            # Try to read a frame
            ret, frame = cap.read()
            if ret:
                print(f"✅ Camera {i} can capture frames!")
                print(f"Frame size: {frame.shape}")
                
                # Show the frame briefly
                cv2.imshow(f'Camera Test {i}', frame)
                cv2.waitKey(2000)  # Show for 2 seconds
                cv2.destroyAllWindows()
                
                cap.release()
                return i
            else:
                print(f"❌ Camera {i} cannot capture frames")
                cap.release()
        else:
            print(f"❌ Camera {i} is not accessible")
    
    print("❌ No cameras found!")
    return None

def check_permissions():
    """Check camera permissions"""
    print("\nCamera Permission Check:")
    print("If you're on macOS, you may need to:")
    print("1. Go to System Preferences > Security & Privacy > Privacy")
    print("2. Select 'Camera' from the left sidebar")
    print("3. Make sure your terminal/IDE is allowed to access the camera")
    print("4. Restart your terminal/IDE after granting permissions")
    
    print("\nIf you're on Linux, you may need to:")
    print("1. Install v4l-utils: sudo apt-get install v4l-utils")
    print("2. Check available devices: v4l2-ctl --list-devices")
    
    print("\nIf you're on Windows, you may need to:")
    print("1. Check Windows Camera app works first")
    print("2. Ensure no other app is using the camera")

if __name__ == "__main__":
    print("🎥 Camera Test Script")
    print("=" * 30)
    
    camera_index = test_camera()
    
    if camera_index is not None:
        print(f"\n✅ Camera test successful! Using camera index {camera_index}")
        print("You can now run the hand gesture controller.")
    else:
        print("\n❌ Camera test failed!")
        check_permissions()
        sys.exit(1) 