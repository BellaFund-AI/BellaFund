import zlib
import msgpack
from collections import deque
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import hmac
import hashlib

class TraceCompressor:
    """追踪数据压缩存储引擎"""
    
    def __init__(self, max_memory=1000):
        self.in_memory = deque(maxlen=max_memory)
        self.compressed_data = []
        
    def add_trace(self, trace: dict) -> None:
        """添加追踪数据并自动压缩"""
        # 内存中保留最新数据
        self.in_memory.append(trace)
        
        # 定期压缩旧数据
        if len(self.in_memory) % 100 == 0:
            self._compress_batch()
            
    def _compress_batch(self) -> None:
        """批量压缩数据"""
        batch = list(self.in_memory)[:-100]  # 保留最后100条
        if not batch:
            return
            
        packed = msgpack.packb(batch, use_bin_type=True)
        compressed = zlib.compress(packed)
        self.compressed_data.append(compressed)
        
        # 从内存中移除已压缩数据
        self.in_memory = deque(list(self.in_memory)[-100:], maxlen=1000)
        
    def retrieve_traces(self, hours: int = 24) -> list:
        """检索指定时间范围内的追踪数据"""
        cutoff = datetime.now() - timedelta(hours=hours)
        results = []
        
        # 检查内存中的最新数据
        for trace in reversed(self.in_memory):
            if trace['start_time'] >= cutoff:
                results.append(trace)
            else:
                break
                
        # 解压历史数据
        for compressed in reversed(self.compressed_data):
            batch = msgpack.unpackb(zlib.decompress(compressed), 
                                   raw=False)
            for trace in reversed(batch):
                if trace['start_time'] >= cutoff:
                    results.append(trace)
                else:
                    break
            if batch[0]['start_time'] < cutoff:
                break
                
        return sorted(results, key=lambda x: x['start_time'], reverse=True) 

class SecureTraceCompressor(TraceCompressor):
    """支持加密的追踪存储"""
    
    def __init__(self, encryption_key: str):
        super().__init__()
        self.cipher = Fernet(encryption_key)
        
    def _compress_batch(self) -> None:
        packed = msgpack.packb(batch, use_bin_type=True)
        compressed = zlib.compress(packed)
        encrypted = self.cipher.encrypt(compressed)  # 新增加密步骤
        self.compressed_data.append(encrypted)
        
    def retrieve_traces(self, hours: int = 24) -> list:
        for encrypted in reversed(self.compressed_data):
            compressed = self.cipher.decrypt(encrypted)  # 解密数据
            batch = msgpack.unpackb(zlib.decompress(compressed))
            for trace in reversed(batch):
                if trace['start_time'] >= cutoff:
                    results.append(trace)
                else:
                    break
            if batch[0]['start_time'] < cutoff:
                break
                
        return sorted(results, key=lambda x: x['start_time'], reverse=True) 

class IntegrityCheckedCompressor(SecureTraceCompressor):
    """添加HMAC完整性校验"""
    
    def __init__(self, encryption_key: str, hmac_key: str):
        super().__init__(encryption_key)
        self.hmac_key = hmac_key.encode()
        
    def _compress_batch(self):
        encrypted = super()._compress_batch()
        signature = hmac.new(self.hmac_key, encrypted, hashlib.sha256).digest()
        self.compressed_data.append(signature + encrypted)
        
    def _verify_batch(self, data: bytes) -> bool:
        signature, encrypted = data[:32], data[32:]
        expected = hmac.new(self.hmac_key, encrypted, hashlib.sha256).digest()
        return hmac.compare_digest(signature, expected) 