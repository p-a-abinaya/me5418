#!/usr/bin/env python3
import rospy
import numpy as np
from turtlebot3_world import TurtleBot3WorldEnv
from dqn_model import DQNNetwork  # DQN model import
import torch

def test_initial_output():
    rospy.init_node('turtlebot3_dqn_test_initial_output', anonymous=True)
    
    # Initialize environment
    env = TurtleBot3WorldEnv()
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    
    # Initialize the DQN model
    model = DQNNetwork(state_size, action_size)
    model.eval()  # Set model to evaluation mode
    
    # Get the initial state from the environment
    state, _ = env.reset()
    #print(state)
    state = np.array(state)  # Ensure state is a NumPy array if not already
    
    # Convert state to tensor and pass it through the model
    state_tensor = torch.from_numpy(state).float()  # Convert to PyTorch tensor
    with torch.no_grad():  # No need for gradients
        q_values = model(state_tensor)  # Forward pass to get Q-values
    
    # Print the Q-values output
    print("Q-values for the initial state:", q_values.numpy())

if __name__ == '__main__':
    try:
        test_initial_output()
    except rospy.ROSInterruptException:
        pass

