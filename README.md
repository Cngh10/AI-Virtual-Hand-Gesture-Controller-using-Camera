# 🤖 AI Virtual Hand Gesture Controller using Camera

A real-time hand gesture recognition system that uses your webcam to detect hand movements and gestures, mapping them to control various system functions like mouse movement, volume control, and more - all with no external hardware required!

## ✨ Features

### 🎯 Core Features
- **Real-time Hand Detection**: Uses MediaPipe Hands to detect 21 hand landmarks in real-time
- **Gesture Recognition**: Recognizes 8 different hand gestures:
  - Open Palm (5 fingers) → Idle/Ready
  - Fist (0 fingers) → Stop/Pause
  - Thumbs Up → Confirm/Click
  - Two Fingers → Play
  - Three Fingers → Volume Up
  - Four Fingers → Volume Down
  - Point (index finger) → Move Mouse
  - Pinch (thumb + index) → Drag & Drop

### 🎮 Control Actions
- **Mouse Control**: Move cursor with hand position
- **Keyboard Simulation**: Press spacebar, enter, volume keys
- **Volume Control**: Adjust system volume with gestures
- **Click Actions**: Simulate mouse clicks and drag operations

### 🎨 Optional Features
- **Virtual Robot Arm**: Interactive 3D robot arm simulation using Pygame
- **Text-to-Speech**: Voice feedback for actions performed
- **Gesture History**: Track and log gesture patterns

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Webcam or laptop camera
- Good lighting for hand detection

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd AI-Virtual-Hand-Gesture-Controller-using-Camera
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

#### Option 1: Full Version (with Virtual Robot Arm)
```bash
python hand_gesture_controller.py
```

#### Option 2: Simple Version (camera only)
```bash
python simple_gesture_controller.py
```

## 🎯 Usage Guide

### Starting the Application
1. Run one of the Python scripts
2. Position your hand in front of the camera
3. Make gestures to control your system
4. Press 'q' to quit

### Gesture Guide

| Gesture | Description | Action |
|---------|-------------|--------|
| 🖐️ Open Palm | All 5 fingers extended | Idle/Ready state |
| ✊ Fist | All fingers closed | Stop/Pause media |
| 👍 Thumbs Up | Only thumb extended | Confirm/Click |
| ✌️ Two Fingers | Index and middle finger | Play media |
| 🤟 Three Fingers | Index, middle, ring finger | Volume Up |
| 🖖 Four Fingers | All except thumb | Volume Down |
| 👆 Point | Only index finger | Move mouse cursor |
| 🤏 Pinch | Thumb and index close | Drag & Drop |

### Tips for Best Performance
- Ensure good lighting
- Keep your hand clearly visible to the camera
- Make gestures slowly and deliberately
- Position your hand at a comfortable distance (20-50cm from camera)
- Avoid rapid hand movements

## 📁 Project Structure

```
AI Virtual Hand Gesture Controller using Camera/
├── hand_gesture_controller.py      # Full version with robot arm
├── simple_gesture_controller.py    # Simple version (camera only)
├── requirements.txt                # Python dependencies
└── README.md                      # This file
```

## 🔧 Technical Details

### Technologies Used
- **OpenCV**: Video capture and image processing
- **MediaPipe**: Real-time hand landmark detection
- **PyAutoGUI**: System control (mouse, keyboard, volume)
- **NumPy**: Numerical computations
- **Pygame**: Virtual robot arm simulation (full version)
- **pyttsx3**: Text-to-speech feedback (full version)

### Hand Landmark Detection
The system uses MediaPipe's 21-point hand landmark model:
- 4 landmarks per finger (tip, pip, dip, mcp)
- 1 landmark for wrist
- Real-time tracking with confidence thresholds

### Gesture Recognition Algorithm
1. **Finger Extension Detection**: Compare tip-to-palm vs base-to-palm distances
2. **Gesture Classification**: Map finger combinations to gestures
3. **Action Mapping**: Execute corresponding system actions
4. **Smoothing**: Apply temporal smoothing to reduce jitter

## 🎮 Virtual Robot Arm (Full Version)

The full version includes an interactive 3D robot arm simulation:
- **Real-time Control**: Arm segments follow hand movements
- **Visual Feedback**: Color-coded arm segments
- **Gesture Display**: Shows current gesture on screen
- **Smooth Animation**: 30 FPS rendering

### Robot Arm Features
- **3-Segment Arm**: Shoulder, elbow, and wrist joints
- **Hand Tracking**: Arm follows hand position and orientation
- **Visual Design**: Colorful segments with end effector
- **Gesture Integration**: Displays current gesture status

## 🚀 Advanced Features

### Custom Gesture Mapping
You can easily modify the gesture-to-action mappings in the code:

```python
# In the controller class
self.action_mappings = {
    'open_palm': self.idle_action,
    'fist': self.stop_action,
    # Add your custom mappings here
}
```

### Performance Optimization
- **Confidence Thresholds**: Adjustable detection sensitivity
- **Frame Rate Control**: Configurable processing speed
- **Memory Management**: Efficient landmark tracking
- **Error Handling**: Graceful degradation on detection failures

## 🔍 Troubleshooting

### Common Issues

**Camera not detected:**
- Check camera permissions
- Try different camera index (0, 1, 2)
- Ensure no other application is using the camera

**Poor gesture recognition:**
- Improve lighting conditions
- Clean camera lens
- Adjust hand distance from camera
- Make gestures more deliberately

**System control not working:**
- Check PyAutoGUI permissions
- Ensure no antivirus blocking automation
- Test with simple mouse movements first

### Performance Tips
- Close unnecessary applications
- Use dedicated GPU if available
- Adjust camera resolution if needed
- Monitor CPU usage during operation

## 🤝 Contributing

Contributions are welcome! Here are some ideas:
- Add new gesture recognition patterns
- Implement machine learning for gesture learning
- Create custom action mappings
- Improve the virtual robot arm
- Add support for multiple hands
- Implement gesture recording and playback

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **MediaPipe**: For excellent hand landmark detection
- **OpenCV**: For computer vision capabilities
- **PyAutoGUI**: For system automation
- **Pygame**: For interactive graphics

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the code comments for configuration options
3. Test with the simple version first
4. Ensure all dependencies are properly installed

---

**Enjoy controlling your computer with just your hands! 🎉** 