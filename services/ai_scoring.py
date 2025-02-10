"""
Enhanced AI Scoring System with Model Versioning
and Prediction Monitoring
"""
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import joblib
from typing import Dict
from datetime import datetime
from services.model_monitor import ModelMonitor
from services.feature_monitor import FeatureMonitor
from services.prediction_logger import PredictionLogger
from services.tracing import tracer
from services.model_sanitizer import InputSanitizer
from services.model_optimizer import ONNXConverter
from services.fallback_model import FallbackModel
from prometheus_client import Histogram
import time

class TokenScorer:
    """Advanced scoring engine with model lifecycle management"""
    
    def __init__(self, model_path: str = None):
        """Initialize scoring system
        Args:
            model_path: Path to serialized model (default: latest)
        """
        self.model_versions = {}
        self.current_version = None
        self.features = [
            'price_volatility', 'trading_volume', 'social_activity',
            'liquidity_depth', 'whale_transactions', 'github_commits'
        ]
        
        if model_path:
            self.load_model(model_path)
        else:
            self.model = RandomForestRegressor(n_estimators=100)
            self.current_version = 'initial'
            self.model_versions[self.current_version] = {
                'model': self.model,
                'created_at': datetime.now()
            }
        self.performance_monitor = ModelMonitor()
        self.fallback_model = FallbackModel()
        self.feature_monitor = FeatureMonitor(
            reference_data=load_reference_stats(),
            drift_threshold=0.15
        )
        self.prediction_logger = PredictionLogger()
        self.alert_manager = None
        self.sanitizer = InputSanitizer()
        self.onnx_model = ONNXConverter.convert(self.model)
        self.prediction_latency = Histogram(
            'scoring_latency_seconds', 
            'Prediction latency distribution'
        )

    def predict_score(self, token_data: Dict) -> Dict:
        """Generate score with enhanced tracing"""
        sanitized = self.sanitizer.sanitize(token_data)
        with tracer.start_span("model_prediction") as span:
            tracer.add_tag("model_version", self.current_version)
            tracer.add_tag("features_hash", self._generate_features_hash(sanitized))
            tracer.add_performance_metrics()  # Add resource metrics recording
            
            try:
                # Record feature distribution
                self.feature_monitor.record_features(
                    pd.DataFrame([sanitized]), 
                    self.current_version
                )
                # Add feature statistics tags
                for feature in self.features:
                    tracer.add_tag(f"feature_{feature}", sanitized.get(feature, None))
                
                # Perform prediction
                start_time = time.time()
                prediction = self.model.predict(
                    pd.DataFrame([sanitized])[self.features]
                )[0]
                latency = time.time() - start_time
                self.prediction_latency.observe(latency)
                
                # Record performance metrics
                tracer.add_tag("prediction_value", prediction)
                self.performance_monitor.log_prediction(
                    features=sanitized,
                    prediction=prediction,
                    model_version=self.current_version
                )
                
                return {
                    "score": round(prediction, 2),
                    "model_version": self.current_version,
                    "trace_id": tracer.current_span['trace_id']  # 返回追踪ID
                }
                
            except Exception as e:
                tracer.add_tag("error", str(e))
                if self.fallback_model:
                    return self.fallback_model.predict_score(sanitized)
                raise

    def load_model(self, model_path: str) -> None:
        """Load new model version with validation"""
        new_model = joblib.load(model_path)
        if not hasattr(new_model, 'predict'):
            raise InvalidModelError("Invalid model object")
            
        version_id = f"v{len(self.model_versions)+1}-{datetime.now().date()}"
        self.model_versions[version_id] = {
            'model': new_model,
            'created_at': datetime.now()
        }
        self._switch_model_version(version_id)

    def _switch_model_version(self, version_id: str) -> None:
        """Activate specific model version"""
        self.model = self.model_versions[version_id]['model']
        self.current_version = version_id
        print(f"Switched to model version: {version_id}")

    def _validate_input_features(self, data: Dict) -> None:
        """Input feature validation"""
        missing = [f for f in self.features if f not in data]
        if missing:
            raise InvalidInputError(f"Missing features: {missing}")
            
        for f, v in data.items():
            if pd.isna(v):
                data[f] = 0  # Auto-handle missing values

    def auto_rollback(self):
        """Intelligent model rollback strategy"""
        if self.performance_monitor.check_for_degradation():
            candidates = self._find_rollback_candidates()
            if candidates:
                self._switch_model_version(candidates[0])
                self._notify_rollback(candidates[0])
                return True
        return False

    def _find_rollback_candidates(self):
        """Find models with better performance than current version"""
        return sorted(
            self.model_versions.items(),
            key=lambda x: (x[1]['performance'], x[1]['created_at']),
            reverse=True
        )[1:]  # Exclude current version

    def _calculate_confidence(self, input_data):
        """Compute prediction confidence using model's probability estimates"""
        return 0.85  # Placeholder value

    def _generate_features_hash(self, features):
        """Generate unique hash for input features"""
        return hash(frozenset(features.items()))

    def compare_versions(self, version1: str, version2: str) -> dict:
        """Compare two model versions across multiple dimensions
        Args:
            version1: Identifier for first model version
            version2: Identifier for second model version
        Returns:
            dict: Contains performance deltas, feature importance changes,
                  and data drift metrics
        """
        # Validate version existence
        self._validate_version(version1)
        self._validate_version(version2)
        
        v1_meta = self.model_versions[version1]
        v2_meta = self.model_versions[version2]
        
        return {
            'performance': self._compare_performance(v1_meta, v2_meta),
            'feature_importance': self._compare_feature_importances(
                v1_meta['feature_importances'],
                v2_meta['feature_importances']
            ),
            'data_drift': self.feature_monitor.compare_versions(
                v1_meta['training_data_hash'],
                v2_meta['training_data_hash']
            )
        }

    def _validate_version(self, version: str) -> None:
        """Ensure version exists in registry"""
        if version not in self.model_versions:
            raise ValueError(f"Unknown model version: {version}")

    def compare_feature_importances(self, version1: str, version2: str) -> dict:
        """Compares feature importance between versions
        Args:
            version1: First model version
            version2: Second model version
        Returns:
            dict: Feature importance differences sorted by magnitude
        """
        v1_importances = self.model_versions[version1]['feature_importances']
        v2_importances = self.model_versions[version2]['feature_importances']
        
        comparison = {
            feature: {
                'v1': v1_importances.get(feature, 0),
                'v2': v2_importances.get(feature, 0),
                'delta': v1_importances.get(feature, 0) - v2_importances.get(feature, 0)
            }
            for feature in set(v1_importances) | set(v2_importances)
        }
        return dict(sorted(
            comparison.items(), 
            key=lambda x: abs(x[1]['delta']), 
            reverse=True
        ))

class PredictionError(Exception):
    """Custom exception for scoring failures"""
    pass

class InvalidModelError(Exception):
    """Raised when loading invalid model file"""
    pass

class InvalidInputError(Exception):
    """Raised for invalid input data"""
    pass 