"""
Multi-source price feed with anomaly detection
"""
import requests
import numpy as np

class OracleAggregator:
    SOURCES = {
        'binance': 'https://api.binance.com/api/v3/ticker/price',
        'coinbase': 'https://api.pro.coinbase.com/products/{}/ticker',
        'chainlink': lambda sym: f'http://chainlink-node:8080/price/{}'
    }

    def __init__(self, symbol):
        self.symbol = symbol
        self.price_history = []
        
    def get_robust_price(self):
        """Get validated median price"""
        prices = []
        for source, url in self.SOURCES.items():
            try:
                if callable(url):
                    url = url(self.symbol)
                response = requests.get(url).json()
                prices.append(self._parse_response(source, response))
            except Exception as e:
                print(f"Error from {source}: {str(e)}")
        
        self._validate_prices(prices)
        return np.median(prices)

    def _parse_response(self, source, data):
        """Parse exchange-specific response formats"""
        if source == 'binance':
            return float(data['price'])
        elif source == 'coinbase':
            return float(data['price'])
        # ... other parsers

    def _validate_prices(self, prices):
        """Detect price anomalies using IQR method"""
        q1 = np.percentile(prices, 25)
        q3 = np.percentile(prices, 75)
        iqr = q3 - q1
        filtered = [p for p in prices if q1 - 1.5*iqr <= p <= q3 + 1.5*iqr]
        return filtered 