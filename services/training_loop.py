from collections import deque

class CacheTrainer:
    """缓存策略训练流程"""
    
    def __init__(self, cache_system):
        self.cache = cache_system
        self.access_log = deque(maxlen=100000)
        
    def log_access(self, key):
        """记录访问日志用于训练"""
        self.access_log.append(key)
        
    def train_online(self):
        """在线训练方法"""
        for key in self.access_log:
            hit = self.cache.get(key)
            if not hit:
                self.cache.put(key)
            self.cache.agent.replay()
            
    def train_batch(self, batch_size=1000):
        """批量训练方法"""
        sequence = list(self.access_log)[-batch_size:]
        for i in range(len(sequence)-1):
            current = sequence[i]
            next_key = sequence[i+1]
            state = self.cache.agent.get_state(current)
            next_state = self.cache.agent.get_state(next_key)
            reward = 1 if self.cache.get(next_key) else -1
            self.cache.agent.remember(state, 0, reward, next_state)
        self.cache.agent.replay() 