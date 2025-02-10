import pandas as pd
from datetime import datetime
from performance_tracker import performance_tracker

class ResourceMonitor:
    """Monitors system resource utilization and prediction metrics"""
    
    def __init__(self):
        self.metrics_history = pd.DataFrame(columns=[
            'timestamp', 'cpu_usage', 'memory_usage',
            'request_rate', 'latency_p50', 'latency_p95'
        ])
        
    def collect_metrics(self) -> dict:
        """Collect current system metrics"""
        return {
            'timestamp': datetime.now(),
            'cpu_usage': self._get_cpu_usage(),
            'memory_usage': self._get_memory_usage(),
            'request_rate': self._get_request_rate(),
            'latency_p50': performance_tracker.analyze_latency()['percentiles']['p50'],
            'latency_p95': performance_tracker.analyze_latency()['percentiles']['p95']
        }
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU utilization percentage"""
        # Implementation using psutil
        return 65.0  # Placeholder
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage percentage"""
        # Implementation using psutil
        return 45.0  # Placeholder
    
    def _get_request_rate(self) -> float:
        """Calculate requests per second"""
        recent = performance_tracker.get_metrics(window=pd.Timedelta(minutes=1))
        return len(recent) / 60  # Requests per second 