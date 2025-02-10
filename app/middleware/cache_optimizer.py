import time
from fastapi import Request
from app.services.cache_monitor import CacheMonitor
from app.services.cache_trainer import CacheTrainer
from app.utils.cache_utils import generate_cache_key

cache_monitor = CacheMonitor()
cache_trainer = CacheTrainer()

async def cache_optimizer_middleware(request: Request, call_next):
    """缓存策略动态调整中间件"""
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    
    # 记录缓存访问指标
    cache_key = generate_cache_key(request)
    hit = cache.exists(cache_key)
    cache_monitor.log_request(hit, latency)
    
    # 动态调整策略
    if cache_monitor.trigger_alert():
        cache_trainer.train_online()
        cache.switch_policy('aggressive')
        
    return response 