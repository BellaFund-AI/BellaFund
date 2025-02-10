import threading
import random
from collections import defaultdict

class TracingCollector:
    """Collects and stores tracing spans for analysis"""
    
    def __init__(self):
        self.spans = []
        self.lock = threading.Lock()
        
    def log_span(self, span: dict) -> None:
        """Store span data with thread safety"""
        with self.lock:
            self.spans.append(span)
            
    def query_traces(self, filters: dict = None) -> list:
        """Query stored traces with filters"""
        filtered = self.spans
        if filters:
            if 'service' in filters:
                filtered = [s for s in filtered if s['tags'].get('service') == filters['service']]
            if 'min_duration' in filters:
                filtered = [s for s in filtered if s['duration'] >= filters['min_duration']]
        return filtered
    
    def get_trace_tree(self, trace_id: str) -> dict:
        """Reconstruct full trace hierarchy"""
        spans = [s for s in self.spans if s['trace_id'] == trace_id]
        return self._build_tree(spans)
    
    def _build_tree(self, spans: list) -> dict:
        """Build hierarchical trace structure"""
        root = next((s for s in spans if not s['parent_id']), None)
        if not root:
            return {}
            
        def build_children(parent_id):
            return [{
                **span,
                'children': build_children(f"{span['trace_id']}:{span['span_id']}")
            } for span in spans if span.get('parent_id') == parent_id]
            
        return {**root, 'children': build_children(f"{root['trace_id']}:{root['span_id']}")}
    
    def should_sample(self, span: dict) -> bool:
        """Determine if span should be stored based on sampling rules"""
        # Sample all errors
        if 'error' in span['tags']:
            return True
        # Sample 10% of slow requests
        if span['duration'] > 1.0 and random.random() < 0.1:
            return True
        # Default sample rate
        return random.random() < 0.01 

    def enrich_with_logs(self, trace_id: str):
        """关联追踪数据与系统日志"""
        trace = self.get_trace_tree(trace_id)
        logs = log_repository.query_logs({
            'trace_id': trace_id,
            'timestamp_between': [
                trace['start_time'],
                trace['end_time']
            ]
        })
        return {
            **trace,
            'logs': self.group_logs_by_span(logs)
        }

    def group_logs_by_span(self, logs: list) -> dict:
        """按Span组织日志"""
        span_logs = defaultdict(list)
        for log in logs:
            span_logs[log['span_id']].append(log)
        return span_logs 