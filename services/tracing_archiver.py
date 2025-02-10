import boto3
import zlib
import msgpack
from datetime import datetime, timedelta

class TraceArchiver:
    """追踪数据归档系统"""
    
    def __init__(self, s3_bucket='tracing-archive'):
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket
        
    def archive_old_traces(self, days: int = 30):
        """添加加密归档"""
        cutoff = datetime.now() - timedelta(days=days)
        traces = trace_compressor.retrieve_traces(hours=24*days)
        to_archive = [t for t in traces if t['start_time'] < cutoff]
        
        if to_archive:
            key = f"encrypted-traces-{datetime.now().date()}.bin"
            data = encrypt_data(zlib.compress(msgpack.packb(to_archive)))  # 使用KMS加密
            self.s3.put_object(
                Bucket=self.bucket,
                Body=data,
                SSE='aws:kms',
                Metadata={'encryption-key': key_id}
            )
            
            # 从本地存储移除已归档数据
            trace_compressor.purge_before(cutoff) 