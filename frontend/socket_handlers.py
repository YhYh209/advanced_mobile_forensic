# frontend/socket_handlers.py
#!/usr/bin/env python3
"""
📡 SOCKET HANDLERS - Real-time WebSocket Communications
"""

from flask_socketio import emit
import threading
import time
from datetime import datetime

class SocketHandlers:
    """WebSocket event handlers for real-time communications"""
    
    def __init__(self, socketio, forensic_core):
        self.socketio = socketio
        self.forensic_core = forensic_core
        self.monitoring_thread = None
        self._setup_socket_handlers()
    
    def _setup_socket_handlers(self):
        """Setup Socket.IO event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            print('Client connected to WebSocket')
            emit('connection_established', {
                'message': 'Connected to Forensic System',
                'timestamp': datetime.now().isoformat()
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            print('Client disconnected')
        
        @self.socketio.on('start_live_monitoring')
        def handle_start_live_monitoring():
            """Start live monitoring of devices and system"""
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                return
            
            self.monitoring_thread = threading.Thread(target=self._live_monitoring_loop)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            emit('monitoring_started', {
                'status': 'active',
                'message': 'Live monitoring started'
            })
        
        @self.socketio.on('stop_live_monitoring')
        def handle_stop_live_monitoring():
            """Stop live monitoring"""
            if self.monitoring_thread:
                # Set flag to stop monitoring
                pass
            
            emit('monitoring_stopped', {
                'status': 'inactive',
                'message': 'Live monitoring stopped'
            })
        
        @self.socketio.on('request_system_status')
        def handle_system_status():
            """Send current system status"""
            status = self.forensic_core.get_system_status()
            emit('system_status_update', status)
        
        @self.socketio.on('start_extraction')
        def handle_start_extraction(data):
            """Start forensic extraction"""
            device_id = data.get('device_id')
            device_type = data.get('device_type')
            
            emit('extraction_started', {
                'device_id': device_id,
                'device_type': device_type,
                'timestamp': datetime.now().isoformat()
            })
            
            # Simulate extraction progress
            def simulate_extraction():
                stages = [
                    'Initializing extraction...',
                    'Extracting device information...',
                    'Collecting user data...',
                    'Analyzing applications...',
                    'Generating report...',
                    'Extraction completed!'
                ]
                
                for i, stage in enumerate(stages):
                    progress = (i + 1) * 100 // len(stages)
                    emit('extraction_progress', {
                        'stage': stage,
                        'progress': progress,
                        'timestamp': datetime.now().isoformat()
                    })
                    time.sleep(2)
                
                emit('extraction_completed', {
                    'success': True,
                    'message': 'Extraction completed successfully',
                    'timestamp': datetime.now().isoformat()
                })
            
            thread = threading.Thread(target=simulate_extraction)
            thread.daemon = True
            thread.start()
    
    def _live_monitoring_loop(self):
        """Live monitoring loop for real-time updates"""
        
        while True:
            try:
                # Get current system status
                system_status = self.forensic_core.get_system_status()
                
                # Get connected devices
                devices = self.forensic_core.scan_devices()
                
                # Send update to all connected clients
                self.socketio.emit('live_monitoring_update', {
                    'system_status': system_status,
                    'connected_devices': devices,
                    'timestamp': datetime.now().isoformat()
                })
                
                time.sleep(5)  # Update every 5 seconds
                
            except Exception as e:
                print(f"Monitoring loop error: {e}")
                time.sleep(10)