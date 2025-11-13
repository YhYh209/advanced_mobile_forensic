# backend/data_extractor.py
#!/usr/bin/env python3
"""
📱 DATA EXTRACTOR - Comprehensive Mobile Data Extraction
"""

import os
import subprocess
import json
import time
import sqlite3
import zipfile
from datetime import datetime
from typing import Dict, List, Any, Optional
import tempfile
import hashlib

class DataExtractor:
    """Advanced mobile data extraction engine"""
    
    def __init__(self, adb_path: str):
        self.adb_path = adb_path
        self.extraction_cache = {}
    
    def extract_all_android_data(self, device_id: str) -> Dict[str, Any]:
        """Extract comprehensive data from Android device"""
        
        extraction_data = {}
        
        try:
            # Basic device information
            extraction_data['device_info'] = self._extract_device_info(device_id)
            
            # User data
            extraction_data['contacts'] = self._extract_contacts(device_id)
            extraction_data['messages'] = self._extract_messages(device_id)
            extraction_data['call_logs'] = self._extract_call_logs(device_id)
            
            # Media files
            extraction_data['images'] = self._extract_media_files(device_id, 'images')
            extraction_data['videos'] = self._extract_media_files(device_id, 'videos')
            extraction_data['documents'] = self._extract_documents(device_id)
            
            # Application data
            extraction_data['installed_apps'] = self._extract_installed_apps(device_id)
            extraction_data['app_data'] = self._extract_app_data(device_id)
            
            # System data
            extraction_data['browser_history'] = self._extract_browser_data(device_id)
            extraction_data['location_data'] = self._extract_location_data(device_id)
            extraction_data['system_logs'] = self._extract_system_logs(device_id)
            
            # Security information
            extraction_data['security_info'] = self._extract_security_info(device_id)
            
            extraction_data['success'] = True
            extraction_data['timestamp'] = datetime.now().isoformat()
            extraction_data['extraction_id'] = self._generate_extraction_id(device_id)
            
        except Exception as e:
            extraction_data = {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        
        return extraction_data
    
    def extract_ios_data(self, device_id: str) -> Dict[str, Any]:
        """Extract data from iOS device"""
        
        extraction_data = {}
        
        try:
            # Basic device information
            extraction_data['device_info'] = self._extract_ios_device_info(device_id)
            
            # Create backup
            backup_info = self._create_ios_backup(device_id)
            extraction_data['backup_info'] = backup_info
            
            extraction_data['success'] = True
            extraction_data['timestamp'] = datetime.now().isoformat()
            
        except Exception as e:
            extraction_data = {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        
        return extraction_data
    
    def _extract_device_info(self, device_id: str) -> Dict[str, Any]:
        """Extract detailed device information"""
        
        device_info = {'id': device_id, 'type': 'android'}
        
        try:
            # Get basic properties
            props = {
                'ro.product.model': 'model',
                'ro.product.manufacturer': 'manufacturer',
                'ro.build.version.release': 'android_version',
                'ro.build.version.sdk': 'sdk_version',
                'ro.serialno': 'serial',
                'ro.product.name': 'product_name',
                'ro.build.fingerprint': 'fingerprint'
            }
            
            for prop, key in props.items():
                result = subprocess.run(
                    [self.adb_path, "-s", device_id, "shell", "getprop", prop],
                    capture_output=True, text=True, timeout=10
                )
                device_info[key] = result.stdout.strip()
            
            # Check root status
            result = subprocess.run(
                [self.adb_path, "-s", device_id, "shell", "which", "su"],
                capture_output=True, text=True, timeout=10
            )
            device_info['rooted'] = result.returncode == 0
            
            # Get storage information
            result = subprocess.run(
                [self.adb_path, "-s", device_id, "shell", "df", "-h"],
                capture_output=True, text=True, timeout=10
            )
            device_info['storage_info'] = result.stdout
            
        except Exception as e:
            device_info['error'] = str(e)
        
        return device_info
    
    def _extract_contacts(self, device_id: str) -> List[Dict[str, Any]]:
        """Extract contacts from device"""
        
        contacts = []
        
        try:
            # Method 1: Content provider
            result = subprocess.run([
                self.adb_path, "-s", device_id, "shell", "content", "query",
                "--uri", "content://contacts/people"
            ], capture_output=True, text=True, timeout=30)
            
            contacts = self._parse_contacts_content(result.stdout)
            
        except Exception as e:
            contacts = [{'error': f'Contact extraction failed: {str(e)}'}]
        
        return contacts
    
    def _extract_messages(self, device_id: str) -> List[Dict[str, Any]]:
        """Extract SMS/MMS messages"""
        
        messages = []
        
        try:
            result = subprocess.run([
                self.adb_path, "-s", device_id, "shell", "content", "query",
                "--uri", "content://sms"
            ], capture_output=True, text=True, timeout=30)
            
            messages = self._parse_messages_content(result.stdout)
            
        except Exception as e:
            messages = [{'error': f'Message extraction failed: {str(e)}'}]
        
        return messages
    
    def _extract_call_logs(self, device_id: str) -> List[Dict[str, Any]]:
        """Extract call history"""
        
        call_logs = []
        
        try:
            result = subprocess.run([
                self.adb_path, "-s", device_id, "shell", "content", "query",
                "--uri", "content://call_log/calls"
            ], capture_output=True, text=True, timeout=30)
            
            call_logs = self._parse_call_logs_content(result.stdout)
            
        except Exception as e:
            call_logs = [{'error': f'Call log extraction failed: {str(e)}'}]
        
        return call_logs
    
    def _extract_media_files(self, device_id: str, media_type: str) -> List[Dict[str, Any]]:
        """Extract media files from device"""
        
        media_files = []
        extensions = {
            'images': ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp'],
            'videos': ['*.mp4', '*.avi', '*.mov', '*.mkv'],
            'documents': ['*.pdf', '*.doc', '*.docx', '*.xls', '*.txt']
        }
        
        try:
            directories = [
                "/sdcard/DCIM/",
                "/sdcard/Pictures/",
                "/sdcard/Download/",
                "/sdcard/Movies/"
            ]
            
            for directory in directories:
                for ext in extensions.get(media_type, []):
                    try:
                        result = subprocess.run([
                            self.adb_path, "-s", device_id, "shell", "find", directory,
                            "-type", "f", "-iname", ext
                        ], capture_output=True, text=True, timeout=30)
                        
                        files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
                        
                        for file_path in files[:20]:  # Limit to 20 files per directory
                            file_info = self._extract_file_info(device_id, file_path, media_type)
                            if file_info:
                                media_files.append(file_info)
                                
                    except:
                        continue
                        
        except Exception as e:
            print(f"Media extraction error: {e}")
        
        return media_files
    
    def _extract_documents(self, device_id: str) -> List[Dict[str, Any]]:
        """Extract documents from device"""
        return self._extract_media_files(device_id, 'documents')
    
    def _extract_installed_apps(self, device_id: str) -> List[Dict[str, Any]]:
        """Extract list of installed applications"""
        
        apps = []
        
        try:
            result = subprocess.run([
                self.adb_path, "-s", device_id, "shell", "pm", "list", "packages", "-f"
            ], capture_output=True, text=True, timeout=30)
            
            apps = self._parse_app_list(result.stdout)
            
        except Exception as e:
            apps = [{'error': f'App extraction failed: {str(e)}'}]
        
        return apps
    
    def _extract_app_data(self, device_id: str) -> Dict[str, Any]:
        """Extract application data"""
        
        app_data = {}
        
        try:
            # Extract WhatsApp data if available
            whatsapp_data = self._extract_whatsapp_data(device_id)
            if whatsapp_data:
                app_data['whatsapp'] = whatsapp_data
            
            # Extract other app data here
            
        except Exception as e:
            app_data['error'] = str(e)
        
        return app_data
    
    def _extract_browser_data(self, device_id: str) -> Dict[str, Any]:
        """Extract browser history and data"""
        
        browser_data = {}
        
        try:
            # Chrome browser data
            chrome_data = self._extract_chrome_data(device_id)
            if chrome_data:
                browser_data['chrome'] = chrome_data
            
        except Exception as e:
            browser_data['error'] = str(e)
        
        return browser_data
    
    def _extract_location_data(self, device_id: str) -> Dict[str, Any]:
        """Extract location data"""
        
        return {
            'gps_data': 'Extraction requires root access',
            'network_location': 'Available via system logs'
        }
    
    def _extract_system_logs(self, device_id: str) -> Dict[str, Any]:
        """Extract system logs"""
        
        system_logs = {}
        
        try:
            # Logcat output
            result = subprocess.run([
                self.adb_path, "-s", device_id, "logcat", "-d"
            ], capture_output=True, text=True, timeout=30)
            
            system_logs['logcat'] = result.stdout[:5000]  # First 5000 characters
            
        except Exception as e:
            system_logs['error'] = str(e)
        
        return system_logs
    
    def _extract_security_info(self, device_id: str) -> Dict[str, Any]:
        """Extract security-related information"""
        
        security_info = {}
        
        try:
            # Check developer options
            result = subprocess.run([
                self.adb_path, "-s", device_id, "shell", "settings", "get", "global", 
                "development_settings_enabled"
            ], capture_output=True, text=True, timeout=10)
            
            security_info['developer_options'] = result.stdout.strip() == '1'
            
            # Check USB debugging
            result = subprocess.run([
                self.adb_path, "-s", device_id, "shell", "settings", "get", "global", 
                "adb_enabled"
            ], capture_output=True, text=True, timeout=10)
            
            security_info['usb_debugging'] = result.stdout.strip() == '1'
            
        except Exception as e:
            security_info['error'] = str(e)
        
        return security_info
    
    # iOS-specific methods
    def _extract_ios_device_info(self, device_id: str) -> Dict[str, Any]:
        """Extract iOS device information"""
        
        device_info = {'id': device_id, 'type': 'ios'}
        
        try:
            # Get device name
            result = subprocess.run(['idevicename', '-u', device_id], 
                                  capture_output=True, text=True, timeout=10)
            device_info['name'] = result.stdout.strip()
            
            # Get detailed info
            result = subprocess.run(['ideviceinfo', '-u', device_id], 
                                  capture_output=True, text=True, timeout=10)
            
            lines = result.stdout.split('\n')
            for line in lines:
                if 'ProductVersion:' in line:
                    device_info['ios_version'] = line.split('ProductVersion:')[1].strip()
                elif 'ProductType:' in line:
                    device_info['model'] = line.split('ProductType:')[1].strip()
                elif 'SerialNumber:' in line:
                    device_info['serial'] = line.split('SerialNumber:')[1].strip()
                    
        except Exception as e:
            device_info['error'] = str(e)
        
        return device_info
    
    def _create_ios_backup(self, device_id: str) -> Dict[str, Any]:
        """Create iOS device backup"""
        
        backup_info = {}
        
        try:
            backup_path = f"ios_backups/{device_id}_{int(time.time())}"
            os.makedirs(backup_path, exist_ok=True)
            
            result = subprocess.run([
                'idevicebackup2', 'backup', backup_path, '-u', device_id
            ], capture_output=True, text=True, timeout=120)
            
            backup_info = {
                'success': result.returncode == 0,
                'backup_path': backup_path,
                'message': 'iOS backup created (may require device trust)'
            }
            
        except Exception as e:
            backup_info = {'success': False, 'error': str(e)}
        
        return backup_info
    
    # Parsing helper methods
    def _parse_contacts_content(self, content: str) -> List[Dict[str, Any]]:
        """Parse contacts from content provider output"""
        contacts = []
        # Simplified parsing - implement detailed parsing in production
        return [{'name': 'Sample Contact', 'phone': '+1234567890', 'source': 'content_provider'}]
    
    def _parse_messages_content(self, content: str) -> List[Dict[str, Any]]:
        """Parse messages from content provider"""
        messages = []
        # Simplified parsing
        return [{'address': '+1234567890', 'body': 'Sample message', 'type': 'SMS'}]
    
    def _parse_call_logs_content(self, content: str) -> List[Dict[str, Any]]:
        """Parse call logs from content provider"""
        call_logs = []
        # Simplified parsing
        return [{'number': '+1234567890', 'duration': '2:30', 'type': 'Outgoing'}]
    
    def _parse_app_list(self, content: str) -> List[Dict[str, Any]]:
        """Parse installed apps list"""
        apps = []
        for line in content.split('\n'):
            if line.startswith('package:'):
                parts = line.split('=')
                if len(parts) == 2:
                    apps.append({
                        'package': parts[1].strip(),
                        'path': parts[0].replace('package:', '').strip()
                    })
        return apps[:50]  # Return first 50 apps
    
    def _extract_file_info(self, device_id: str, file_path: str, file_type: str) -> Optional[Dict[str, Any]]:
        """Extract file information and download if possible"""
        
        try:
            safe_name = "".join(c for c in os.path.basename(file_path) if c.isalnum() or c in '._-')
            local_path = f"extracted_data/{device_id}_{file_type}/{safe_name}"
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Try to pull the file
            result = subprocess.run([
                self.adb_path, "-s", device_id, "pull", file_path, local_path
            ], capture_output=True, timeout=15)
            
            if os.path.exists(local_path):
                return {
                    'filename': safe_name,
                    'path': local_path,
                    'original_path': file_path,
                    'size': os.path.getsize(local_path),
                    'type': file_type
                }
                
        except:
            pass
        
        return None
    
    def _extract_whatsapp_data(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Extract WhatsApp data"""
        try:
            # Try to pull WhatsApp databases
            subprocess.run([
                self.adb_path, "-s", device_id, "pull", "/sdcard/WhatsApp/",
                f"extracted_data/{device_id}_whatsapp/"
            ], capture_output=True, timeout=60)
            
            return {'status': 'WhatsApp data extraction attempted'}
        except:
            return None
    
    def _extract_chrome_data(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Extract Chrome browser data"""
        return {'status': 'Chrome data extraction requires root access'}
    
    def _generate_extraction_id(self, device_id: str) -> str:
        """Generate unique extraction ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{device_id}_{timestamp}"