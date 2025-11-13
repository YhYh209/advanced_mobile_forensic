# main.py
#!/usr/bin/env python3
"""
🚀 MAIN APPLICATION - Advanced Mobile Forensic System
Complete Forensic Solution for Android & iOS Devices
"""

import os
import sys
import logging
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.forensic_core import AdvancedForensicCore
from frontend.web_app import ForensicWebApp
from config.settings import Config

def setup_logging():
    """Setup application logging"""
    
    log_dir = Config.LOG_FOLDER
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'{log_dir}/forensic_system_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def print_banner():
    """Print application banner"""
    
    banner = f"""
    🚀 ADVANCED MOBILE FORENSIC SYSTEM v{Config.get_version()}
    {'=' * 60}
    📱 Complete Forensic Solution for Android & iOS Devices
    🤖 AI-Powered Analysis & Real-time Monitoring
    📄 Professional Reporting & Advanced Extraction
    🔒 Security-Focused Design
    {'=' * 60}
    Build: {Config.get_build_date()}
    """
    
    print(banner)

def main():
    """Main application entry point"""
    
    # Setup logging
    setup_logging()
    
    # Print banner
    print_banner()
    
    try:
        # Initialize forensic core
        logging.info("Initializing Advanced Forensic Core...")
        forensic_core = AdvancedForensicCore()
        
        # Check system status
        status = forensic_core.get_system_status()
        logging.info(f"System Status: ADB={status['adb_available']}, iOS={status['ios_support']}")
        
        # Initialize web application
        logging.info("Initializing Web Application...")
        web_app = ForensicWebApp(forensic_core)
        
        # Create necessary directories
        directories = [
            Config.UPLOAD_FOLDER,
            Config.EXTRACTION_FOLDER, 
            Config.REPORT_FOLDER,
            Config.LOG_FOLDER,
            'static/css',
            'static/js',
            'static/images',
            'templates'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Start the application
        logging.info("Starting Forensic Web Application...")
        web_app.run(
            host='0.0.0.0',
            port=5000,
            debug=Config.DEBUG
        )
        
    except Exception as e:
        logging.error(f"Application failed to start: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()