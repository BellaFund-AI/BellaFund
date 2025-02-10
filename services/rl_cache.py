import torch
import torch.nn as nn
from collections import deque, OrderedDict
import random

class QNetwork(nn.Module):
    """深度Q网络结构"""
    def __init__(self, state_size=6, action_size=2):
        super().__init__()
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_size)
        
    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class RLCache:
    """强化学习缓存管理代理"""
    def __init__(self, cache_capacity):
        self.q_net = QNetwork()
        self.target_net = QNetwork()
        self.optimizer = torch.optim.Adam(self.q_net.parameters(), lr=0.001)
        self.memory = deque(maxlen=10000)
        self.cache = OrderedDict()
        self.capacity = cache_capacity
        self.batch_size = 32
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

    def get_state(self, key):
        """Generate current cache state features"""
        return [
            len(self.cache)/self.capacity,
            self.cache.get(key, 0),  # 访问次数
            self._get_recency(key),
            self._get_predictability(key)
        ]

    def choose_action(self, state):
        """Select cache replacement action"""
        if random.random() < self.epsilon:
            return random.choice([0, 1])  # 随机探索
        else:
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state)
                q_values = self.q_net(state_tensor)
                return torch.argmax(q_values).item()

    def remember(self, state, action, reward, next_state):
        """Store experience replay"""
        self.memory.append((state, action, reward, next_state))

    def replay(self):
        """Perform experience replay training"""
        if len(self.memory) < self.batch_size:
            return
            
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states = zip(*batch)
        
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        
        current_q = self.q_net(states).gather(1, actions.unsqueeze(1))
        next_q = self.target_net(next_states).max(1)[0].detach()
        target_q = rewards + self.gamma * next_q
        
        loss = nn.MSELoss()(current_q.squeeze(), target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # 更新探索率
        self.epsilon = max(self.epsilon_min, self.epsilon*self.epsilon_decay)

    def predict_next_access(self):
        # This method is not provided in the original file or the new file
        # It's assumed to exist as it's called in the choose_action method
        pass 