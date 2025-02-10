"""
Centralized alerting system with multiple notification channels
"""
import requests
from typing import Dict
import os
import time

class AlertManager:
    def __init__(self):
        self.config = {
            'slack_webhook': os.getenv('SLACK_WEBHOOK'),
            'email_api_key': os.getenv('EMAIL_API_KEY')
        }
        self.silenced_alerts = {}
        self.acknowledged_alerts = set()
        
    def trigger_alert(self, alert_data: Dict):
        """Route alerts based on severity"""
        if alert_data['severity'] == 'critical':
            self._send_slack(alert_data)
            self._send_email(alert_data)
        elif alert_data['severity'] == 'warning':
            self._send_slack(alert_data)
            
    def _send_slack(self, alert):
        """Post alert to Slack channel"""
        payload = {
            "text": f"🚨 {alert['title']}",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{alert['title']}*\n{alert['message']}"
                    }
                }
            ]
        }
        requests.post(self.config['slack_webhook'], json=payload)
        
    def _send_email(self, alert):
        """Send email via SMTP"""
        # Implementation using SMTP library
        pass 

    def acknowledge_alert(self, alert_id, silence_duration):
        """标记单个警报为已处理"""
        self.acknowledged_alerts.add(alert_id)
        if silence_duration > 0:
            self.silenced_alerts[alert_id] = time.time() + silence_duration

    def silence_alert_type(self, alert_type, duration):
        """静音特定类型警报"""
        self.silenced_alerts[alert_type] = time.time() + duration

    def should_trigger(self, alert):
        """检查是否应该触发警报"""
        if alert.get('id') in self.acknowledged_alerts:
            return False
        if alert['type'] in self.silenced_alerts:
            if time.time() < self.silenced_alerts[alert['type']]:
                return False
        return True 