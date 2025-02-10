from datetime import datetime, timedelta
from collections import deque

class LifecyclePolicy:
    """数据生命周期策略引擎"""
    
    def __init__(self):
        self.policies = {
            'hot': {'max_age': 7, 'storage_class': 'memory'},
            'warm': {'max_age': 30, 'storage_class': 'compressed'},
            'cold': {'max_age': 365, 'storage_class': 'archived'}
        }
        
    def apply_policies(self):
        """应用存储策略"""
        now = datetime.now()
        
        # 处理热数据
        hot_data = [t for t in trace_compressor.in_memory 
                   if (now - t['start_time']).days <= 7]
        trace_compressor.in_memory = deque(hot_data, maxlen=1000)
        
        # 处理温数据
        warm_cutoff = now - timedelta(days=30)
        trace_compressor._compress_batch(force=True)
        
        # 处理冷数据
        if trace_archiver:
            trace_archiver.archive_old_traces(days=30) 