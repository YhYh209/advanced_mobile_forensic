# frontend/api_routes.py
#!/usr/bin/env python3
"""
🔗 API ROUTES - RESTful API for Forensic Operations
"""

from flask import jsonify, request
from datetime import datetime
import uuid

class APIRoutes:
    """API routes for forensic operations"""
    
    def __init__(self, app, forensic_core):
        self.app = app
        self.forensic_core = forensic_core
        self._setup_api_routes()
    
    def _setup_api_routes(self):
        """Setup API routes"""
        
        @self.app.route('/api/devices/list')
        def api_devices_list():
            devices = self.forensic_core.scan_devices()
            return jsonify(devices)
        
        @self.app.route('/api/device/<device_type>/<device_id>/info')
        def api_device_info(device_type, device_id):
            if device_type == 'android':
                info = self.forensic_core._get_android_device_info(device_id)
            else:
                info = self.forensic_core._get_ios_device_info(device_id)
            
            return jsonify(info)
        
        @self.app.route('/api/extraction/start', methods=['POST'])
        def api_extraction_start():
            data = request.json
            device_id = data.get('device_id')
            device_type = data.get('device_type')
            
            if not device_id or not device_type:
                return jsonify({'success': False, 'error': 'Device ID and type required'})
            
            result = self.forensic_core.comprehensive_analysis(device_id, device_type)
            return jsonify(result)
        
        @self.app.route('/api/analysis/history')
        def api_analysis_history():
            history = self.forensic_core.get_extraction_history()
            return jsonify(history)
        
        @self.app.route('/api/hacking/enable_adb', methods=['POST'])
        def api_hacking_enable_adb():
            data = request.json
            target_ip = data.get('target_ip')
            
            result = self.forensic_core.force_adb_enablement(target_ip)
            return jsonify(result)
        
        @self.app.route('/api/monitoring/status')
        def api_monitoring_status():
            status = {
                'active': self.forensic_core.monitoring_active,
                'devices': len(self.forensic_core.connected_devices),
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(status)
        
        @self.app.route('/api/reports/list')
        def api_reports_list():
            # Return list of generated reports
            reports = [
                {
                    'id': str(uuid.uuid4()),
                    'name': 'Forensic Analysis Report',
                    'date': datetime.now().isoformat(),
                    'status': 'completed'
                }
            ]
            return jsonify(reports)