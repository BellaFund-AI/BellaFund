class StorageCostAnalyzer:
    """存储成本分析引擎"""
    
    def __init__(self):
        self.price_rates = {
            'memory': 0.10,    # 每GB/天
            'compressed': 0.03,
            'archived': 0.01
        }
        
    def calculate_daily_cost(self) -> dict:
        """Calculate daily storage costs"""
        memory_size = sum(
            len(msgpack.packb(t)) for t in trace_compressor.in_memory
        ) / 1024**3  # GB
        
        compressed_size = sum(
            len(b) for b in trace_compressor.compressed_data
        ) / 1024**3
        
        archived_size = trace_archiver.get_archived_size() / 1024**3
        
        return {
            'memory': memory_size * self.price_rates['memory'],
            'compressed': compressed_size * self.price_rates['compressed'],
            'archived': archived_size * self.price_rates['archived'],
            'total': (memory_size * self.price_rates['memory'] +
                     compressed_size * self.price_rates['compressed'] +
                     archived_size * self.price_rates['archived'])
        } 

class AnomalyDetector:
    """Storage cost anomaly detection"""
    
    def __init__(self, threshold=3.0):
        self.threshold = threshold  # Standard deviation multiplier
        self.history = []
        
    def check_anomaly(self, current_cost: float) -> bool:
        """Detect cost anomalies"""
        if len(self.history) < 10:
            self.history.append(current_cost)
            return False
            
        mean = np.mean(self.history)
        std = np.std(self.history)
        
        # 更新历史数据
        self.history.pop(0)
        self.history.append(current_cost)
        
        return abs(current_cost - mean) > self.threshold * std 

         """Predict future cost trends""" 