import rospy
import numpy
from gym import spaces
from openai_ros import turtlebot3_env
from gym.envs.registration import register
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import PoseStamped
import numpy as np
import cv2
from tf.transformations import euler_from_quaternion
import cv_bridge
import math

# The path is __init__.py of openai_ros, where we import the TurtleBot2MazeEnv directly
timestep_limit_per_episode = 10000 # Can be any Value

register(
        id='TurtleBot3Terrainscape-v1',
        entry_point='openai_ros:TurtleBot3WorldEnv',
        max_episode_steps=timestep_limit_per_episode,
    )

class TurtleBot3WorldEnv(turtlebot3_env.TurtleBot3Env):
    def __init__(self):
        """
        This Task Env is designed for having the TurtleBot3 in the turtlebot3 world
        closed room with columns.
        It will learn how to move around without crashing.
        """
        
        # Only variable needed to be set here
        number_actions = 12
        self.action_space = spaces.Discrete(number_actions)
        
        # We set the reward range, which is not compulsory but here we do it.
        self.reward_range = (-numpy.inf, numpy.inf)
        #number_observations = rospy.get_param('/turtlebot3/n_observations')
        """
        We set the Observation space for the 6 observations
        cube_observations = [
            round(current_disk_roll_vel, 0),
            round(y_distance, 1),
            round(roll, 1),
            round(pitch, 1),
            round(y_linear_speed,1),
            round(yaw, 1),
        ]
        """
        
        # Actions and Observations
        self.angular_speed = 0
        self.init_linear_forward_speed = 0
        self.init_linear_turn_speed = 0

        self.max_linear_aceleration = 2.0
        
        
        # We create two arrays based on the binary values that will be assigned
        # In the discretization method.
        
        #laser_scan = self._check_laser_scan_ready()
        #num_laser_readings = len(laser_scan.ranges)/self.new_ranges
        #high = numpy.full((num_laser_readings), self.max_laser_value)
        #low = numpy.full((num_laser_readings), self.min_laser_value)
        #depth_pc = self._check_depth_cloud_ready()

        self._check_odom_ready()
        self.odom_data = self.get_odom()

        self._check_imu_ready()
        self.imu_data = self.get_imu()

        self._check_elevation_map_ready()    

        self.orientation_range = [-np.pi, np.pi]
        self.acceleration_range = [-10.0, 10.0]

        # Define the lower and upper bounds for the observation space
        low = np.array([self.orientation_range[0]] * 3 +
                    [self.acceleration_range[0]] * 3)
                    
        high = np.array([self.orientation_range[1]] * 3 +
                        [self.acceleration_range[1]] * 3)

        # Define the observation space using the Box space
        self.observation_space = spaces.Box(low, high, dtype=np.float32)
    

        # We only use two integers
        #self.observation_space = spaces.Box(low, high)
        
        rospy.logdebug("ACTION SPACES TYPE===>"+str(self.action_space))
        rospy.logdebug("OBSERVATION SPACES TYPE===>"+str(self.observation_space))
        
        # Rewards
        self.goal_position = [10.0, 10.0]

        self.linear_fast_speed = 0.25
        self.linear_slow_speed = 0.03
        self.linear_nominal_speed = 0.14

        self.in_place_left_speed = 0.5
        self.in_place_right_speed = -0.5
        self.max_left_turn_speed = 0.2
        self.max_right_turn_speed = -0.2

        self.cumulated_steps = 0.0

        # Here we will add any init functions prior to starting the MyRobotEnv
        super(TurtleBot3WorldEnv, self).__init__()

    def _set_init_pose(self):
        """Sets the Robot in its init pose
        """
        self.move_base( self.init_linear_forward_speed,
                        self.init_linear_turn_speed,
                        epsilon=0.05,
                        update_rate=10)

        return True


    def _init_env_variables(self):
        """
        Inits variables needed to be initialised each time we reset at the start
        of an episode.
        :return:
        """
        # For Info Purposes
        self.cumulated_reward = 0.0
        # Set to false Done, because its calculated asyncronously
        self._episode_done = False


    def _set_action(self, action):
        """
        This set action will set the linear and angular speed of the TurtleBot3
        based on the action number given.
        :param action: The action integer that sets what movement to do next.

        Action 0: forward, slow
        Action 1: forward, nominal
        Action 2: forward, fast

        Action 3: in place, turn left
        Action 4: in place, turn right

        Action 5: forward, slow, left
        Action 6: forward, slow, right

        Action 7: forward, nominal, left
        Action 8: forward, nominal, right

        Action 9: forward, fast, left
        Action 10: forward, fast, right

        """
        # Set linear and angular velocities based on the action
        if action == 0:  # Forward, slow
            linear_speed = self.linear_slow_speed  # Slow
            angular_speed = 0.0
            self.last_action = "FORWARD_SLOW"

        elif action == 1:  # Forward, nominal
            linear_speed = self.linear_nominal_speed # Nominal
            angular_speed = 0.0
            self.last_action = "FORWARD_NOMINAL"

        elif action == 2:  # Forward, fast
            linear_speed = self.linear_fast_speed # Fast
            angular_speed = 0.0
            self.last_action = "FORWARD_FAST"

        elif action == 3:  # In place, turn left
            linear_speed = 0.0
            angular_speed = self.in_place_left_speed
            self.last_action = "IN_PLACE_LEFT"

        elif action == 4:  # In place, turn right
            linear_speed = 0.0
            angular_speed = self.in_place_right_speed
            self.last_action = "IN_PLACE_RIGHT"

        elif action == 5:  # Forward, slow, left
            linear_speed = self.linear_slow_speed  # Slow
            angular_speed = self.max_left_turn_speed
            self.last_action = "FORWARD_SLOW_LEFT"

        elif action == 6:  # Forward, slow, right
            linear_speed = self.linear_slow_speed  # Slow
            angular_speed = self.max_right_turn_speed
            self.last_action = "FORWARD_SLOW_RIGHT"

        elif action == 7:  # Forward, nominal, left
            linear_speed = self.linear_nominal_speed  # Nominal
            angular_speed = self.max_left_turn_speed
            self.last_action = "FORWARD_NOMINAL_LEFT"

        elif action == 8:  # Forward, nominal, right
            linear_speed = self.linear_nominal_speed  # Nominal
            angular_speed = self.max_right_turn_speed
            self.last_action = "FORWARD_NOMINAL_RIGHT"

        elif action == 9:  # Forward, fast, left
            linear_speed = self.linear_fast_speed  # Fast
            angular_speed = self.max_left_turn_speed
            self.last_action = "FORWARD_FAST_LEFT"

        elif action == 10:  # Forward, fast, right
            linear_speed = self.linear_fast_speed # Fast
            angular_speed = self.max_right_turn_speed
            self.last_action = "FORWARD_FAST_RIGHT"

        # Log the chosen action
        rospy.logdebug(f"Action Set: {self.last_action} -> Linear Speed = {linear_speed}, Angular Speed = {angular_speed}")

        # Set the base movement with the chosen linear and angular velocities
        self.move_base(linear_speed, angular_speed, epsilon=0.05, update_rate=10)

        rospy.logdebug("END Set Action ==> " + str(action))


    def _get_obs(self):
        """
        Here we define what sensor data defines our robots observations
        To know which Variables we have acces to, we need to read the
        TurtleBot2Env API DOCS
        :return:
        """
        rospy.logdebug("Start Get Observation ==>")
        # We get the laser scan data
        #laser_scan = self.get_laser_scan()
        #depth_pc = self.get_depth_cloud()
        '''
        discretized_observations = self.discretize_scan_observation(    laser_scan,
                                                                        self.new_ranges
                                                                        )

        rospy.logdebug("Observations==>"+str(discretized_observations))
        rospy.logdebug("END Get Observation ==>")
        return discretized_observations
        '''

        # We get the map data
        elevation_map = self.get_elevation_map()
        elevation_dictionary_list = self.elevation_map_observation(elevation_map)
        rospy.logdebug("END Get Observation ==>")
        return elevation_dictionary_list

    def _is_done(self, elevation_dictionary_list):
        
        if self._episode_done:
            rospy.logerr("TurtleBot is Too Close to wall==>")
        else:
            rospy.logwarn("TurtleBot is NOT close to a wall ==>")
            
        # Now we check if it has crashed based on the imu
        linear_acceleration_magnitude = self.get_vector_magnitude(self.imu_data.linear_acceleration)
        if linear_acceleration_magnitude > self.max_linear_aceleration:
            rospy.logerr("TurtleBot Crashed==>"+str(linear_acceleration_magnitude)+">"+str(self.max_linear_aceleration))
            self._episode_done = True
        else:
            rospy.logerr("DIDNT crash TurtleBot ==>"+str(linear_acceleration_magnitude)+">"+str(self.max_linear_aceleration))
        

        return self._episode_done

    def _compute_reward(self, elevation_dictionary_list, done):

        current_position = self.odom_data.pose.pose.position
        goal_position = self.goal_position
        distance_to_goal = self.distance_to_goal(current_position, goal_position)

        current_velocity = self.odom_data.twist.twist.linear.x
        orientation_q = [self.imu_data.orientation.x, self.imu_data.orientation.y, self.imu_data.orientation.z, self.imu_data.orientation.w]
        roll, pitch, yaw = euler_from_quaternion(orientation_q)
        yaw_rate = self.imu_data.angular_velocity.z

        alpha = 1.0
        beta = 1.0
        gamma = 1.0
        delta = 1.0

        r_goal = -alpha*distance_to_goal
        r_energy = -beta*current_velocity*self.terrain_difficulty()
        r_terrain = -delta*current_velocity*self.terrain_difficulty()*(abs(roll)+abs(pitch))
        r_stability = -gamma*yaw_rate*self.get_vel_change_rate(current_velocity, self.last_action)

        r_goal_achieved = 0

        if done and self.is_goal_achieved():
            R_goal = 100
            r_goal_achieved = R_goal

        total_reward = r_goal + r_energy + r_terrain + r_stability + r_goal_achieved
        rospy.logdebug(f"Reward components -> r_goal: {r_goal}, r_energy: {r_energy}, r_terrain: {r_terrain}, r_stability: {r_stability}, r_goal_achieved: {r_goal_achieved}")
        rospy.logdebug(f"Total reward: {total_reward}")

        self.cumulated_reward += total_reward
        self.cumulated_steps += 1

        return total_reward


    # Internal TaskEnv Methods

    def elevation_map_observation(self, data):
        '''
        The idea is to consider only certain cells from the elevation map that are in the vicinity of
        the robot as observations. we make use of "elevation_mapping" package by AnyBotics here. 

        So we perform the following:
            1. consider only those cells within 1.5m radius.
            2. extract elevation values of the cells
            3. compute their slopes with respect to a fixed frame ie. /odom
            
        '''

        rospy.loginfo("Starting elevation map observation...")

        # Get the elevation layer from the grid map
        try:
            layer_index = data.layers.index("elevation")
            elevation_data = np.array(data.data[layer_index].data)
        except ValueError as e:
            rospy.logerr("Elevation layer not found in the grid map. Error: {}".format(e))
            return [], []


        # grid properties
        resol = data.info.resolution #cell size in meters
        map_len_x = data.info.length_x #total length of grid in x dir
        map_len_y = data.info.length_y #total length of grid in y dir
        map_position = data.info.pose.position #position of map's centre in the fixed frame
        rospy.loginfo("Grid map properties: resolution = {}, map size = ({}, {})".format(resol, map_len_x, map_len_y))


        # to get the robot's orientation and position
        robot_position = self.odom_data.pose.pose.position
        rospy.loginfo("Robot's current position: x = {}, y = {}, z = {}".format(robot_position.x, robot_position.y, robot_position.z))

        #self._check_imu_ready()
        #imu_data = self.get_imu()
        #quat = [imu_data.orientation.x, imu_data.orientation.y, imu_data.orientation.z, imu_data.orientation.w]
        #(roll, pitch, yaw) = euler_from_quaternion(quat)
        radius = 1.5

        cell_info_list = []

        # loop through all cells in the elevation layer
        for i in range(len(elevation_data)):
            # convert the 1D index to 2D grid coordinates (x, y)
            x_index = i % map_len_x
            y_index = i // map_len_x

            # convert grid coordinates to world coordinates
            cell_x = map_position.x + (x_index - map_len_x // 2) * resol
            cell_y = map_position.y + (y_index - map_len_y // 2) * resol

            # calculate distance from robot to the cell
            distance = np.linalg.norm([cell_x - robot_position.x, cell_y - robot_position.y])

            # if within the 1.5m radius, add the elevation value to the list and calculate slope between neighboring cells
            if distance <= radius:
                cell_elevation = elevation_data[i]
                # Calculate slope using neighbors (right and down as an example)
                slope = 0
                num_neighbors = 0

                if x_index + 1 < map_len_x:  # Right neighbor
                    neighbor_elevation_right = elevation_data[i + 1]
                    delta_z_right = neighbor_elevation_right - cell_elevation
                    slope_right = delta_z_right / resol  # Horizontal distance between neighbors is the resolution
                    slope += slope_right
                    num_neighbors += 1

                if y_index + 1 < map_len_y:  # Downward neighbor
                    neighbor_elevation_down = elevation_data[i + map_len_x]
                    delta_z_down = neighbor_elevation_down - cell_elevation
                    slope_down = delta_z_down / resol
                    slope += slope_down
                    num_neighbors += 1

                # Average slope if there are valid neighbors
                if num_neighbors > 0:
                    slope /= num_neighbors

                # Store cell information in a dictionary
                cell_info = {
                    'cell_number': i,             # The cell index
                    'elevation': cell_elevation,   # The elevation of the cell
                    'slope': slope                 # The slope of the cell
                }
                cell_info_list.append(cell_info)

        # Return both elevation values and slopes
        return cell_info_list
        
    def get_vector_magnitude(self, vector):
        """
        It calculated the magnitude of the Vector3 given.
        This is usefull for reading imu accelerations and knowing if there has been 
        a crash
        :return:
        """
        contact_force_np = numpy.array((vector.x, vector.y, vector.z))
        force_magnitude = numpy.linalg.norm(contact_force_np)

        return force_magnitude
    
    def distance_to_goal(self, curr, goal):
        dx = curr.x - goal[0]
        dy = curr.y - goal[1]

        distance = math.sqrt(dx**2 + dy**2)
        return distance
    
    def get_vel_change_rate(self, current):
        if self.last_action == "FORWARD_SLOW":
            last_v = self.linear_slow_speed
        elif self.last_action == "FORWARD_NOMINAL":
            last_v = self.linear_nominal_speed
        elif self.last_action == "FORWARD_FAST":
            last_v = self.linear_fast_speed
        elif self.last_action in ["FORWARD_SLOW_LEFT", "FORWARD_SLOW_RIGHT"]:
            last_v = self.linear_slow_speed
        elif self.last_action in ["FORWARD_NOMINAL_LEFT", "FORWARD_NOMINAL_RIGHT"]:
            last_v = self.linear_nominal_speed
        elif self.last_action in ["FORWARD_FAST_LEFT", "FORWARD_FAST_RIGHT"]:
            last_v = self.linear_fast_speed
        else:
            # If the last action was not related to forward movement, assume no forward velocity
            last_v = 0.0

        # Compute the velocity change rate (difference between current velocity and last action's velocity)
        velocity_change_rate = current - last_v

        return velocity_change_rate
    
    def terrain_difficulty(self, elevation_dictionary_list):
        return
    
    def is_goal_achieved(self, position):
        dx = position.x - self.goal_position[0]
        dy = position.y - self.goal_position[1]

        if abs(dx) and abs(dy) <= 0.01:
            return True
        else:
            return False