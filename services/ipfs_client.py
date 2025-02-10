"""
IPFS integration for storing rating certificates
and model metadata in decentralized storage
"""
import ipfshttpclient
import json

class IPFSClient:
    def __init__(self, host='ipfs.infura.io', port=5001):
        self.client = ipfshttpclient.connect(f'/dns/{host}/tcp/{port}/https')
        
    def store_rating_proof(self, score_data: dict) -> str:
        """Store immutable rating record on IPFS"""
        serialized = json.dumps(score_data).encode('utf-8')
        result = self.client.add_bytes(serialized)
        return result
        
    def retrieve_rating_proof(self, cid: str) -> dict:
        """Fetch rating data from IPFS"""
        data = self.client.cat(cid)
        return json.loads(data.decode('utf-8'))
        
    def store_model_weights(self, model_path: str) -> str:
        """Store AI model parameters on IPFS"""
        return self.client.add(model_path)['Hash'] 