from collections import deque

class AdaptivePolicyEngine:
    """Adaptive storage policy engine"""
    
    def __init__(self, cost_analyzer: StorageCostAnalyzer):
        self.cost_analyzer = cost_analyzer
        self.history = deque(maxlen=30)  # 保留30天历史
        
    def optimize_policies(self):
        """Automatically optimize storage policies"""
        current_cost = self.cost_analyzer.calculate_daily_cost()
        self.history.append(current_cost)
        
        # Analyze cost trends
        cost_trend = self._calculate_trend()
        
        # Adjust hot data retention period
        new_hot_days = self._adjust_hot_data_policy(cost_trend)
        lifecycle_manager.policies['hot']['max_age'] = new_hot_days
        
        # Adjust archiving frequency
        new_archive_freq = self._adjust_archive_frequency(cost_trend)
        trace_archiver.archive_frequency = new_archive_freq
        
    def _calculate_trend(self) -> float:
        """Calculate cost change trend"""
        if len(self.history) < 2:
            return 0
        return (self.history[-1]['total'] - self.history[0]['total']) / len(self.history)
    
    def _adjust_hot_data_policy(self, trend: float) -> int:
        """Adjust hot data retention period"""
        current = lifecycle_manager.policies['hot']['max_age']
        if trend > 0.05:  # Cost increase exceeds 5%
            return max(3, current - 1)
        elif trend < -0.02:  # Cost decrease
            return min(14, current + 1)
        return current
    
    def _adjust_archive_frequency(self, trend: float) -> int:
        """Adjust archiving frequency (days)"""
        current = trace_archiver.archive_frequency
        if trend > 0.1:
            return max(7, current - 3)
        elif trend < -0.05:
            return min(30, current + 5)
        return current 