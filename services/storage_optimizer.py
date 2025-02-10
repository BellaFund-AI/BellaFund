from collections import defaultdict
from datetime import datetime

class StorageOptimizer:
    """Access pattern-based storage optimization"""
    
    def __init__(self, access_analyzer: AccessPatternAnalyzer):
        self.analyzer = access_analyzer
        self.cache = LRUCache(capacity=1000)
        
    def optimize_placement(self):
        """Optimize data storage location"""
        hot_data = self.analyzer.get_hot_data()
        
        # Move hot data to cache
        for data_key, _ in hot_data:
            if data_key in trace_compressor.compressed_data:
                self._promote_to_cache(data_key)
                
        # Evict cold data from cache
        for data_key in list(self.cache.keys()):
            if data_key not in [d[0] for d in hot_data]:
                self._demote_from_cache(data_key)
    
    def _promote_to_cache(self, data_key: str):
        """Promote data to cache"""
        if data_key in self.cache:
            return
        # Load data from compressed storage
        data = trace_compressor.retrieve_data(data_key)
        self.cache.put(data_key, data)
        trace_compressor.remove_data(data_key)
    
    def _demote_from_cache(self, data_key: str):
        """Evict data from cache"""
        data = self.cache.get(data_key)
        if data:
            trace_compressor.add_data(data_key, data)
            self.cache.remove(data_key)

class StorageTierOptimizer:
    """Cost-based storage tier optimization"""
    
    def __init__(self, cloud_storage: MultiCloudStorage):
        self.cloud = cloud_storage
        self.access_stats = defaultdict(lambda: {'access_count': 0, 'last_accessed': 0})
        
    def optimize_tier_placement(self):
        """Optimize data storage tier"""
        for data_key in list(data_registry.keys()):
            stats = self.access_stats[data_key]
            current_tier = data_registry[data_key]['tier']
            
            # Reclassify based on access patterns
            target_tier = self._classify_data(stats)
            if target_tier != current_tier:
                self._migrate_data(data_key, current_tier, target_tier)
                
    def _classify_data(self, stats: dict) -> str:
        """Classify storage tier based on access patterns"""
        if stats['access_count'] > 1000:
            return 'hot'
        elif stats['access_count'] > 100:
            return 'warm'
        else:
            return 'cold'
            
    def _migrate_data(self, data_key: str, from_tier: str, to_tier: str):
        """Execute data migration"""
        data = storage_backend.retrieve(data_key)
        new_uri = self.cloud.store(data, to_tier)
        data_registry[data_key] = {
            'uri': new_uri,
            'tier': to_tier,
            'migrated_at': datetime.now()
        }
        storage_backend.delete(data_key) 