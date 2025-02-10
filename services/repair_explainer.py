class RepairExplainer:
    """修复策略可解释性引擎"""
    
    def explain(self, data_key: str) -> dict:
        features = self.feature_extractor.extract_features(data_key)
        explanation = {
            "feature_contributions": self._calculate_feature_importance(features),
            "similar_cases": self._find_similar_historical_cases(data_key),
            "strategy_effectiveness": self._get_strategy_stats()
        }
        return explanation

    def _calculate_feature_importance(self, features: dict) -> list:
        shap_values = self.shap_explainer.shap_values([features])
        return sorted(zip(self.model.feature_names_in_, shap_values[0]), 
                     key=lambda x: -abs(x[1])) 