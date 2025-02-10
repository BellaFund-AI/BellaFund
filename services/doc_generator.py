import json

class ModelDocGenerator:
    """Generates model documentation from version metadata
    
    Uses template-based approach to create standardized
    model cards for reproducibility and auditing.
    """
    
    TEMPLATE = """## Model Version {version}
    **Training Dataset**: {dataset_name}
    **Validation Strategy**: {validation_strategy}
    **Primary Metrics**:
    - ROC AUC: {roc_auc:.3f}
    - F1 Score: {f1:.3f}
    - Precision@K: {precision_at_k:.3f}
    """
    
    def generate_report(self, version: str) -> str:
        """Produces markdown format model card
        Args:
            version: Model version identifier
        Returns:
            str: Formatted documentation in markdown
        """
        metadata = model_repo.get_version_metadata(version)
        return self.TEMPLATE.format(
            version=version,
            dataset_name=metadata['data_stats']['dataset_name'],
            validation_strategy=metadata['data_stats']['validation_strategy'],
            roc_auc=metadata['performance']['roc_auc'],
            f1=metadata['performance']['f1'],
            precision_at_k=metadata['performance']['precision_at_k']
        ) 