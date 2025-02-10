import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class DataConsistencyVerifier:
    """Cross-cloud data consistency verifier"""
    
    def __init__(self, cloud_storage: MultiCloudStorage):
        self.cloud = cloud_storage
        self.checksum_cache = {}
        
    def verify_integrity(self, data_key: str) -> bool:
        """Verify data integrity and consistency"""
        stored_uri = data_registry[data_key]['uri']
        provider_name, object_id = stored_uri.split('://')
        primary_data = self._fetch_data(provider_name, object_id)
        
        # Get replica hashes
        replica_hashes = self._get_replica_hashes(data_key)
        current_hash = self._calculate_hash(primary_data)
        
        # Verify all replica consistency
        return all(h == current_hash for h in replica_hashes.values())
    
    def _fetch_data(self, provider: str, object_id: str) -> bytes:
        """Retrieve data from specified provider"""
        provider = next(p for p in self.cloud.providers if p.name == provider)
        return provider.retrieve(object_id)
    
    def _get_replica_hashes(self, data_key: str) -> dict:
        """Get all replica hashes"""
        return {
            p.name: p.get_object_hash(data_registry[data_key]['uri'])
            for p in self.cloud.active_providers
            if p.supports_replica()
        }
    
    def _calculate_hash(self, data: bytes) -> str:
        """Use more secure hashing algorithm"""
        # Use more secure hashing algorithm
        digest = hashes.Hash(hashes.SHA3_256(), backend=default_backend())
        digest.update(data)
        return digest.finalize().hex()

    def _quarantine_data(self, data_key: str):
        """Quarantine inconsistent data"""
        # Mark data as suspicious
        data_registry[data_key]['status'] = 'quarantined'
        # Disable related cache
        cache_system.disable_data(data_key)
        # Trigger data repair process
        self._initiate_repair(data_key)

    def _initiate_repair(self, data_key: str):
        """Initiate data repair process"""
        primary_uri = data_registry[data_key]['uri']
        correct_data = self._fetch_consensus_data(data_key)
        
        # Update all replicas
        for provider in self.cloud.active_providers:
            if provider.supports_replica():
                provider.store(correct_data, data_registry[data_key]['tier'])
        
        # Restore data status
        data_registry[data_key]['status'] = 'active'
        cache_system.enable_data(data_key) 