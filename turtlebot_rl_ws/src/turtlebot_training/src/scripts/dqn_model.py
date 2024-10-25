import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque

class DQNNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQNNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Hyperparameters
state_size = 6  # Example size of state vector
action_size = 12  # Number of actions (as defined in the environment)
lr = 0.001
gamma = 0.99
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995
batch_size = 64
memory = deque(maxlen=2000)
model = DQNNetwork(state_size, action_size)
target_model = DQNNetwork(state_size, action_size)
optimizer = optim.Adam(model.parameters(), lr=lr)

# Training loop
for episode in range(max_episodes):
    state = env.reset()
    state = np.reshape(state, [1, state_size])  # Ensure state is the correct shape for the NN
    done = False
    while not done:
        # Choose action based on epsilon-greedy policy
        if np.random.rand() < epsilon:
            action = np.random.choice(action_size)
        else:
            q_values = model(torch.from_numpy(state).float())
            action = np.argmax(q_values.detach().numpy())

        # Execute the action
        next_state, reward, done, _ = env.step(action)
        next_state = np.reshape(next_state, [1, state_size])

        # Store experience in replay memory
        memory.append((state, action, reward, next_state, done))

        # Train the model using a random batch from memory
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
            for s, a, r, s_next, done in minibatch:
                target = r
                if not done:
                    target = r + gamma * np.max(target_model(torch.from_numpy(s_next).float()).detach().numpy())
                target_f = model(torch.from_numpy(s).float()).detach().numpy()
                target_f[0][a] = target
                optimizer.zero_grad()
                loss = nn.MSELoss()(model(torch.from_numpy(s).float()), torch.tensor(target_f))
                loss.backward()
                optimizer.step()

        state = next_state

        if done:
            print(f"Episode {episode} finished with reward {reward}")
            epsilon = max(epsilon_min, epsilon_decay * epsilon)
