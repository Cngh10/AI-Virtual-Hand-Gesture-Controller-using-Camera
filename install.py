#!/usr/bin/env python3
"""
Installation script for Hand Gesture Controller
This script helps users install dependencies and set up the system
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_camera():
    """Check if camera is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✅ Camera is working!")
                return True
            else:
                print("⚠️  Camera detected but not responding")
                return False
        else:
            print("❌ No camera detected")
            return False
    except ImportError:
        print("❌ OpenCV not installed")
        return False

def install_dependencies():
    """Install all required dependencies"""
    print("\n📦 Installing dependencies...")
    
    packages = [
        "opencv-python==4.8.1.78",
        "mediapipe==0.10.7", 
        "pyautogui==0.9.54",
        "numpy==1.24.3",
        "pygame==2.5.2",
        "pyttsx3==2.90"
    ]
    
    failed_packages = []
    
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed successfully")
        else:
            print(f"❌ Failed to install {package}")
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n⚠️  Failed to install: {', '.join(failed_packages)}")
        print("You may need to install these manually:")
        for package in failed_packages:
            print(f"  pip install {package}")
        return False
    else:
        print("\n✅ All dependencies installed successfully!")
        return True

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    modules = [
        ("cv2", "OpenCV"),
        ("mediapipe", "MediaPipe"),
        ("pyautogui", "PyAutoGUI"),
        ("numpy", "NumPy"),
        ("pygame", "Pygame"),
        ("pyttsx3", "pyttsx3")
    ]
    
    failed_imports = []
    
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"✅ {display_name} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {display_name}: {e}")
            failed_imports.append(display_name)
    
    if failed_imports:
        print(f"\n⚠️  Failed imports: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All modules imported successfully!")
        return True

def create_shortcuts():
    """Create shortcut scripts for easy running"""
    print("\n🔗 Creating shortcut scripts...")
    
    # Create run_demo.py
    demo_script = '''#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from demo import GestureDemo
demo = GestureDemo()
demo.run_demo()
'''
    
    # Create run_simple.py
    simple_script = '''#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simple_gesture_controller import SimpleHandGestureController
controller = SimpleHandGestureController()
controller.run()
'''
    
    # Create run_full.py
    full_script = '''#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from hand_gesture_controller import HandGestureController
controller = HandGestureController()
controller.run()
'''
    
    try:
        with open("run_demo.py", "w") as f:
            f.write(demo_script)
        os.chmod("run_demo.py", 0o755)
        print("✅ Created run_demo.py")
        
        with open("run_simple.py", "w") as f:
            f.write(simple_script)
        os.chmod("run_simple.py", 0o755)
        print("✅ Created run_simple.py")
        
        with open("run_full.py", "w") as f:
            f.write(full_script)
        os.chmod("run_full.py", 0o755)
        print("✅ Created run_full.py")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create shortcuts: {e}")
        return False

def show_usage_instructions():
    """Show usage instructions after installation"""
    print("\n" + "="*60)
    print("🎉 INSTALLATION COMPLETE!")
    print("="*60)
    print("\nYou can now run the hand gesture controller using:")
    print("\n1. Demo mode (no system control):")
    print("   python run_demo.py")
    print("   or")
    print("   python demo.py")
    
    print("\n2. Simple controller (camera only):")
    print("   python run_simple.py")
    print("   or")
    print("   python simple_gesture_controller.py")
    
    print("\n3. Full controller (with robot arm):")
    print("   python run_full.py")
    print("   or")
    print("   python hand_gesture_controller.py")
    
    print("\n📖 For detailed instructions, see README.md")
    print("\n🎯 Quick start:")
    print("   1. Run: python run_demo.py")
    print("   2. Position your hand in front of the camera")
    print("   3. Make gestures to see them detected")
    print("   4. Press 'q' to quit")
    
    print("\n⚠️  Note: The full controller requires system permissions")
    print("   for mouse and keyboard control.")

def main():
    """Main installation function"""
    print("🤖 Hand Gesture Controller - Installation")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed. Please check the errors above.")
        return
    
    # Test imports
    if not test_imports():
        print("\n❌ Some modules failed to import. Please reinstall dependencies.")
        return
    
    # Check camera
    print("\n📷 Checking camera...")
    camera_ok = check_camera()
    if not camera_ok:
        print("⚠️  Camera issues detected. You may need to:")
        print("   - Check camera permissions")
        print("   - Ensure no other app is using the camera")
        print("   - Try a different camera index")
    
    # Create shortcuts
    create_shortcuts()
    
    # Show usage instructions
    show_usage_instructions()

if __name__ == "__main__":
    main() 