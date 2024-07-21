import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
import math
from ai.ai_model import DQN
from ai.ai_utils import ReplayMemory
from collections import namedtuple, deque

class DQNAgent:
    def __init__(self, state_dim, action_dim, memory_capacity=10000, batch_size=64, gamma=0.99, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=500):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.memory = ReplayMemory(memory_capacity)
        self.batch_size = batch_size
        self.gamma = gamma
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.epsilon = epsilon_start
        self.steps_done = 0

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policy_net = DQN(state_dim, action_dim).to(self.device)
        self.target_net = DQN(state_dim, action_dim).to(self.device)
        self.optimizer = optim.Adam(self.policy_net.parameters())

    def select_action(self, state):
        self.steps_done += 1
        self.epsilon = self.epsilon_end + (self.epsilon_start - self.epsilon_end) * \
                       math.exp(-1. * self.steps_done / self.epsilon_decay)

        if random.random() > self.epsilon:
            with torch.no_grad():
                state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
                return self.policy_net(state).max(1)[1].item()
        else:
            return random.randrange(self.policy_net.fc3.out_features)

    def push_memory(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)

    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return
        transitions = self.memory.sample(self.batch_size)
        batch_state, batch_action, batch_reward, batch_next_state, batch_done = zip(*transitions)

        batch_state = torch.tensor(np.array(batch_state), dtype=torch.float32).to(self.device)
        batch_action = torch.tensor(batch_action, dtype=torch.long).unsqueeze(1).to(self.device)
        batch_reward = torch.tensor(batch_reward, dtype=torch.float32).to(self.device)
        batch_next_state = torch.tensor(np.array(batch_next_state), dtype=torch.float32).to(self.device)
        batch_done = torch.tensor(batch_done, dtype=torch.float32).to(self.device)

        current_q_values = self.policy_net(batch_state).gather(1, batch_action)
        next_q_values = self.target_net(batch_next_state).max(1)[0].detach()
        expected_q_values = batch_reward + (self.gamma * next_q_values * (1 - batch_done))

        loss = nn.MSELoss()(current_q_values, expected_q_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update_target_net(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())

