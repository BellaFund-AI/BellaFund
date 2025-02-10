from collections import deque
from datetime import datetime

class AccessPatternAnalyzer:
    """Access pattern analysis engine"""
    
    def __init__(self):
        self.access_log = deque(maxlen=100000)
        self.hotspots = {}
        
    def log_access(self, trace: dict):
        """Log data access patterns"""
        access_info = {
            'timestamp': datetime.now(),
            'trace_id': trace['trace_id'],
            'accessed_data': self._extract_data_refs(trace),
            'user': trace['tags'].get('user', 'anonymous'),
            'endpoint': trace['tags'].get('endpoint')
        }
        self.access_log.append(access_info)
        self._update_hotspots(access_info)
        
    def _extract_data_refs(self, trace: dict) -> list:
        """Extract data references from traces"""
        return [
            span['tags'].get('data_key')
            for span in flatten_trace(trace)
            if 'data_key' in span['tags']
        ]
    
    def _update_hotspots(self, access: dict):
        """Update hotspot statistics"""
        for data_key in access['accessed_data']:
            if data_key not in self.hotspots:
                self.hotspots[data_key] = {
                    'access_count': 0,
                    'last_accessed': datetime.min
                }
            self.hotspots[data_key]['access_count'] += 1
            self.hotspots[data_key]['last_accessed'] = datetime.now()
    
    def get_hot_data(self, top_n=10) -> list:
        """Get data hotspot rankings"""
        return sorted(
            self.hotspots.items(),
            key=lambda x: (-x[1]['access_count'], x[1]['last_accessed']),
        )[:top_n] 