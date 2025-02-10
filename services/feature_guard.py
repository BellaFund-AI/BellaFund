class FeatureGuard:
    """基于追踪数据的特征异常检测"""
    
    def __init__(self, window_size=1000):
        self.feature_stats = defaultdict(lambda: {
            'mean': 0,
            'std': 1,
            'min': 0,
            'max': 0,
            'count': 0
        })
        self.window_size = window_size
        
    def update_stats(self, trace: dict):
        """从追踪数据更新特征统计"""
        for key in trace['tags']:
            if key.startswith('feature_'):
                feature = key[8:]
                value = float(trace['tags'][key])
                self._update_feature(feature, value)
                
    def _update_feature(self, feature: str, value: float):
        """使用Welford算法在线更新统计量"""
        stats = self.feature_stats[feature]
        stats['count'] += 1
        
        if stats['count'] > self.window_size:
            # 维持滑动窗口
            stats['count'] = self.window_size
            delta = (value - stats['mean']) / self.window_size
        else:
            delta = (value - stats['mean']) / stats['count']
            
        new_mean = stats['mean'] + delta
        new_std = stats['std'] + (value - stats['mean']) * (value - new_mean)
        
        stats['mean'] = new_mean
        stats['std'] = new_std / max(stats['count'], 1)
        stats['min'] = min(value, stats['min'])
        stats['max'] = max(value, stats['max'])

    def detect_anomalies(self, trace: dict) -> dict:
        """检测特征异常"""
        anomalies = {}
        for key in trace['tags']:
            if key.startswith('feature_'):
                feature = key[8:]
                value = float(trace['tags'][key])
                z_score = (value - self.feature_stats[feature]['mean']) / self.feature_stats[feature]['std']
                if abs(z_score) > 3:
                    anomalies[feature] = {
                        'value': value,
                        'mean': self.feature_stats[feature]['mean'],
                        'z_score': z_score
                    }
        return anomalies 