"""
Blockchain transaction analysis module
Monitors on-chain activities and whale movements
"""
from web3 import Web3
import datetime

class ChainAnalyzer:
    def __init__(self, chain_type: str, node_url=None):
        """Initialize analyzer for different blockchain types
        Args:
            chain_type: 'solana' or 'bnb'
            node_url: Required for BNB Chain, optional for Solana
        """
        self.chain_type = chain_type
        if chain_type == 'bnb':
            self.w3 = Web3(Web3.HTTPProvider(node_url))
        elif chain_type == 'solana':
            from solana.rpc.api import Client
            self.client = Client(node_url) if node_url else Client()
        else:
            raise ValueError("Unsupported chain type")

    def validate_address(self, address: str) -> bool:
        """Verify address format validity based on chain type"""
        if self.chain_type == 'bnb':
            return Web3.is_address(address)
        elif self.chain_type == 'solana':
            return len(address) == 44 and address.isalnum()
        return False

    def detect_whale_activity(self, token_address: str, threshold=100000):
        """Unified interface for whale detection"""
        if not self.validate_address(token_address):
            raise ValueError("Invalid address for selected chain")
            
        if self.chain_type == 'bnb':
            return self._bnb_whale_detection(token_address, threshold)
        elif self.chain_type == 'solana':
            return self._solana_whale_detection(token_address, threshold)

    def _bnb_whale_detection(self, token_address, threshold):
        """BNB Chain (EVM compatible) implementation"""
        contract = self.load_erc20_contract(token_address)
        transfer_events = contract.events.Transfer.createFilter(fromBlock='latest')
        
        whale_txs = []
        for event in transfer_events.get_new_entries():
            value = event['args']['value'] / 10**18  # BEP-20 uses 18 decimals
            if value > threshold:
                whale_txs.append({
                    'chain': 'bnb',
                    'from': event['args']['from'],
                    'value': value,
                    'token': token_address,
                    'timestamp': datetime.datetime.now()
                })
        return whale_txs

    def _solana_whale_detection(self, token_address, threshold):
        """Detect large transactions on Solana network
        Implementation for SPL token standard with simplified parsing
        """
        from solana.rpc.types import TokenAccountOpts
        recent_txs = self.client.get_signatures_for_address(token_address)['result']
        
        whale_txs = []
        for tx in recent_txs:
            tx_detail = self.client.get_transaction(tx['signature'])['result']
            # Parse SPL token transfers (simplified example)
            transfers = self._parse_spl_transfers(tx_detail)
            for transfer in transfers:
                if transfer['amount'] > threshold:
                    whale_txs.append({
                        'chain': 'solana',
                        'from': transfer['source'],
                        'value': transfer['amount'],
                        'token': token_address,
                        'timestamp': datetime.datetime.fromtimestamp(tx['blockTime'])
                    })
        return whale_txs 