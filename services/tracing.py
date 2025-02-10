import uuid
from datetime import datetime
from collections import Counter
import psutil
import threading

class TraceContext:
    """Manages distributed tracing context across services"""
    
    def __init__(self):
        self.current_span = None
        
    def start_span(self, name: str, parent_id: str = None) -> dict:
        """Initialize new tracing span
        Args:
            name: Operation name
            parent_id: Parent span identifier
        Returns:
            dict: Span context with trace/span IDs
        """
        span_id = str(uuid.uuid4())
        self.current_span = {
            'trace_id': parent_id.split(':')[0] if parent_id else str(uuid.uuid4()),
            'span_id': span_id,
            'parent_id': parent_id,
            'name': name,
            'start_time': datetime.now(),
            'tags': {}
        }
        return self.current_span
    
    def add_tag(self, key: str, value: str) -> None:
        """Attach metadata to current span"""
        if self.current_span:
            self.current_span['tags'][key] = value
            
    def end_span(self) -> dict:
        """Finalize current span"""
        if self.current_span:
            self.current_span['end_time'] = datetime.now()
            self.current_span['duration'] = (
                self.current_span['end_time'] - self.current_span['start_time']
            ).total_seconds()
            return self.current_span
        return None 

    def add_performance_metrics(self):
        """记录资源使用指标"""
        if self.current_span:
            self.current_span['metrics'] = {
                'memory_usage': psutil.virtual_memory().percent,
                'cpu_usage': psutil.cpu_percent(),
                'thread_count': threading.active_count(),
                'open_files': len(psutil.Process().open_files())
            }

def analyze_trace_performance(trace: dict) -> dict:
    """Identify performance bottlenecks in trace"""
    slowest_span = max(trace['children'], key=lambda x: x['duration'])
    return {
        "total_duration": trace['duration'],
        "slowest_operation": slowest_span['name'],
        "slowest_duration": slowest_span['duration'],
        "service_breakdown": Counter(
            span['tags'].get('service', 'unknown') 
            for span in flatten_trace(trace)
        )
    } 