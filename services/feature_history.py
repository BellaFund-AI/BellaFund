"""
Tracks feature importance evolution across model versions
"""
import pandas as pd
from datetime import datetime

class FeatureHistory:
    def __init__(self):
        self.history = pd.DataFrame(columns=[
            'timestamp', 'model_version', 'feature', 'importance'
        ])
        
    def record_importance(self, version, feature_importances):
        """Store feature importance for model version"""
        timestamp = datetime.now()
        records = [{
            'timestamp': timestamp,
            'model_version': version,
            'feature': feature,
            'importance': importance
        } for feature, importance in feature_importances.items()]
        
        self.history = pd.concat([
            self.history, 
            pd.DataFrame(records)
        ], ignore_index=True)
        
    def get_trend(self, feature, window=30):
        """Get importance trend for specific feature"""
        return self.history[
            (self.history.feature == feature) &
            (self.history.timestamp > pd.Timestamp.now() - pd.DateOffset(days=window))
        ].sort_values('timestamp') 