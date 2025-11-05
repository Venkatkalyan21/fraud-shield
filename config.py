"""
Configuration file for the Fraud Detection System
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"


MODEL_PATHS = [
    MODELS_DIR / "random_forest_fraud.pkl",
    MODELS_DIR / "logistic_regression_fraud.pkl",
    BASE_DIR / "creditcard.pkl",
]

# Risk thresholds
RISK_THRESHOLDS = {
    "LOW": 2.0,      # Below 2% fraud rate
    "MEDIUM": 5.0,   # 2-5% fraud rate
    "HIGH": 5.0      # Above 5% fraud rate
}

# UI Configuration (updated to match Fraud Shield branding)
UI_CONFIG = {
    "page_title": "Fraud Shield — Redefining Financial Security",
    "page_icon": "🛡️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Feature columns (expected in CSV)
FEATURE_COLUMNS = [f"V{i}" for i in range(1, 29)] + ["Amount"]

# Colors for visualizations
COLORS = {
    "legitimate": "#28a745",   # Bootstrap green
    "fraudulent": "#dc3545",   # Bootstrap red
    "primary": "#007BFF",      # Fraud Shield blue
    "secondary": "#5aa3ff"     # Lighter accent blue
}

# File upload settings
UPLOAD_SETTINGS = {
    "max_file_size": 200 * 1024 * 1024,  # 200MB
    "allowed_types": ["csv"],
    "encoding": "utf-8"
}

# Ensure directories exist
def ensure_directories():
    """Create necessary directories if they don't exist"""
    MODELS_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

# Call this when module is imported
ensure_directories()
