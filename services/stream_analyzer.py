from collections import deque, Counter

class StreamAnalyzer:
    """实时访问模式分析引擎"""
    
    def __init__(self, window_size=1000):
        self.window = deque(maxlen=window_size)
        self.freq_counter = Counter()
        self.pattern_detector = PatternDetector()
        
    def process(self, access_log: dict):
        """实时处理访问事件"""
        self.window.append(access_log)
        self.freq_counter[access_log['endpoint']] += 1
        
        # 检测突发访问模式
        if len(self.window) > 100:
            current_rate = len(self.window) / 60  # 请求/秒
            if current_rate > 2 * self.avg_rate:
                self.trigger_scaling()
                
        # 更新实时热点
        self.update_hotspots(access_log)
        
    def update_hotspots(self, access: dict):
        """实时更新热点数据"""
        for data_key in access['accessed_data']:
            self.freq_counter[data_key] += 1
            self.pattern_detector.log_access(
                user=access['user'],
                data_key=data_key,
                timestamp=access['timestamp']
            )
            
    def trigger_scaling(self):
        """触发自动扩展"""
        autoscaler.scale(
            metric='request_rate',
            current=len(self.window)/60,
            threshold=100
        ) 