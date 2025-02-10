"""
Tracks feature distributions and importance over time
Identifies concept drift in input patterns
"""
import pandas as pd
from datetime import datetime
import numpy as np

class FeatureMonitor:
    """Monitors feature distributions and concept drift over time
    
    Attributes:
        reference (pd.DataFrame): Baseline feature statistics
        feature_history (list): Record of feature distribution changes
        importance_history (list): Track feature importance evolution
    """
    
    def __init__(self, reference_data):
        self.reference = reference_data
        self.feature_history = []
        self.importance_history = []
        
    def record_features(self, features, importances):
        """Store feature stats and importance scores"""
        self.feature_history.append({
            'timestamp': datetime.now(),
            'means': features.mean().to_dict(),
            'stds': features.std().to_dict()
        })
        self.importance_history.append({
            'timestamp': datetime.now(),
            'importances': importances
        })
        
    def detect_concept_drift(self, window_size=30) -> dict:
        """Detects significant feature distribution shifts
        Args:
            window_size: Days to consider for recent data
        Returns:
            dict: Features with z-score exceeding 3 sigma threshold
        """
        recent = [f for f in self.feature_history 
                if f['timestamp'] > datetime.now() - pd.Timedelta(days=window_size)]
        
        drift_scores = {}
        for feature in self.reference.columns:
            ref_mean = self.reference[feature].mean()
            current_means = [f['means'][feature] for f in recent]
            z_scores = (np.array(current_means) - ref_mean) / self.reference[feature].std()
            drift_scores[feature] = np.max(np.abs(z_scores))
            
        return {k: v for k, v in drift_scores.items() if v > 3}  # 3 sigma threshold 

    def compare_version_drift(self, version1_hash: str, version2_hash: str) -> dict:
        """Compare data drift between two model versions
        Args:
            version1_hash: Training data hash for first version
            version2_hash: Training data hash for second version
        Returns:
            dict: Drift scores for common features
        """
        ref1 = self.get_version_stats(version1_hash)
        ref2 = self.get_version_stats(version2_hash)
        
        common_features = set(ref1.columns) & set(ref2.columns)
        drift_scores = {}
        
        for feature in common_features:
            # Calculate population stability index
            psi = self._calculate_psi(ref1[feature], ref2[feature])
            drift_scores[feature] = {
                'psi': psi,
                'v1_mean': ref1[feature].mean(),
                'v2_mean': ref2[feature].mean()
            }
        
        return drift_scores 