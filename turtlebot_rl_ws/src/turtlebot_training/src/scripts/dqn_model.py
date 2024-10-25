import rospy #not sure about this lol 
import torch
import torch.nn as net   #run on cpu if there is error
import torch.optim as optim
import random
import numpy as np
from collections import deque
from turtlebot3_world import TurtleBot3WorldEnv  

class DQNNetwork(net.Module):
    def __init__(self, state_size, action_size):
        super(DQNNetwork, self).__init__()
        self.fc1 = net.Linear(state_size, 128)  #check 128 note to self
        self.fc2 = net.Linear(128, 128)
        self.fc3 = net.Linear(128, action_size)

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
