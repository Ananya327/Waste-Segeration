from pathlib import Path

# Root directory
ROOT = Path(__file__).resolve().parent

# Sources
IMAGE = 'Image'
WEBCAM = 'Webcam'
SOURCES_LIST = [IMAGE, WEBCAM]

# Images
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'def.jfif'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'def1.jpg'

# Model
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'best.pt'   # ✅ ONLY .pt

# Webcam
WEBCAM_PATH = 0
