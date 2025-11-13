# backend/forensic_core.py
#!/usr/bin/env python3
"""
🔍 ADVANCED FORENSIC CORE - Complete Mobile Forensic Engine
"""

import os
import sys
import json
import time
import subprocess
import threading
import hashlib
import uuid
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional
import sqlite3
import xml.etree.ElementTree as ET
import zipfile
import base64

class AdvancedForensicCore:
    """Advanced forensic analysis core engine"""
    
    def __init__(self):
        self.connected_devices = []
        self.analysis_results = {}
        self.extraction_history = []
        self.adb_path = self._find_adb()
        self.ios_support = self._check_ios_support()
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Initialize modules
        from .ai_analyzer import AIAnalysisEngine
        from .data_extractor import DataExtractor
        from .report_generator import ReportGenerator
        
        self.ai_engine = AIAnalysisEngine()
        self.data_extractor = DataExtractor(self.adb_path)
        self.report_generator = ReportGenerator()
    
    def _find_adb(self) -> Optional[str]:
        """Find ADB executable"""
        paths = [
            "adb", 
            "/usr/bin/adb", 
            "/usr/local/bin/adb",
            "./platform-tools/adb",
            "C:\\Platform-Tools\\adb.exe"
        ]
        
        for path in paths:
            try:
                result = subprocess.run([path, "version"], 
                                      capture_output=True, check=True, timeout=10)
                return path
            except:
                continue
        return None
    
    def _check_ios_support(self) -> bool:
        """Check if iOS forensic tools are available"""
        try:
            tools = ['idevice_id', 'ideviceinfo']
            for tool in tools:
                result = subprocess.run(['which', tool], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    return False
            return True
        except:
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            'adb_available': self.adb_path is not None,
            'adb_path': self.adb_path,
            'ios_support': self.ios_support,
            'platform': sys.platform,
            'python_version': sys.version,
            'timestamp': datetime.now().isoformat(),
            'devices_connected': len(self.connected_devices),
            'monitoring_active': self.monitoring_active
        }
    
    def scan_devices(self) -> Dict[str, List]:
        """Scan for all connected devices"""
        devices = {'android': [], 'ios': [], 'total': 0}
        
        # Scan Android devices
        if self.adb_path:
            try:
                result = subprocess.run([self.adb_path, "devices", "-l"], 
                                      capture_output=True, text=True, timeout=15)
                lines = result.stdout.strip().split('\n')[1:]
                
                for line in lines:
                    if line.strip() and 'device' in line:
                        parts = line.split()
                        device_id = parts[0]
                        device_info = self._get_android_device_info(device_id)
                        devices['android'].append(device_info)
                        
            except Exception as e:
                print(f"Android scan error: {e}")
        
        # Scan iOS devices
        if self.ios_support:
            try:
                result = subprocess.run(['idevice_id', '-l'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    ios_devices = result.stdout.strip().split('\n')
                    for device_id in ios_devices:
                        if device_id:
                            device_info = self._get_ios_device_info(device_id)
                            devices['ios'].append(device_info)
                            
            except Exception as e:
                print(f"iOS scan error: {e}")
        
        devices['total'] = len(devices['android']) + len(devices['ios'])
        self.connected_devices = devices
        return devices
    
    def _get_android_device_info(self, device_id: str) -> Dict[str, Any]:
        """Get detailed Android device information"""
        info = {
            'id': device_id,
            'type': 'android',
            'status': 'connected',
            'model': 'Unknown',
            'version': 'Unknown',
            'manufacturer': 'Unknown',
            'serial': 'Unknown'
        }
        
        try:
            # Get basic properties
            props = {
                'ro.product.model': 'model',
                'ro.product.manufacturer': 'manufacturer',
                'ro.build.version.release': 'version',
                'ro.serialno': 'serial',
                'ro.product.name': 'name'
            }
            
            for prop, key in props.items():
                result = subprocess.run(
                    [self.adb_path, "-s", device_id, "shell", "getprop", prop],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    info[key] = result.stdout.strip()
            
            # Get additional info
            try:
                # Storage info
                result = subprocess.run(
                    [self.adb_path, "-s", device_id, "shell", "df", "-h", "/sdcard"],
                    capture_output=True, text=True, timeout=10
                )
                info['storage'] = result.stdout
            except:
                info['storage'] = "Unknown"
                
        except Exception as e:
            info['error'] = str(e)
        
        return info
    
    def _get_ios_device_info(self, device_id: str) -> Dict[str, Any]:
        """Get iOS device information"""
        info = {'id': device_id, 'type': 'ios', 'status': 'connected'}
        
        try:
            # Get device name
            result = subprocess.run(['idevicename', '-u', device_id], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                info['name'] = result.stdout.strip()
            
            # Get detailed info
            result = subprocess.run(['ideviceinfo', '-u', device_id], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'ProductVersion:' in line:
                        info['version'] = line.split('ProductVersion:')[1].strip()
                    elif 'ProductType:' in line:
                        info['model'] = line.split('ProductType:')[1].strip()
                    elif 'ProductName:' in line:
                        info['product_name'] = line.split('ProductName:')[1].strip()
        
        except Exception as e:
            info['error'] = str(e)
        
        return info
    
    def comprehensive_analysis(self, device_id: str, device_type: str) -> Dict[str, Any]:
        """Perform comprehensive forensic analysis"""
        analysis_data = {}
        
        try:
            # Extract device data
            if device_type == 'android':
                extraction_result = self.data_extractor.extract_all_android_data(device_id)
            else:
                extraction_result = self.data_extractor.extract_ios_data(device_id)
            
            if not extraction_result['success']:
                return {'success': False, 'error': extraction_result['error']}
            
            # Run AI analysis
            ai_analysis = self.ai_engine.analyze_forensic_data(extraction_result['data'])
            
            # Generate report
            report = self.report_generator.generate_comprehensive_report(
                extraction_result['data'], ai_analysis
            )
            
            analysis_data = {
                'success': True,
                'device_data': extraction_result['data'],
                'ai_analysis': ai_analysis,
                'report': report,
                'extraction_id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat()
            }
            
            # Save to history
            self.extraction_history.append(analysis_data)
            
        except Exception as e:
            analysis_data = {'success': False, 'error': str(e)}
        
        return analysis_data
    
    def start_real_time_monitoring(self):
        """Start real-time device monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_real_time_monitoring(self):
        """Stop monitoring"""
        self.monitoring_active = False
    
    def _monitoring_loop(self):
        """Real-time monitoring loop"""
        while self.monitoring_active:
            try:
                # Monitor device connections
                current_devices = self.scan_devices()
                
                # Monitor system activities
                system_status = self.get_system_status()
                
                # Log monitoring data
                monitoring_data = {
                    'timestamp': datetime.now().isoformat(),
                    'devices': current_devices,
                    'system_status': system_status,
                    'alerts': self._check_security_alerts()
                }
                
                # Store monitoring data
                self._store_monitoring_data(monitoring_data)
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(30)
    
    def _check_security_alerts(self) -> List[str]:
        """Check for security alerts"""
        alerts = []
        
        # Check for suspicious activities
        if len(self.connected_devices) > 5:
            alerts.append("High number of connected devices detected")
        
        # Add more security checks here
        return alerts
    
    def _store_monitoring_data(self, data: Dict):
        """Store monitoring data"""
        try:
            log_file = f"logs/monitoring_{datetime.now().strftime('%Y%m%d')}.json"
            os.makedirs("logs", exist_ok=True)
            
            with open(log_file, 'a') as f:
                f.write(json.dumps(data) + '\n')
        except Exception as e:
            print(f"Error storing monitoring data: {e}")
    
    def get_extraction_history(self) -> List[Dict]:
        """Get extraction history"""
        return self.extraction_history[-50:]  # Last 50 extractions
    
    def force_adb_enablement(self, target_ip: str = None) -> Dict[str, Any]:
        """Force ADB enablement on target"""
        attempts = []
        
        if target_ip:
            # Try WiFi ADB
            try:
                result = subprocess.run(
                    [self.adb_path, "connect", f"{target_ip}:5555"],
                    capture_output=True, text=True, timeout=10
                )
                attempts.append(f"WiFi ADB: {result.stdout}")
                if "connected" in result.stdout:
                    return {'success': True, 'message': 'ADB enabled via WiFi'}
            except Exception as e:
                attempts.append(f"WiFi ADB failed: {str(e)}")
        
        # Try USB methods
        try:
            subprocess.run([self.adb_path, "kill-server"], capture_output=True)
            time.sleep(2)
            subprocess.run([self.adb_path, "start-server"], capture_output=True)
            time.sleep(3)
            
            result = subprocess.run([self.adb_path, "devices"], 
                                  capture_output=True, text=True, timeout=10)
            attempts.append(f"USB Detection: {result.stdout}")
            
            if "device" in result.stdout:
                return {'success': True, 'message': 'ADB enabled via USB'}
                
        except Exception as e:
            attempts.append(f"USB method failed: {str(e)}")
        
        return {'success': False, 'attempts': attempts}