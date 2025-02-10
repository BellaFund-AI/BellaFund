"""
Enhanced Model Performance Monitoring
Tracks prediction accuracy and data drift over time
"""
from datetime import datetime, timedelta
import numpy as np
from sklearn.metrics import mean_absolute_error

class ModelMonitor:
    def __init__(self, reference_data, window_size=7):
        self.reference = reference_data
        self.performance_log = []
        self.window_size = window_size  # Days
        
    def log_performance(self, y_true, y_pred, features):
        """Record model predictions and actual outcomes"""
        entry = {
            'timestamp': datetime.now(),
            'mae': mean_absolute_error(y_true, y_pred),
            'feature_drift': self._calculate_feature_drift(features),
            'sample_size': len(y_true)
        }
        self.performance_log.append(entry)
        
    def check_for_degradation(self):
        """Detect performance degradation in recent window"""
        recent = [log for log in self.performance_log 
                 if log['timestamp'] > datetime.now() - timedelta(days=self.window_size)]
        
        if len(recent) < 5:  # Minimum data points
            return False
            
        current_mae = np.mean([log['mae'] for log in recent[-3:]])
        baseline_mae = np.mean([log['mae'] for log in self.performance_log[:30]])
        
        return current_mae > baseline_mae * 1.15  # 15% performance drop

    def _calculate_feature_drift(self, current_features):
        """Compute KL divergence between current and reference features"""
        # Simplified implementation
        ref_means = self.reference.mean()
        curr_means = current_features.mean()
        return np.sum((curr_means - ref_means)**2) 