import pandas as pd
from datetime import datetime

class PerformanceTracker:
    """Tracks and analyzes model performance metrics over time"""
    
    def __init__(self):
        self.history = pd.DataFrame(columns=[
            'timestamp', 'version', 'accuracy', 
            'precision', 'recall', 'f1', 'roc_auc',
            'inference_latency', 'throughput'
        ])
        self.baselines = {
            'accuracy': 0.85,
            'precision': 0.8,
            'recall': 0.75,
            'roc_auc': 0.9
        }
        
    def log_performance(self, version: str, metrics: dict) -> None:
        """Records comprehensive performance metrics
        Args:
            version: Model version identifier
            metrics: Dictionary containing:
                - accuracy: Classification accuracy
                - precision: Precision score
                - recall: Recall score  
                - f1: F1 score
                - roc_auc: AUC-ROC score
                - inference_latency: Average prediction time (ms)
                - throughput: Predictions per second
        """
        new_entry = {
            'timestamp': datetime.now(),
            'version': version,
            **{k: metrics.get(k, None) for k in self.history.columns[2:]}
        }
        self.history = pd.concat([self.history, pd.DataFrame([new_entry])], ignore_index=True)
        
    def get_metrics(self, version: str = None, window: pd.Timedelta = pd.Timedelta(days=30)) -> pd.DataFrame:
        """Retrieves metrics with filtering options
        Args:
            version: Specific model version to filter
            window: Time window for historical data
        Returns:
            Filtered DataFrame of performance metrics
        """
        cutoff = pd.Timestamp.now() - window
        query = self.history[self.history.timestamp >= cutoff]
        
        if version:
            query = query[query.version == version]
            
        return query.sort_values('timestamp')
    
    def calculate_statistics(self, version: str) -> dict:
        """Computes summary statistics for model version"""
        df = self.get_metrics(version)
        return {
            'mean_accuracy': df.accuracy.mean(),
            'max_precision': df.precision.max(),
            'min_recall': df.recall.min(),
            'std_f1': df.f1.std()
        }

    def detect_anomalies(self, version: str) -> dict:
        """Detects performance anomalies using statistical process control"""
        df = self.get_metrics(version)
        anomalies = {}
        
        for metric in ['accuracy', 'precision', 'recall']:
            if df.empty or metric not in df:
                continue
            
            # Calculate control limits
            mean = df[metric].mean()
            std = df[metric].std()
            upper_limit = mean + 3*std
            lower_limit = mean - 3*std
            
            # Check latest value
            latest = df[metric].iloc[-1]
            if latest < lower_limit or latest > upper_limit:
                anomalies[metric] = {
                    'current': latest,
                    'mean': mean,
                    'std': std,
                    'threshold': 3
                }
            
        return anomalies 

    def auto_adjust_baselines(self, window=pd.Timedelta(days=7)):
        """Automatically adjust performance baselines based on recent data"""
        recent = self.get_metrics(window=window)
        self.baselines = {
            'accuracy': recent.accuracy.quantile(0.9),
            'precision': recent.precision.quantile(0.9),
            'recall': recent.recall.quantile(0.9),
            'roc_auc': recent.roc_auc.quantile(0.9)
        } 

    def track_latency(self, version: str, request_size: int, latency: float):
        """Track prediction latency with request size context"""
        self.history = self.history.append({
            'timestamp': datetime.now(),
            'version': version,
            'request_size': request_size,
            'latency': latency,
            'throughput': request_size / latency if latency > 0 else 0
        }, ignore_index=True)
        
    def analyze_latency(self, version: str) -> dict:
        """Perform latency breakdown analysis"""
        df = self.get_metrics(version)
        return {
            'percentiles': {
                'p50': df.latency.quantile(0.5),
                'p95': df.latency.quantile(0.95),
                'p99': df.latency.quantile(0.99)
            },
            'size_correlation': df[['request_size', 'latency']].corr().iloc[0,1]
        } 