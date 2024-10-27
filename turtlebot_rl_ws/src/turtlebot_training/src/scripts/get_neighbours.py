#!/usr/bin/env python3

import rospy
import numpy as np
from grid_map_msgs.msg import GridMap
from std_msgs.msg import Float32MultiArray, MultiArrayDimension
from math import atan2, degrees

class RobotSurroundingElevationSlopeNode:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('robot_surrounding_elevation_slope_node', anonymous=True)

        # Subscribe to the elevation map to access the GridMapInfo
        self.elevation_map_sub = rospy.Subscriber("/elevation_mapping/elevation_map", GridMap, self.elevation_map_callback)

        # Publishers for elevation, slope, and cell coordinates
        self.elevation_pub = rospy.Publisher("/surrounding_elevation", Float32MultiArray, queue_size=1)
        self.slope_pub = rospy.Publisher("/surrounding_slope", Float32MultiArray, queue_size=1)
        self.cell_coords_pub = rospy.Publisher("/surrounding_cell_coords", Float32MultiArray, queue_size=1)

        # Variables to store grid map properties
        self.resolution = None
        self.origin_x = None
        self.origin_y = None
        self.grid_width = None
        self.grid_height = None

    def elevation_map_callback(self, msg):
        # Set grid map properties if not already set
        if self.resolution is None:
            self.resolution = msg.info.resolution
            self.grid_width = int(msg.info.length_x / self.resolution)
            self.grid_height = int(msg.info.length_y / self.resolution)

            # Calculate the map origin (bottom-left corner) in the world frame
            self.origin_x = msg.info.pose.position.x - msg.info.length_x / 2
            self.origin_y = msg.info.pose.position.y - msg.info.length_y / 2
            rospy.loginfo(f"Map origin: ({self.origin_x}, {self.origin_y}), Resolution: {self.resolution}")

        # Get the robot's position in the map frame
        robot_x = msg.info.pose.position.x
        robot_y = msg.info.pose.position.y

        # Calculate the robot's grid cell position
        grid_x = int((robot_x - self.origin_x) / self.resolution)
        grid_y = int((robot_y - self.origin_y) / self.resolution)

        # Define the range for the 20x20 grid around the robot
        half_size = 10
        min_x = max(0, grid_x - half_size)
        max_x = min(self.grid_width, grid_x + half_size)
        min_y = max(0, grid_y - half_size)
        max_y = min(self.grid_height, grid_y + half_size)

        # Find the index of the elevation layer
        try:
            elevation_layer_index = msg.layers.index("elevation")
        except ValueError:
            rospy.logwarn("Elevation layer not found in GridMap message.")
            return

        # Extract elevation values from the grid map
        elevation_values = np.array(msg.data[elevation_layer_index].data).reshape(self.grid_height, self.grid_width)
        surrounding_elevation = elevation_values[min_y:max_y, min_x:max_x]

        # Initialize arrays for slope values and cell coordinates
        slope_values = np.full(surrounding_elevation.shape, np.nan)
        cell_coordinates = np.zeros((20, 20, 2))  # 20x20 grid with (x, y) coordinates

        # Calculate slope and map coordinates for each cell
        for i in range(1, surrounding_elevation.shape[0] - 1):
            for j in range(1, surrounding_elevation.shape[1] - 1):
                # Calculate the world coordinates for the cell
                cell_x_map = self.origin_x + (min_x + j) * self.resolution
                cell_y_map = self.origin_y + (min_y + i) * self.resolution
                cell_coordinates[i, j] = [cell_x_map, cell_y_map]

                # Calculate slope using neighbors if available
                dz_dx = (surrounding_elevation[i, j + 1] - surrounding_elevation[i, j - 1]) / (2 * self.resolution)
                dz_dy = (surrounding_elevation[i + 1, j] - surrounding_elevation[i - 1, j]) / (2 * self.resolution)
                slope_values[i, j] = degrees(atan2((dz_dx**2 + dz_dy**2)**0.5, 1))

        # Publish the elevation array
        elevation_msg = Float32MultiArray()
        elevation_msg.layout.dim = [
            MultiArrayDimension(label="height", size=surrounding_elevation.shape[0], stride=surrounding_elevation.shape[0] * surrounding_elevation.shape[1]),
            MultiArrayDimension(label="width", size=surrounding_elevation.shape[1], stride=surrounding_elevation.shape[1])
        ]
        elevation_msg.data = surrounding_elevation.flatten().tolist()
        self.elevation_pub.publish(elevation_msg)

        # Publish the slope array
        slope_msg = Float32MultiArray()
        slope_msg.layout.dim = [
            MultiArrayDimension(label="height", size=slope_values.shape[0], stride=slope_values.shape[0] * slope_values.shape[1]),
            MultiArrayDimension(label="width", size=slope_values.shape[1], stride=slope_values.shape[1])
        ]
        slope_msg.data = slope_values.flatten().tolist()
        self.slope_pub.publish(slope_msg)

        # Publish cell coordinates as a flattened array
        cell_coords_msg = Float32MultiArray()
        cell_coords_msg.layout.dim = [
            MultiArrayDimension(label="height", size=cell_coordinates.shape[0], stride=cell_coordinates.shape[0] * cell_coordinates.shape[1] * 2),
            MultiArrayDimension(label="width", size=cell_coordinates.shape[1], stride=cell_coordinates.shape[1] * 2),
            MultiArrayDimension(label="coordinate", size=2, stride=2)
        ]
        cell_coords_msg.data = cell_coordinates.flatten().tolist()
        self.cell_coords_pub.publish(cell_coords_msg)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        node = RobotSurroundingElevationSlopeNode()
        node.run()
    except rospy.ROSInterruptException:
        pass
