#!/usr/bin/env python3

import gym
import rospy
import rospkg
from gym import wrappers
import turtlebot3_world

if __name__ == '__main__':
    
    # Initialize the ROS node
    rospy.init_node('turtlebot3_gym_test', anonymous=True)

    # Create the Gym environment
    env = gym.make('TurtleBot3Terrainscape-v0')
    rospy.loginfo("Gym environment initialized")    

    # Reset the environment to get the initial observation
    observation = env.reset()
    rospy.loginfo(f"Initial Observation: {observation}")

    # Take one deterministic action
    # For example, let's say action 0 is 'forward' as per your action space setup
    action = 0
    rospy.loginfo(f"Taking action: {action}")

    # Take the step with the selected action
    observation, reward, done, info = env.step(action)

    # Log the output from the step
    rospy.loginfo(f"Observation after action: {observation}")
    rospy.loginfo(f"Reward received: {reward}")
    rospy.loginfo(f"Done status: {done}")
    rospy.loginfo(f"Additional info: {info}")

    # Close the environment when done
    env.close()
