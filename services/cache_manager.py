class ARCCache:
    """自适应缓存替换算法（ARC）实现"""
    
    def __init__(self, capacity):
        self.t1 = OrderedDict()  # 最近访问
        self.t2 = OrderedDict()  # 频繁访问
        self.b1 = OrderedDict()  # 淘汰历史T1
        self.b2 = OrderedDict()  # 淘汰历史T2
        self.p = 0  # 目标T1大小
        self.capacity = capacity
        
    def get(self, key):
        if key in self.t1:
            del self.t1[key]
            self.t2[key] = True
            return True
        if key in self.t2:
            self.t2.move_to_end(key)
            return True
        return False
    
    def put(self, key):
        if self.get(key):
            return
            
        if len(self.t1) + len(self.b1) >= self.capacity:
            if len(self.t1) < self.capacity:
                self.b1.popitem(last=False)
                self._replace()
            else:
                self.t1.popitem(last=False)
                
        self.t1[key] = True
        
    def _replace(self):
        if len(self.t1) > 0 and (
            (len(self.t1) > self.p) or 
            (len(self.t1) == self.p and len(self.b2) > len(self.b1))
        ):
            self.b1[self.t1.popitem(last=False)[0]] = True
        else:
            self.b2[self.t2.popitem(last=False)[0]] = True 

class RLEnhancedCache:
    """集成强化学习的智能缓存系统"""
    def __init__(self, capacity):
        self.agent = RLCacheAgent(capacity)
        self.cache = OrderedDict()
        self.capacity = capacity
        
    def get(self, key):
        """带强化学习的缓存访问"""
        # 记录访问模式
        prev_state = self.agent.get_state(key)
        hit = key in self.cache
        
        # 更新强化学习状态
        reward = 1 if hit else -1
        next_state = self.agent.get_state(key)
        self.agent.remember(prev_state, 0, reward, next_state)
        self.agent.replay()
        
        if hit:
            self.cache.move_to_end(key)
            return True
        return False

    def put(self, key):
        """带强化学习的缓存存储"""
        if len(self.cache) >= self.capacity:
            state = self.agent.get_state(key)
            action = self.agent.choose_action(state)
            
            if action == 1:  # 替换决策
                self.cache.popitem(last=False)
        self.cache[key] = True
        self.cache.move_to_end(key) 