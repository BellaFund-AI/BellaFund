class AutoRemediator:
    def analyze_and_fix(self, trace: dict):
        """根据追踪数据执行自动修复"""
        # 识别数据库慢查询
        slow_db = next((s for s in flatten_trace(trace) 
                      if s['name'] == 'db_query' and s['duration'] > 1.0), None)
        if slow_db:
            self.optimize_query(slow_db['tags']['query'])
            
        # 检测重试循环
        retry_pattern = self.detect_retry_loop(trace)
        if retry_pattern:
            self.circuit_breaker.enable(retry_pattern['service'])
            
    def detect_retry_loop(self, trace: dict) -> dict:
        """识别异常重试模式"""
        service_calls = Counter()
        for span in flatten_trace(trace):
            if span['name'].startswith('service_call:'):
                service_calls[span['tags']['service']] += 1
                
        for service, count in service_calls.items():
            if count > self.config['max_retries']:
                return {
                    'service': service,
                    'call_count': count
                }
        return None 