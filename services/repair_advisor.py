import joblib
import numpy as np
from datetime import datetime
import pandas as pd

class RepairAdvisor:
    """基于机器学习的修复策略推荐引擎"""
    
    def __init__(self, model_path='models/repair_predictor.pkl'):
        self.model = joblib.load(model_path)
        self.feature_extractor = RepairFeatureExtractor()
        self.version = 1
        self.training_data = pd.DataFrame()
        self.feedback_queue = None
        
    def recommend_strategy(self, data_key: str) -> dict:
        """推荐最优修复策略"""
        features = self.feature_extractor.extract_features(data_key)
        prediction = self.model.predict_proba([features])[0]
        
        return {
            'strategy': self.model.classes_[np.argmax(prediction)],
            'confidence': np.max(prediction),
            'feature_weights': dict(zip(
                self.model.feature_names_in_,
                self.model.coef_[0]
            ))
        }

    def update_model(self, new_data: pd.DataFrame):
        """在线更新模型"""
        # 增量训练
        partial_fit = hasattr(self.model, 'partial_fit')
        if partial_fit:
            X = new_data.drop('strategy', axis=1)
            y = new_data['strategy']
            self.model.partial_fit(X, y)
        else:
            # 全量重新训练
            combined = pd.concat([self.training_data, new_data])
            self.model.fit(combined.drop('strategy', axis=1), combined['strategy'])
        
        # 保存新版本模型
        joblib.dump(self.model, f"models/repair_model_v{self.version}.pkl")
        self.version += 1

    def log_feedback(self, data_key: str, strategy: str, success: bool):
        """记录修复结果反馈"""
        features = self.feature_extractor.extract_features(data_key)
        features['strategy'] = strategy
        features['success'] = success
        self.feedback_queue.put(features)

class RepairFeatureExtractor:
    """修复策略特征工程"""
    
    def extract_features(self, data_key: str) -> dict:
        data_info = data_registry[data_key]
        return {
            'access_frequency': access_stats[data_key]['count'],
            'storage_tier': data_info['tier'],
            'data_size': len(storage_backend.retrieve(data_key)),
            'provider_failure_rate': provider_stats[data_info['uri'].split('://')[0]]['failure_rate'],
            'last_verified': (datetime.now() - data_info['last_verified']).total_seconds(),
            'replica_count': len(cloud_storage.get_replicas(data_key))
        } 