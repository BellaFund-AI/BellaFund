"""
SHAP-based Feature Explanation System
Provides interpretable AI insights for investment decisions
"""
import shap
import pandas as pd
from typing import Dict

class ScoreExplainer:
    def __init__(self, model):
        self.explainer = shap.TreeExplainer(model)
        self.feature_names = [
            'price_volatility', 'trading_volume', 'social_activity',
            'liquidity_depth', 'whale_transactions', 'github_commits'
        ]
        
    def explain_prediction(self, input_data: Dict) -> Dict:
        """Generate feature importance scores for a prediction"""
        input_df = self._prepare_input(input_data)
        shap_values = self.explainer.shap_values(input_df)
        return self._format_explanation(input_df, shap_values[0])
        
    def _prepare_input(self, data: Dict) -> pd.DataFrame:
        """Convert input dict to properly formatted DataFrame"""
        return pd.DataFrame([data])[self.feature_names]
        
    def _format_explanation(self, input_df, shap_values):
        """Create human-readable explanation"""
        return {
            'feature_importances': dict(zip(
                self.feature_names,
                shap_values.tolist()
            )),
            'base_value': float(self.explainer.expected_value),
            'prediction_shift': float(shap_values.sum())
        } 