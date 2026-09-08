import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(DATA_DIR, "terrasync.db")

os.makedirs(DATA_DIR, exist_ok=True)

# Risk Threshold Constants
HIGH_RISK_THRESHOLD = 0.70
MEDIUM_RISK_THRESHOLD = 0.40

# Supported Languages
SUPPORTED_LANGUAGES = ["en", "hi", "te", "pa"]
DEFAULT_LANGUAGE = "hi"
