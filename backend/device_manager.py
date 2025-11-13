# backend/device_manager.py
#!/usr/bin/env python3
"""
📱 DEVICE MANAGER - Mobile Device Management & Control
"""

import subprocess
import time
from typing import Dict, List, Any, Optional

class DeviceManager:
    """Mobile device management and control"""
    
    def __init__(self, adb_path: str):
        self.adb_path = adb_path
        self.connected_devices = []
    
    def force_adb_enablement(self, target_ip: str = None) -> Dict[str, Any]:
        """Force ADB enablement using various techniques"""
        
        results = {
            'success': False,
            'methods_tried': [],
            'final_status': 'Unknown'
        }
        
        # Method 1: Standard ADB connection
        if target_ip:
            result = self._try_wifi_adb(target_ip)
            results['methods_tried'].append(result)
            if result['success']:
                results['success'] = True
                results['final_status'] = 'WiFi ADB Enabled'
                return results
        
        # Method 2: USB forced enablement
        result = self._try_usb_force_enablement()
        results['methods_tried'].append(result)
        if result['success']:
            results['success'] = True
            results['final_status'] = 'USB ADB Enabled'
            return results
        
        # Method 3: Port scanning and brute force
        result = self._try_port_brute_force(target_ip)
        results['methods_tried'].append(result)
        if result['success']:
            results['success'] = True
            results['final_status'] = 'Brute Force Success'
        
        return results
    
    def _try_wifi_adb(self, target_ip: str) -> Dict[str, Any]:
        """Try WiFi ADB connection"""
        
        try:
            result = subprocess.run(
                [self.adb_path, "connect", f"{target_ip}:5555"],
                capture_output=True, text=True, timeout=10
            )
            
            return {
                'method': 'WiFi ADB',
                'success': 'connected' in result.stdout,
                'output': result.stdout,
                'target': f"{target_ip}:5555"
            }
            
        except Exception as e:
            return {
                'method': 'WiFi ADB',
                'success': False,
                'error': str(e),
                'target': f"{target_ip}:5555"
            }
    
    def _try_usb_force_enablement(self) -> Dict[str, Any]:
        """Try USB forced ADB enablement"""
        
        try:
            # Kill ADB server
            subprocess.run([self.adb_path, "kill-server"], capture_output=True)
            time.sleep(2)
            
            # Start ADB server
            subprocess.run([self.adb_path, "start-server"], capture_output=True)
            time.sleep(3)
            
            # Check for devices
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True, text=True, timeout=10
            )
            
            success = 'device' in result.stdout
            
            return {
                'method': 'USB Force Enablement',
                'success': success,
                'output': result.stdout,
                'devices_found': len([line for line in result.stdout.split('\n') if 'device' in line])
            }
            
        except Exception as e:
            return {
                'method': 'USB Force Enablement',
                'success': False,
                'error': str(e)
            }
    
    def _try_port_brute_force(self, target_ip: str) -> Dict[str, Any]:
        """Try ADB port brute force"""
        
        if not target_ip:
            return {
                'method': 'Port Brute Force',
                'success': False,
                'error': 'No target IP provided'
            }
        
        ports = [5555, 4444, 3838, 7777, 8888]
        results = []
        
        for port in ports:
            try:
                result = subprocess.run(
                    [self.adb_path, "connect", f"{target_ip}:{port}"],
                    capture_output=True, text=True, timeout=5
                )
                
                results.append({
                    'port': port,
                    'success': 'connected' in result.stdout,
                    'output': result.stdout
                })
                
                if 'connected' in result.stdout:
                    return {
                        'method': 'Port Brute Force',
                        'success': True,
                        'working_port': port,
                        'all_attempts': results
                    }
                    
            except Exception as e:
                results.append({
                    'port': port,
                    'success': False,
                    'error': str(e)
                })
        
        return {
            'method': 'Port Brute Force',
            'success': False,
            'all_attempts': results
        }
    
    def take_device_screenshot(self, device_id: str) -> Optional[str]:
        """Take screenshot of device"""
        
        try:
            screenshot_path = f"screenshots/{device_id}_{int(time.time())}.png"
            
            result = subprocess.run([
                self.adb_path, "-s", device_id, "shell", "screencap", "-p", "/sdcard/screenshot.png"
            ], capture_output=True, timeout=10)
            
            if result.returncode == 0:
                # Pull the screenshot
                subprocess.run([
                    self.adb_path, "-s", device_id, "pull", "/sdcard/screenshot.png", screenshot_path
                ], capture_output=True, timeout=10)
                
                return screenshot_path
                
        except Exception as e:
            print(f"Screenshot error: {e}")
        
        return None
    
    def record_device_screen(self, device_id: str, duration: int = 10) -> Optional[str]:
        """Record device screen"""
        
        try:
            video_path = f"recordings/{device_id}_{int(time.time())}.mp4"
            
            # Start recording
            subprocess.run([
                self.adb_path, "-s", device_id, "shell", "screenrecord", "--verbose", 
                f"--time-limit", str(duration), "/sdcard/recording.mp4"
            ], capture_output=True, timeout=duration + 5)
            
            # Pull the recording
            subprocess.run([
                self.adb_path, "-s", device_id, "pull", "/sdcard/recording.mp4", video_path
            ], capture_output=True, timeout=10)
            
            return video_path
            
        except Exception as e:
            print(f"Screen recording error: {e}")
        
        return None
    
    def get_device_logs(self, device_id: str) -> Dict[str, Any]:
        """Get comprehensive device logs"""
        
        logs = {}
        
        try:
            # Logcat logs
            result = subprocess.run([
                self.adb_path, "-s", device_id, "logcat", "-d"
            ], capture_output=True, text=True, timeout=30)
            
            logs['logcat'] = result.stdout[:10000]  # First 10000 characters
            
            # System logs
            result = subprocess.run([
                self.adb_path, "-s", device_id, "shell", "dmesg"
            ], capture_output=True, text=True, timeout=20)
            
            logs['kernel'] = result.stdout[:5000]
            
        except Exception as e:
            logs['error'] = str(e)
        
        return logs