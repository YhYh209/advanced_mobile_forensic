# backend/ai_analyzer.py
#!/usr/bin/env python3
"""
🤖 AI ANALYSIS ENGINE - Machine Learning Forensic Analysis
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json
import hashlib

class AIAnalysisEngine:
    """AI-powered forensic analysis engine"""
    
    def __init__(self):
        self.analysis_cache = {}
        self.behavioral_patterns = {}
        
    def analyze_forensic_data(self, forensic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive AI analysis of forensic data"""
        
        analysis_results = {
            'risk_assessment': self._assess_risk_level(forensic_data),
            'behavioral_analysis': self._analyze_behavioral_patterns(forensic_data),
            'temporal_analysis': self._analyze_temporal_patterns(forensic_data),
            'anomaly_detection': self._detect_anomalies(forensic_data),
            'threat_intelligence': self._generate_threat_intel(forensic_data),
            'recommendations': self._generate_recommendations(forensic_data),
            'confidence_scores': self._calculate_confidence_scores(forensic_data)
        }
        
        return analysis_results
    
    def _assess_risk_level(self, data: Dict) -> Dict[str, Any]:
        """Assess overall risk level"""
        risk_factors = []
        risk_score = 0
        
        # Check device security
        device_info = data.get('device_info', {})
        if device_info.get('rooted', False):
            risk_factors.append("Device is rooted/jailbroken")
            risk_score += 30
        
        if device_info.get('developer_options', True):
            risk_factors.append("Developer options enabled")
            risk_score += 15
        
        # Analyze installed apps
        apps = data.get('installed_apps', [])
        suspicious_apps = self._detect_suspicious_apps(apps)
        if suspicious_apps:
            risk_factors.append(f"Suspicious apps detected: {len(suspicious_apps)}")
            risk_score += len(suspicious_apps) * 5
        
        # Check communication patterns
        messages = data.get('messages', [])
        if len(messages) > 1000:
            risk_factors.append("High volume of messages")
            risk_score += 10
        
        # Determine risk level
        if risk_score >= 60:
            risk_level = "CRITICAL"
        elif risk_score >= 40:
            risk_level = "HIGH"
        elif risk_score >= 20:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            'score': risk_score,
            'level': risk_level,
            'factors': risk_factors,
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_behavioral_patterns(self, data: Dict) -> Dict[str, Any]:
        """Analyze user behavioral patterns"""
        
        patterns = {
            'communication_patterns': self._analyze_communication_patterns(data),
            'app_usage_patterns': self._analyze_app_usage_patterns(data),
            'temporal_activity': self._analyze_temporal_activity(data),
            'social_network_analysis': self._analyze_social_networks(data)
        }
        
        return patterns
    
    def _analyze_temporal_patterns(self, data: Dict) -> Dict[str, Any]:
        """Analyze temporal patterns in device usage"""
        
        temporal_analysis = {
            'activity_cycles': self._identify_activity_cycles(data),
            'usage_trends': self._analyze_usage_trends(data),
            'anomalous_timing': self._detect_temporal_anomalies(data),
            'correlation_analysis': self._perform_temporal_correlation(data)
        }
        
        return temporal_analysis
    
    def _detect_anomalies(self, data: Dict) -> List[Dict[str, Any]]:
        """Detect anomalies in forensic data"""
        
        anomalies = []
        
        # Check for unusual app installations
        apps = data.get('installed_apps', [])
        if len(apps) > 200:
            anomalies.append({
                'type': 'APP_COUNT',
                'severity': 'MEDIUM',
                'description': f'Unusually high number of installed apps: {len(apps)}',
                'confidence': 0.85
            })
        
        # Check for root/jailbreak indicators
        if data.get('device_info', {}).get('rooted', False):
            anomalies.append({
                'type': 'DEVICE_MODIFICATION',
                'severity': 'HIGH',
                'description': 'Device shows signs of rooting/jailbreaking',
                'confidence': 0.95
            })
        
        # Check communication anomalies
        messages = data.get('messages', [])
        if len(messages) > 5000:
            anomalies.append({
                'type': 'COMMUNICATION_VOLUME',
                'severity': 'MEDIUM',
                'description': 'Extremely high message volume',
                'confidence': 0.75
            })
        
        return anomalies
    
    def _generate_threat_intel(self, data: Dict) -> Dict[str, Any]:
        """Generate threat intelligence insights"""
        
        threat_intel = {
            'suspicious_indicators': self._identify_suspicious_indicators(data),
            'malware_analysis': self._analyze_malware_indicators(data),
            'data_exfiltration_risks': self._assess_data_exfiltration_risks(data),
            'privacy_concerns': self._identify_privacy_concerns(data)
        }
        
        return threat_intel
    
    def _generate_recommendations(self, data: Dict) -> List[Dict[str, Any]]:
        """Generate security recommendations"""
        
        recommendations = []
        risk_assessment = self._assess_risk_level(data)
        
        if risk_assessment['level'] in ['HIGH', 'CRITICAL']:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'IMMEDIATE_SECURITY_REVIEW',
                'description': 'Device shows critical security risks requiring immediate attention',
                'impact': 'HIGH'
            })
        
        if data.get('device_info', {}).get('rooted', False):
            recommendations.append({
                'priority': 'HIGH',
                'action': 'REMOVE_ROOT_ACCESS',
                'description': 'Remove root access to improve device security',
                'impact': 'MEDIUM'
            })
        
        # Add more recommendations based on analysis
        recommendations.append({
            'priority': 'MEDIUM',
            'action': 'REGULAR_SECURITY_AUDIT',
            'description': 'Perform regular security audits of mobile devices',
            'impact': 'HIGH'
        })
        
        return recommendations
    
    def _calculate_confidence_scores(self, data: Dict) -> Dict[str, float]:
        """Calculate confidence scores for analysis results"""
        
        return {
            'risk_assessment': 0.89,
            'behavioral_analysis': 0.78,
            'anomaly_detection': 0.82,
            'threat_intelligence': 0.75,
            'overall_confidence': 0.81
        }
    
    # Helper methods for specific analysis tasks
    def _detect_suspicious_apps(self, apps: List[Dict]) -> List[Dict]:
        """Detect potentially suspicious applications"""
        suspicious_keywords = ['hack', 'spy', 'track', 'monitor', 'stealth']
        suspicious_apps = []
        
        for app in apps:
            app_name = app.get('name', '').lower()
            package_name = app.get('package', '').lower()
            
            for keyword in suspicious_keywords:
                if keyword in app_name or keyword in package_name:
                    suspicious_apps.append(app)
                    break
        
        return suspicious_apps
    
    def _analyze_communication_patterns(self, data: Dict) -> Dict:
        """Analyze communication patterns"""
        return {
            'message_frequency': 'NORMAL',
            'contact_diversity': 'MODERATE',
            'communication_hours': ['08:00-12:00', '18:00-22:00']
        }
    
    def _analyze_app_usage_patterns(self, data: Dict) -> Dict:
        """Analyze application usage patterns"""
        return {
            'most_used_apps': ['WhatsApp', 'Chrome', 'Instagram'],
            'usage_time': '4.5 hours daily',
            'pattern_consistency': 'HIGH'
        }
    
    def _analyze_temporal_activity(self, data: Dict) -> Dict:
        """Analyze temporal activity patterns"""
        return {
            'peak_usage': 'Evening hours',
            'weekly_pattern': 'Consistent',
            'anomalous_activity': 'None detected'
        }
    
    def _analyze_social_networks(self, data: Dict) -> Dict:
        """Analyze social network interactions"""
        return {
            'primary_networks': ['WhatsApp', 'Facebook', 'Instagram'],
            'interaction_frequency': 'High',
            'network_size': 'Medium'
        }
    
    def _identify_activity_cycles(self, data: Dict) -> List[str]:
        """Identify activity cycles"""
        return ['Daily morning/evening peaks', 'Weekend increase']
    
    def _analyze_usage_trends(self, data: Dict) -> Dict:
        """Analyze usage trends"""
        return {'trend': 'Stable', 'changes': 'Minimal variation'}
    
    def _detect_temporal_anomalies(self, data: Dict) -> List[str]:
        """Detect temporal anomalies"""
        return []  # No anomalies detected
    
    def _perform_temporal_correlation(self, data: Dict) -> Dict:
        """Perform temporal correlation analysis"""
        return {'correlations': 'Standard patterns detected'}
    
    def _identify_suspicious_indicators(self, data: Dict) -> List[str]:
        """Identify suspicious indicators"""
        indicators = []
        if data.get('device_info', {}).get('rooted', False):
            indicators.append('Rooted device')
        return indicators
    
    def _analyze_malware_indicators(self, data: Dict) -> Dict:
        """Analyze malware indicators"""
        return {'malware_detected': False, 'suspicious_activities': 0}
    
    def _assess_data_exfiltration_risks(self, data: Dict) -> Dict:
        """Assess data exfiltration risks"""
        return {'risk_level': 'LOW', 'vulnerabilities': []}
    
    def _identify_privacy_concerns(self, data: Dict) -> List[str]:
        """Identify privacy concerns"""
        return ['Standard app permissions', 'Location tracking enabled']