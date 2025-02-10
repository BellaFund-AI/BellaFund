from collections import deque
from datetime import datetime

class TraceAwareRollback:
    """Intelligent model rollback system"""
    
    def __init__(self, stability_threshold=0.95):
        self.stability_score = 1.0
        self.stability_threshold = stability_threshold
        self.performance_history = deque(maxlen=100)
        
    def evaluate_rollback(self, trace: dict) -> bool:
        """Rollback decision based on trace data"""
        # 计算稳定性得分
        error_rate = self._calculate_error_rate(trace)
        latency_ratio = self._calculate_latency_ratio(trace)
        self.stability_score *= (1 - error_rate) * (1 - latency_ratio)
        
        # 记录性能指标
        self.performance_history.append({
            'timestamp': datetime.now(),
            'stability': self.stability_score,
            'error_rate': error_rate,
            'latency': trace['duration']
        })
        
        return self.stability_score < self.stability_threshold

    def _calculate_error_rate(self, trace: dict) -> float:
        """Calculate error rate in traces"""
        error_spans = [s for s in flatten_trace(trace) if 'error' in s.get('tags', {})]
        return len(error_spans) / len(flatten_trace(trace))

    def _calculate_latency_ratio(self, trace: dict) -> float:
        """Calculate latency-to-baseline ratio"""
        baseline = 1.0  # 基准响应时间（秒）
        return min(trace['duration'] / baseline, 1.0)

    def execute_rollback(self):
        """执行回滚操作"""
        stable_version = self._find_stable_version()
        if stable_version:
            ai_scorer.load_model(stable_version)
            self._reset_monitoring()
            return True
        return False

    def _find_stable_version(self) -> str:
        """Find most recent stable model version"""
        versions = ai_scorer.get_version_history()
        for v in reversed(versions):
            if v['stability'] > self.stability_threshold:
                return v['id']
        return None 