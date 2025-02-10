"""
Real-time market data processing pipeline
Consumes from Kafka and updates AI models
"""
from kafka import KafkaConsumer
import json

class StreamProcessor:
    def __init__(self, bootstrap_servers):
        self.consumer = KafkaConsumer(
            'market-data',
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
        self.window_size = 100  # Data points per analysis window
        
    def start_processing(self, model):
        """Process real-time data stream"""
        window = []
        for message in self.consumer:
            data = message.value
            window.append(self._extract_features(data))
            
            if len(window) >= self.window_size:
                predictions = model.predict(window)
                self._update_dashboard(predictions)
                window = []

    def _extract_features(self, raw_data):
        """Convert raw market data to model features"""
        return {
            'volatility': raw_data['price_change_24h'],
            'volume': raw_data['total_volume'],
            'social_score': raw_data['social_mentions']
        } 