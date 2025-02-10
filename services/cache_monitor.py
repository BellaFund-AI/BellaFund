from collections import deque
import numpy as np

class CacheMonitor:
    """Real-time cache performance monitoring"""
    
    def __init__(self, cache_system):
        self.cache = cache_system
        self.metrics = {
            'hit_rate': deque(maxlen=1000),
            'latency': deque(maxlen=1000),
            'throughput': deque(maxlen=1000)
        }
        
    def log_request(self, hit: bool, latency: float):
        """Log cache request metrics"""
        self.metrics['hit_rate'].append(1 if hit else 0)
        self.metrics['latency'].append(latency)
        
    def get_realtime_metrics(self) -> dict:
        """Get real-time performance metrics"""
        return {
            'hit_rate': np.mean(self.metrics['hit_rate']) if self.metrics['hit_rate'] else 0,
            'avg_latency': np.mean(self.metrics['latency']) if self.metrics['latency'] else 0,
            'throughput': len(self.metrics['latency']) / 60  # Requests per second
        }
    
    def trigger_alert(self) -> bool:
        """Performance anomaly detection"""
        recent_hits = list(self.metrics['hit_rate'])[-100:]
        if len(recent_hits) < 50:
            return False
        current = np.mean(recent_hits)
        return current < 0.5  # Trigger alert when hit rate below 50% 

    """Real-time performance metrics tracking"""

    """Maximum compression level""" 