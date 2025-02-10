import zlib
from fastapi import Request

async def storage_optimizer_middleware(request: Request, call_next):
    """Automatic storage optimization middleware"""
    response = await call_next(request)
    
    if request.url.path == "/tracing/traces":
        # 压缩响应数据
        if len(response.body) > 1024:
            compressed = zlib.compress(response.body, level=9)  # 最高压缩级别
            response.headers["Content-Encoding"] = "deflate"
            response.headers["X-Compression-Ratio"] = f"{len(response.body)/len(compressed):.1f}x"
            response.body = compressed
            
    return response 