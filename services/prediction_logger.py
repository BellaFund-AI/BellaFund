import json
from datetime import datetime
from uuid import uuid4
from services.sqlite_connection import SQLiteConnection

class PredictionLogger:
    """Logs model predictions with full audit trail
    
    Persists prediction inputs, outputs and context
    for compliance and model monitoring purposes.
    """
    
    def __init__(self):
        self.db = SQLiteConnection('predictions.db')
        self._init_schema()
        
    def log_prediction(self, features: dict, prediction: float, 
                       model_version: str, metadata: dict) -> None:
        """Records complete prediction context
        Args:
            features: Model input features
            prediction: Output score from model
            model_version: Version identifier
            metadata: Additional context (e.g. session ID)
        """
        self.db.execute('''
            INSERT INTO predictions VALUES (
                ?, ?, ?, ?, ?, ?
            )
        ''', (
            str(uuid4()),
            json.dumps(features),
            prediction,
            model_version,
            metadata.get('confidence', 0.0),
            metadata.get('features_hash', ''),
            datetime.now()
        )) 