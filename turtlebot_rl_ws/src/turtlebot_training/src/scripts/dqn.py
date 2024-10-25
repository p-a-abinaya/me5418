import rospy
import numpy as np
from turtlebot3_world import TurtleBot3WorldEnv
from dqn_model import DQNNetwork  # network
import torch
import torch.optim as optim
import random
from collections import deque

class TurtleBot3DQNAgent:
    def __init__(self):
        rospy.init_node('turtlebot3_dqn_node', anonymous=True)

        self.env = TurtleBot3WorldEnv()

        self.state_size = self.env.observation_space.shape[0]
        self.action_size = self.env.action_space.n
        self.lr = 0.001
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.batch_size = 64
        self.memory = deque(maxlen=2000)

        self.model = DQNNetwork(self.state_size, self.action_size)
        self.target_model = DQNNetwork(self.state_size, self.action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)

    def select_action(self, state):
        #"""Epsilon-greedy action selection.""" 
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.action_size)
        else:
            q_values = self.model(torch.from_numpy(state).float())
            return np.argmax(q_values.detach().numpy())

    def replay(self):
        #"""Sample a batch from memory and train the model."""
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.max(self.target_model(torch.from_numpy(next_state).float()).detach().numpy())
            target_f = self.model(torch.from_numpy(state).float()).detach().numpy()
            target_f[0][action] = target

            self.optimizer.zero_grad()
            loss = torch.nn.MSELoss()(self.model(torch.from_numpy(state).float()), torch.tensor(target_f))
            loss.backward()
            self.optimizer.step()

    def train(self, episodes=1):
        #"""Train the DQN agent on the environment."""
        for e in range(episodes):
            state = self.env.reset()
            state = np.reshape(state, [1, self.state_size])
            done = False
            total_reward = 0

            while not done:
                # not sure about the action, for testing you give something
                next_state, reward, done, _ = self.env.step(action)
                next_state = np.reshape(next_state, [1, self.state_size])
        
                self.memory.append((state, action, reward, next_state, done))
                self.replay()

                total_reward += reward

            
                if done:
                    print(f"Episode: {e}/{episodes}, Score: {total_reward}, Epsilon: {self.epsilon}")
                    break

            
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
           
            if e % 10 == 0:
                self.target_model.load_state_dict(self.model.state_dict())

if __name__ == '__main__':
    try:
        agent = TurtleBot3DQNAgent()
        agent.train(episodes=1) #randomly gave 1000 eps
    except rospy.ROSInterruptException:
        pass
