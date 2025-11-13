# frontend/web_app.py
#!/usr/bin/env python3
"""
🌐 FORENSIC WEB APPLICATION - Professional Web Interface
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_file, session
from flask_socketio import SocketIO
from datetime import datetime
import uuid

class ForensicWebApp:
    """Advanced forensic web application"""
    
    def __init__(self, forensic_core):
        self.app = Flask(__name__)
        self.app.secret_key = 'advanced_forensic_secret_2024'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.forensic_core = forensic_core
        
        self._setup_routes()
        self._setup_socket_handlers()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('dashboard.html')
        
        @self.app.route('/dashboard')
        def dashboard():
            return render_template('dashboard.html')
        
        @self.app.route('/devices')
        def devices():
            return render_template('devices.html')
        
        @self.app.route('/extraction')
        def extraction():
            return render_template('extraction.html')
        
        @self.app.route('/analysis')
        def analysis():
            return render_template('analysis.html')
        
        @self.app.route('/reports')
        def reports():
            return render_template('reports.html')
        
        @self.app.route('/monitoring')
        def monitoring():
            return render_template('monitoring.html')
        
        @self.app.route('/hacking')
        def hacking():
            return render_template('hacking.html')
        
        # API Routes
        @self.app.route('/api/system/status')
        def api_system_status():
            status = self.forensic_core.get_system_status()
            return jsonify(status)
        
        @self.app.route('/api/devices/scan')
        def api_scan_devices():
            devices = self.forensic_core.scan_devices()
            return jsonify(devices)
        
        @self.app.route('/api/analysis/start', methods=['POST'])
        def api_start_analysis():
            data = request.json
            device_id = data.get('device_id')
            device_type = data.get('device_type')
            
            if not device_id or not device_type:
                return jsonify({'success': False, 'error': 'Missing device parameters'})
            
            result = self.forensic_core.comprehensive_analysis(device_id, device_type)
            return jsonify(result)
        
        @self.app.route('/api/hacking/force_adb', methods=['POST'])
        def api_force_adb():
            data = request.json
            target_ip = data.get('target_ip')
            
            result = self.forensic_core.force_adb_enablement(target_ip)
            return jsonify(result)
        
        @self.app.route('/api/reports/generate', methods=['POST'])
        def api_generate_report():
            data = request.json
            analysis_id = data.get('analysis_id')
            
            # Generate report based on analysis ID
            report = {
                'report_id': str(uuid.uuid4()),
                'status': 'generated',
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(report)
    
    def _setup_socket_handlers(self):
        """Setup Socket.IO event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            print('Client connected')
            self.socketio.emit('system_status', {'message': 'Connected to Forensic System'})
        
        @self.socketio.on('start_monitoring')
        def handle_start_monitoring():
            self.forensic_core.start_real_time_monitoring()
            self.socketio.emit('monitoring_started', {'status': 'active'})
        
        @self.socketio.on('stop_monitoring')
        def handle_stop_monitoring():
            self.forensic_core.stop_real_time_monitoring()
            self.socketio.emit('monitoring_stopped', {'status': 'inactive'})
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the web application"""
        
        print(f"🚀 Starting Advanced Mobile Forensic System...")
        print(f"🌐 Web Interface: http://{host}:{port}")
        print(f"📱 Supported: Android & iOS devices")
        print(f"🤖 Features: AI Analysis, Real-time Monitoring, Professional Reports")
        
        self.socketio.run(self.app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)
