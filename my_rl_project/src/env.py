import gym
import rospy
from std_msgs.msg import Twist  # or any relevant message type
from sensor_msgs.msg import LaserScan  # or other sensor data
import numpy as np

class TurtleBotGymEnv(gym.Env):
    def __init__(self):
        # Initialize Gym environment
        super(TurtleBotGymEnv, self).__init__()

        # Define action and observation space
        self.action_space = gym.spaces.Box(low=np.array([-1.0, -1.0]), high=np.array([1.0, 1.0]), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(360,), dtype=np.float32)

        # Initialize ROS node
        rospy.init_node('turtlebot_rl_node', anonymous=True)
        
        # Publishers and Subscribers
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.lidar_sub = rospy.Subscriber('/scan', LaserScan, self._lidar_callback)

        self.current_lidar_data = None

    def _lidar_callback(self, data):
        """Handle incoming lidar data"""
        self.current_lidar_data = data.ranges

    def step(self, action):
        """Send an action to Gazebo (e.g., velocity commands)"""
        # Convert action (e.g., velocity) into a ROS message
        twist_msg = Twist()
        twist_msg.linear.x = action[0]  # Forward/Backward velocity
        twist_msg.angular.z = action[1]  # Angular velocity

        # Publish the velocity command
        self.cmd_vel_pub.publish(twist_msg)

        # Get observation (lidar or other sensor data)
        obs = np.array(self.current_lidar_data) if self.current_lidar_data else np.zeros(360)

        # Calculate reward (for simplicity, assume constant reward for now)
        reward = 1.0

        # Determine if episode is done (e.g., collision detected or time limit reached)
        done = False

        # Additional information (optional)
        info = {}

        return obs, reward, done, info

    def reset(self):
        """Reset the environment"""
        # Send a reset command to Gazebo if needed, or reset internal variables
        rospy.loginfo("Resetting environment")

        # Return initial observation (sensor data)
        return np.zeros(360)

    def render(self, mode='human'):
        """Render the environment (optional, useful for debugging)"""
        pass

