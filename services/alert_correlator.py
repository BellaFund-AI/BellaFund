from sklearn.metrics.pairwise import cosine_similarity

class AlertCorrelator:
    def find_related_alerts(self, alert_id):
        """Identify related alert events"""
        base_alert = alert_repo.get_alert(alert_id)
        return [
            alert for alert in alert_repo.get_recent_alerts(168)  # Last 7 days
            if self._is_related(base_alert, alert)
        ]
    
    def _is_related(self, alert1, alert2):
        """Determine alert correlation"""
        time_diff = abs((alert1['timestamp'] - alert2['timestamp']).total_seconds())
        return (
            alert1['type'] == alert2['type'] or
            time_diff < 3600  # Alerts within 1 hour
        ) 

class AdvancedAlertCorrelator(AlertCorrelator):
    def _is_related(self, alert1, alert2):
        """Enhanced correlation detection logic"""
        # Add feature similarity check
        feature_sim = cosine_similarity(
            alert1['feature_vector'],
            alert2['feature_vector']
        )
        return super()._is_related(alert1, alert2) or feature_sim > 0.8 

# Discover cross-system correlated events 