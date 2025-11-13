# config/settings.py
"""
⚙️ CONFIGURATION SETTINGS - Application Configuration
"""

import os
from datetime import datetime

class Config:
    """Application configuration settings"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'advanced_forensic_secret_2024')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Forensic settings
    MAX_EXTRACTION_TIME = 300  # 5 minutes
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    SUPPORTED_PLATFORMS = ['android', 'ios']
    
    # AI Analysis settings
    AI_CONFIDENCE_THRESHOLD = 0.7
    ENABLE_REAL_TIME_ANALYSIS = True
    
    # Security settings
    ENABLE_AUTHENTICATION = False
    ALLOW_REMOTE_ACCESS = True
    
    # Storage settings
    UPLOAD_FOLDER = 'uploads'
    EXTRACTION_FOLDER = 'extracted_data'
    REPORT_FOLDER = 'reports'
    LOG_FOLDER = 'logs'
    
    @classmethod
    def get_version(cls):
        """Get application version"""
        return "2.0.0"
    
    @classmethod
    def get_build_date(cls):
        """Get build date"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")