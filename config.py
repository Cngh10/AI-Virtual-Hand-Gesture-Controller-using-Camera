# Configuration file for Hand Gesture Controller

# Camera Settings
CAMERA_INDEX = 0  # Try 1, 2 if camera not detected
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30

# MediaPipe Settings
MEDIAPIPE_MODEL_COMPLEXITY = 1  # 0, 1, or 2 (higher = more accurate but slower)
MEDIAPIPE_MIN_DETECTION_CONFIDENCE = 0.7
MEDIAPIPE_MIN_TRACKING_CONFIDENCE = 0.5
MEDIAPIPE_MAX_NUM_HANDS = 1

# Gesture Recognition Settings
FINGER_EXTENSION_THRESHOLD = 1.2  # Multiplier for finger extension detection
PINCH_DISTANCE_THRESHOLD = 0.05   # Distance threshold for pinch gesture
GESTURE_COOLDOWN_TIME = 1.0       # Seconds between gesture actions

# Mouse Control Settings
MOUSE_SMOOTHING_FACTOR = 0.7      # Smoothing for mouse movement (0.0-1.0)
MOUSE_SENSITIVITY = 2.0           # Mouse movement sensitivity

# Robot Arm Settings (Full Version)
ROBOT_ARM_WIDTH = 800
ROBOT_ARM_HEIGHT = 600
ROBOT_ARM_SEGMENTS = [150, 120, 80]  # Lengths of arm segments
ROBOT_ARM_FPS = 30

# Text-to-Speech Settings (Full Version)
TTS_RATE = 150  # Speech rate (words per minute)
TTS_VOLUME = 0.8  # Volume level (0.0-1.0)

# Gesture Mappings
GESTURE_ACTIONS = {
    'open_palm': {
        'name': 'Idle',
        'description': 'All 5 fingers extended',
        'action': 'idle'
    },
    'fist': {
        'name': 'Stop',
        'description': 'All fingers closed',
        'action': 'stop'
    },
    'thumbs_up': {
        'name': 'Confirm',
        'description': 'Only thumb extended',
        'action': 'confirm'
    },
    'two_fingers': {
        'name': 'Play',
        'description': 'Index and middle finger',
        'action': 'play'
    },
    'three_fingers': {
        'name': 'Volume Up',
        'description': 'Index, middle, ring finger',
        'action': 'volume_up'
    },
    'four_fingers': {
        'name': 'Volume Down',
        'description': 'All except thumb',
        'action': 'volume_down'
    },
    'point': {
        'name': 'Move Mouse',
        'description': 'Only index finger',
        'action': 'move_mouse'
    },
    'pinch': {
        'name': 'Drag',
        'description': 'Thumb and index close',
        'action': 'drag'
    }
}

# Keyboard Mappings
KEYBOARD_ACTIONS = {
    'stop': 'space',
    'confirm': 'enter',
    'play': 'space',
    'volume_up': 'volumeup',
    'volume_down': 'volumedown'
}

# Visual Settings
DRAW_HAND_LANDMARKS = True
DRAW_GESTURE_INFO = True
GESTURE_INFO_COLOR = (0, 255, 0)  # Green
ACTION_INFO_COLOR = (255, 0, 0)    # Red

# Performance Settings
ENABLE_SMOOTHING = True
ENABLE_GESTURE_HISTORY = True
GESTURE_HISTORY_SIZE = 10
ENABLE_VOICE_FEEDBACK = True  # Full version only
ENABLE_ROBOT_ARM = True       # Full version only

# Debug Settings
DEBUG_MODE = False
LOG_GESTURES = False
SAVE_FRAMES = False 