class TraceAnalyzer:
    def detect_anomalies(self, trace: dict) -> list:
        """自动检测追踪中的异常模式"""
        anomalies = []
        
        # 检测超长span
        if trace['duration'] > self.config['max_trace_duration']:
            anomalies.append({
                'type': 'long_trace',
                'threshold': self.config['max_trace_duration'],
                'actual': trace['duration']
            })
            
        # 检测错误级联
        error_spans = [s for s in flatten_trace(trace) if 'error' in s.get('tags', {})]
        if len(error_spans) > 3:
            anomalies.append({
                'type': 'error_cascade',
                'count': len(error_spans)
            })
            
        return anomalies 