"""Configuration and environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

# Model paths
MODEL_DIR = os.getenv("MODEL_DIR", "models")
CROP_HEALTH_MODEL = os.path.join(MODEL_DIR, "crop_health", "model.pt")
DAMAGE_MODEL = os.path.join(MODEL_DIR, "damage", "model.pt")
YIELD_MODEL = os.path.join(MODEL_DIR, "yield", "yield_model.pkl")   # matches train.py output
RISK_MODEL = os.path.join(MODEL_DIR, "risk", "risk_model.pkl")     # matches train.py output

# Confidence thresholds
MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", "0.7"))

# External APIs
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
SATELLITE_API_KEY = os.getenv("SATELLITE_API_KEY")

# Storage
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/uploads")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
