# backend/report_generator.py
#!/usr/bin/env python3
"""
📄 REPORT GENERATOR - Professional Forensic Reports
"""

import json
import base64
import hashlib
from datetime import datetime
from typing import Dict, List, Any
import uuid

class ReportGenerator:
    """Advanced forensic report generation"""
    
    def __init__(self):
        self.report_templates = self._load_templates()
    
    def generate_comprehensive_report(self, forensic_data: Dict, ai_analysis: Dict) -> Dict[str, Any]:
        """Generate comprehensive forensic report"""
        
        report_data = {
            'report_metadata': self._generate_report_metadata(),
            'executive_summary': self._generate_executive_summary(forensic_data, ai_analysis),
            'device_information': self._format_device_info(forensic_data.get('device_info', {})),
            'data_extraction_summary': self._generate_extraction_summary(forensic_data),
            'ai_analysis_results': self._format_ai_analysis(ai_analysis),
            'risk_assessment': self._format_risk_assessment(ai_analysis.get('risk_assessment', {})),
            'security_recommendations': self._format_recommendations(ai_analysis.get('recommendations', [])),
            'technical_details': self._generate_technical_details(forensic_data),
            'conclusion': self._generate_conclusion(ai_analysis)
        }
        
        # Generate different report formats
        report_formats = {
            'html': self._generate_html_report(report_data),
            'json': self._generate_json_report(report_data),
            'executive_summary': self._generate_executive_report(report_data)
        }
        
        return {
            'report_id': str(uuid.uuid4()),
            'formats': report_formats,
            'timestamp': datetime.now().isoformat(),
            'data_hash': self._generate_data_hash(forensic_data)
        }
    
    def _generate_report_metadata(self) -> Dict[str, Any]:
        """Generate report metadata"""
        
        return {
            'report_id': str(uuid.uuid4()),
            'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'version': '2.0',
            'tool': 'Advanced Mobile Forensic System',
            'investigator': 'Forensic Analyst',
            'case_number': f"CASE-{datetime.now().strftime('%Y%m%d')}",
            'confidentiality': 'STRICTLY CONFIDENTIAL'
        }
    
    def _generate_executive_summary(self, forensic_data: Dict, ai_analysis: Dict) -> Dict[str, Any]:
        """Generate executive summary"""
        
        risk_assessment = ai_analysis.get('risk_assessment', {})
        device_info = forensic_data.get('device_info', {})
        
        return {
            'overview': f"Forensic analysis of {device_info.get('model', 'Unknown Device')}",
            'key_findings': self._extract_key_findings(forensic_data, ai_analysis),
            'risk_level': risk_assessment.get('level', 'UNKNOWN'),
            'risk_score': risk_assessment.get('score', 0),
            'critical_issues': self._identify_critical_issues(ai_analysis),
            'immediate_actions': self._get_immediate_actions(risk_assessment)
        }
    
    def _generate_extraction_summary(self, forensic_data: Dict) -> Dict[str, Any]:
        """Generate data extraction summary"""
        
        summary = {}
        
        for data_type, data in forensic_data.items():
            if isinstance(data, list):
                summary[data_type] = len(data)
            elif isinstance(data, dict):
                summary[data_type] = f"{len(data)} items"
            else:
                summary[data_type] = 'Extracted'
        
        return summary
    
    def _format_device_info(self, device_info: Dict) -> Dict[str, Any]:
        """Format device information for report"""
        
        return {
            'basic_info': {
                'Model': device_info.get('model', 'Unknown'),
                'Manufacturer': device_info.get('manufacturer', 'Unknown'),
                'Android Version': device_info.get('android_version', 'Unknown'),
                'Serial Number': device_info.get('serial', 'Unknown')
            },
            'security_status': {
                'Rooted/Jailbroken': device_info.get('rooted', False),
                'Developer Options': device_info.get('developer_options', 'Unknown'),
                'USB Debugging': device_info.get('usb_debugging', 'Unknown')
            },
            'storage_info': device_info.get('storage_info', 'Not available')
        }
    
    def _format_ai_analysis(self, ai_analysis: Dict) -> Dict[str, Any]:
        """Format AI analysis results"""
        
        return {
            'behavioral_analysis': ai_analysis.get('behavioral_analysis', {}),
            'temporal_analysis': ai_analysis.get('temporal_analysis', {}),
            'anomaly_detection': ai_analysis.get('anomaly_detection', []),
            'threat_intelligence': ai_analysis.get('threat_intelligence', {}),
            'confidence_scores': ai_analysis.get('confidence_scores', {})
        }
    
    def _format_risk_assessment(self, risk_assessment: Dict) -> Dict[str, Any]:
        """Format risk assessment for report"""
        
        return {
            'overall_risk': {
                'level': risk_assessment.get('level', 'UNKNOWN'),
                'score': risk_assessment.get('score', 0),
                'interpretation': self._interpret_risk_level(risk_assessment.get('level', 'UNKNOWN'))
            },
            'risk_factors': risk_assessment.get('factors', []),
            'mitigation_strategy': self._generate_mitigation_strategy(risk_assessment)
        }
    
    def _format_recommendations(self, recommendations: List[Dict]) -> List[Dict[str, Any]]:
        """Format security recommendations"""
        
        formatted_recommendations = []
        
        for rec in recommendations:
            formatted_recommendations.append({
                'priority': rec.get('priority', 'MEDIUM'),
                'action': rec.get('action', ''),
                'description': rec.get('description', ''),
                'impact': rec.get('impact', 'MEDIUM'),
                'timeline': self._get_recommendation_timeline(rec.get('priority', 'MEDIUM'))
            })
        
        return formatted_recommendations
    
    def _generate_technical_details(self, forensic_data: Dict) -> Dict[str, Any]:
        """Generate technical details section"""
        
        return {
            'extraction_methodology': 'Advanced forensic extraction using multiple techniques',
            'data_verification': 'SHA-256 hashing and integrity checks',
            'tools_used': ['ADB', 'Content Providers', 'File System Analysis', 'AI Analysis'],
            'timeline_analysis': 'Temporal pattern recognition applied',
            'data_preservation': 'Chain of custody maintained'
        }
    
    def _generate_conclusion(self, ai_analysis: Dict) -> Dict[str, Any]:
        """Generate report conclusion"""
        
        risk_level = ai_analysis.get('risk_assessment', {}).get('level', 'UNKNOWN')
        
        return {
            'summary': self._generate_conclusion_summary(risk_level),
            'next_steps': self._get_next_steps(risk_level),
            'legal_considerations': 'All procedures followed legal and ethical guidelines',
            'contact_information': 'Forensic Team - security@organization.com'
        }
    
    # Helper methods
    def _load_templates(self) -> Dict[str, Any]:
        """Load report templates"""
        
        return {
            'html': self._get_html_template(),
            'executive': self._get_executive_template()
        }
    
    def _extract_key_findings(self, forensic_data: Dict, ai_analysis: Dict) -> List[str]:
        """Extract key findings from analysis"""
        
        findings = []
        risk_assessment = ai_analysis.get('risk_assessment', {})
        
        findings.append(f"Overall Risk Level: {risk_assessment.get('level', 'UNKNOWN')}")
        
        if forensic_data.get('device_info', {}).get('rooted', False):
            findings.append("Device shows signs of rooting/jailbreaking")
        
        anomalies = ai_analysis.get('anomaly_detection', [])
        if anomalies:
            findings.append(f"Detected {len(anomalies)} security anomalies")
        
        return findings
    
    def _identify_critical_issues(self, ai_analysis: Dict) -> List[str]:
        """Identify critical security issues"""
        
        critical_issues = []
        risk_level = ai_analysis.get('risk_assessment', {}).get('level', 'UNKNOWN')
        
        if risk_level in ['HIGH', 'CRITICAL']:
            critical_issues.append("Immediate security review required")
        
        anomalies = ai_analysis.get('anomaly_detection', [])
        for anomaly in anomalies:
            if anomaly.get('severity') in ['HIGH', 'CRITICAL']:
                critical_issues.append(anomaly.get('description', 'Critical anomaly detected'))
        
        return critical_issues
    
    def _get_immediate_actions(self, risk_assessment: Dict) -> List[str]:
        """Get immediate actions based on risk assessment"""
        
        actions = []
        risk_level = risk_assessment.get('level', 'UNKNOWN')
        
        if risk_level in ['HIGH', 'CRITICAL']:
            actions.extend([
                "Isolate device from network",
                "Perform immediate security audit",
                "Review and update security policies"
            ])
        elif risk_level == 'MEDIUM':
            actions.append("Schedule security assessment within 48 hours")
        
        return actions
    
    def _interpret_risk_level(self, risk_level: str) -> str:
        """Interpret risk level for report"""
        
        interpretations = {
            'CRITICAL': 'Immediate action required - severe security compromise detected',
            'HIGH': 'Urgent attention needed - significant security risks present',
            'MEDIUM': 'Monitor closely - moderate security concerns identified',
            'LOW': 'Standard security posture - minimal risks detected',
            'UNKNOWN': 'Insufficient data for complete risk assessment'
        }
        
        return interpretations.get(risk_level, 'Risk level interpretation not available')
    
    def _generate_mitigation_strategy(self, risk_assessment: Dict) -> List[str]:
        """Generate risk mitigation strategy"""
        
        strategy = []
        risk_level = risk_assessment.get('level', 'UNKNOWN')
        
        if risk_level in ['HIGH', 'CRITICAL']:
            strategy.extend([
                "Immediate device isolation and forensic imaging",
                "Comprehensive security review of all connected systems",
                "Implementation of enhanced monitoring and detection"
            ])
        elif risk_level == 'MEDIUM':
            strategy.append("Enhanced security controls and regular monitoring")
        
        return strategy
    
    def _get_recommendation_timeline(self, priority: str) -> str:
        """Get timeline for recommendation implementation"""
        
        timelines = {
            'HIGH': 'Immediate (within 24 hours)',
            'MEDIUM': 'Short-term (within 7 days)',
            'LOW': 'Medium-term (within 30 days)'
        }
        
        return timelines.get(priority, 'To be determined')
    
    def _generate_conclusion_summary(self, risk_level: str) -> str:
        """Generate conclusion summary based on risk level"""
        
        summaries = {
            'CRITICAL': 'Critical security issues detected requiring immediate intervention',
            'HIGH': 'Significant security risks identified needing urgent attention',
            'MEDIUM': 'Moderate security concerns that should be addressed promptly',
            'LOW': 'Standard security posture with minimal identified risks',
            'UNKNOWN': 'Incomplete assessment - additional analysis recommended'
        }
        
        return summaries.get(risk_level, 'Assessment completed')
    
    def _get_next_steps(self, risk_level: str) -> List[str]:
        """Get next steps based on risk level"""
        
        next_steps = []
        
        if risk_level in ['HIGH', 'CRITICAL']:
            next_steps.extend([
                "Immediate incident response activation",
                "Forensic preservation of all evidence",
                "Legal and compliance team notification"
            ])
        else:
            next_steps.append("Continue with standard security monitoring procedures")
        
        return next_steps
    
    def _generate_data_hash(self, data: Dict) -> str:
        """Generate hash of forensic data for integrity verification"""
        
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def _generate_html_report(self, report_data: Dict) -> str:
        """Generate HTML format report"""
        
        html_template = self.report_templates['html']
        
        # Replace placeholders with actual data
        html_report = html_template.replace('{{REPORT_TITLE}}', 'Mobile Forensic Analysis Report')
        html_report = html_report.replace('{{REPORT_DATE}}', report_data['report_metadata']['generated_date'])
        html_report = html_report.replace('{{EXECUTIVE_SUMMARY}}', 
                                         json.dumps(report_data['executive_summary'], indent=2))
        
        return html_report
    
    def _generate_json_report(self, report_data: Dict) -> str:
        """Generate JSON format report"""
        
        return json.dumps(report_data, indent=2)
    
    def _generate_executive_report(self, report_data: Dict) -> str:
        """Generate executive summary report"""
        
        executive_data = {
            'executive_summary': report_data['executive_summary'],
            'risk_assessment': report_data['risk_assessment'],
            'key_recommendations': report_data['security_recommendations'][:3]  # Top 3 recommendations
        }
        
        return json.dumps(executive_data, indent=2)
    
    def _get_html_template(self) -> str:
        """Get HTML report template"""
        
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>{{REPORT_TITLE}}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background: #2c3e50; color: white; padding: 20px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
        .critical { color: #e74c3c; font-weight: bold; }
        .high { color: #e67e22; }
        .medium { color: #f39c12; }
        .low { color: #27ae60; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{REPORT_TITLE}}</h1>
        <p>Generated: {{REPORT_DATE}}</p>
    </div>
    
    <div class="section">
        <h2>Executive Summary</h2>
        <pre>{{EXECUTIVE_SUMMARY}}</pre>
    </div>
</body>
</html>
'''
    
    def _get_executive_template(self) -> str:
        """Get executive report template"""
        
        return "Executive report template"