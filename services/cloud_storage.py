from collections import defaultdict

class MultiCloudStorage:
    """Multi-cloud storage abstraction layer"""
    
    def __init__(self, providers: list):
        self.providers = providers
        self.active_providers = providers.copy()
        self.failover_threshold = 3
        self.failure_counts = defaultdict(int)
        
    def store(self, data: bytes, tier: str) -> str:
        """Intelligently select storage provider"""
        provider = self._select_provider(tier)
        try:
            object_id = provider.store(data, tier)
            return f"{provider.name}://{object_id}"
        except StorageError as e:
            self._handle_failure(provider)
            return self.store(data, tier)  # Retry
            
    def _select_provider(self, tier: str) -> StorageProvider:
        """Select optimal provider based on storage tier"""
        candidates = [p for p in self.active_providers 
                      if tier in p.supported_tiers]
        return min(candidates, key=lambda x: x.get_cost(tier))
        
    def _handle_failure(self, provider: StorageProvider):
        """Handle storage failures"""
        self.failure_counts[provider.name] += 1
        if self.failure_counts[provider.name] >= self.failover_threshold:
            self.active_providers = [p for p in self.active_providers
                                    if p != provider]
            alert_manager.trigger_alert({
                "type": "storage_failover",
                "provider": provider.name
            }) 