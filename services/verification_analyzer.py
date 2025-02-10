from collections import deque, defaultdict
from datetime import datetime
from prometheus_client import Gauge, Counter

class VerificationAnalyzer:
    """验证结果模式分析"""
    
    def __init__(self):
        self.history = deque(maxlen=1000)
        self.patterns = defaultdict(int)
        self.metrics = {
            'success_gauge': Gauge('verification_success_rate', 'Data verification success rate'),
            'failure_counter': Counter('verification_failures', 'Total verification failures')
        }
        
    def log_result(self, data_key: str, result: dict):
        """记录验证结果"""
        entry = {
            'timestamp': datetime.now(),
            'data_key': data_key,
            **result
        }
        self.history.append(entry)
        self._detect_patterns(entry)
        
    def _detect_patterns(self, entry: dict):
        """检测异常模式"""
        if entry['status'] == 'failed':
            self.patterns['verification_failure'] += 1
            self.metrics['failure_counter'].inc()
        elif not entry.get('consistent', True):
            provider = data_registry[entry['data_key']]['uri'].split('://')[0]
            self.patterns[f'provider_{provider}_inconsistency'] += 1
            self.metrics['failure_counter'].inc()
            
    def generate_report(self) -> dict:
        """生成验证分析报告"""
        return {
            'total_checks': len(self.history),
            'success_rate': sum(1 for e in self.history 
                               if e['status'] == 'completed' 
                               and e['consistent']) / len(self.history),
            'common_issues': sorted(self.patterns.items(), 
                                  key=lambda x: -x[1])[:5]
        } 