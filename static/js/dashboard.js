// static/js/dashboard.js
class ForensicDashboard {
    constructor() {
        this.socket = io();
        this.initializeSocket();
        this.loadSystemStatus();
        this.startAutoRefresh();
    }

    initializeSocket() {
        this.socket.on('connect', () => {
            this.addActivityLog('Connected to forensic system');
        });

        this.socket.on('system_status_update', (data) => {
            this.updateSystemStatus(data);
        });

        this.socket.on('live_monitoring_update', (data) => {
            this.updateMonitoringData(data);
        });

        this.socket.on('extraction_progress', (data) => {
            this.updateExtractionProgress(data);
        });

        this.socket.on('extraction_completed', (data) => {
            this.addActivityLog('Data extraction completed successfully');
        });
    }

    async loadSystemStatus() {
        try {
            const response = await fetch('/api/system/status');
            const status = await response.json();
            this.updateSystemStatus(status);
        } catch (error) {
            console.error('Error loading system status:', error);
        }
    }

    updateSystemStatus(status) {
        // Update ADB status
        const adbStatus = document.getElementById('adb-status-text');
        const adbDot = document.querySelector('#adb-status .status-dot');
        
        if (status.adb_available) {
            adbStatus.textContent = 'Available';
            adbDot.className = 'status-dot online';
        } else {
            adbStatus.textContent = 'Not Available';
            adbDot.className = 'status-dot';
        }

        // Update iOS status
        const iosStatus = document.getElementById('ios-status-text');
        const iosDot = document.querySelector('#ios-status .status-dot');
        
        if (status.ios_support) {
            iosStatus.textContent = 'Supported';
            iosDot.className = 'status-dot online';
        } else {
            iosStatus.textContent = 'Limited';
            iosDot.className = 'status-dot';
        }

        // Update device count
        document.getElementById('active-devices').textContent = status.devices_connected;
        document.getElementById('devices-count').textContent = status.devices_connected;

        // Update monitoring status
        const monitoringStatus = document.getElementById('monitoring-status');
        if (status.monitoring_active) {
            monitoringStatus.textContent = 'Active';
            monitoringStatus.style.color = 'var(--success-color)';
        } else {
            monitoringStatus.textContent = 'Inactive';
            monitoringStatus.style.color = 'var(--danger-color)';
        }
    }

    updateMonitoringData(data) {
        document.getElementById('last-update').textContent = 
            new Date(data.timestamp).toLocaleTimeString();
        
        document.getElementById('active-alerts').textContent = 
            data.system_status.alerts || 0;
    }

    async scanDevices() {
        this.addActivityLog('Scanning for connected devices...');
        
        try {
            const response = await fetch('/api/devices/scan');
            const devices = await response.json();
            
            document.getElementById('devices-count').textContent = devices.total;
            this.addActivityLog(`Found ${devices.total} devices`);
            
        } catch (error) {
            this.addActivityLog(`Device scan failed: ${error.message}`, 'error');
        }
    }

    startMonitoring() {
        this.socket.emit('start_live_monitoring');
        this.addActivityLog('Live monitoring started');
    }

    quickExtraction() {
        this.addActivityLog('Starting quick extraction...');
        // Implementation for quick extraction
    }

    generateReport() {
        this.addActivityLog('Generating forensic report...');
        // Implementation for report generation
    }

    addActivityLog(message, type = 'info') {
        const log = document.getElementById('activity-log');
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        
        const timestamp = new Date().toLocaleTimeString();
        const icon = type === 'error' ? '❌' : 'ℹ️';
        
        entry.innerHTML = `
            <span class="log-time">[${timestamp}]</span>
            <span class="log-message">${icon} ${message}</span>
        `;
        
        log.appendChild(entry);
        log.scrollTop = log.scrollHeight;
    }

    startAutoRefresh() {
        // Refresh system status every 30 seconds
        setInterval(() => {
            this.loadSystemStatus();
        }, 30000);
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.forensicDashboard = new ForensicDashboard();
});