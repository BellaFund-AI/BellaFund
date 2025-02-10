"""
Gradual Model Rollout System
Implements canary releases for model deployment
"""
from datetime import datetime
import random

class CanaryDeployer:
    def __init__(self, production_model, candidate_model):
        self.production = production_model
        self.candidate = candidate_model
        self.traffic_split = 0.1  # Initial 10% to candidate
        self.metrics = {
            'production': [],
            'candidate': []
        }
        
    def route_request(self, input_data):
        """Route traffic based on canary percentage"""
        if random.random() < self.traffic_split:
            result = self.candidate.predict(input_data)
            self._log_performance('candidate', result)
            return result
        else:
            result = self.production.predict(input_data)
            self._log_performance('production', result)
            return result
            
    def adjust_traffic(self, success_rate_diff):
        """Adjust traffic split based on performance"""
        if success_rate_diff > 0.05:  # Candidate performs 5% better
            self.traffic_split = min(1.0, self.traffic_split + 0.2)
        elif success_rate_diff < -0.03:  # Candidate underperforms
            self.traffic_split = max(0.0, self.traffic_split - 0.1)
            
    def _log_performance(self, version, prediction_result):
        """Track model performance metrics"""
        self.metrics[version].append({
            'timestamp': datetime.now(),
            'accuracy': prediction_result.get('accuracy', 0),
            'latency': prediction_result.get('latency', 0)
        }) 