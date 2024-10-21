ROS distro: noetic
gazebo version: 11.11.0
gym version: Version: 0.24.1

Packages installed: 
## elevation_mapping by anybotics: 
https://github.com/ANYbotics/elevation_mapping.git

Dependencies:

grid_map: https://github.com/anybotics/grid_map

To install elevation mapping package:

> sudo apt-get install libeigen3-dev

> sudo apt-get install ros-noetic-grid-map

> cd workspace/src

> git clone https://github.com/ANYbotics/elevation_mapping.git

> cd ..

> catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release

> catkin build

## turtlebot3 simulation installation

> cd workspace/src

> git clone -b noetic-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git

> git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git

> cd ..

> catkin build

## openai_ros installation

> cd workspace/src

> git clone https://github.com/anton-matosov/openai_ros.git

> git clone https://bitbucket.org/theconstructcore/theconstruct_msgs.git

> cd ..

> catkin build 

## ws building
- remove devel and build folders from the turtlebot_rl_ws in the zip folder
- catkin build

> rm -rf devel build

> catkin build

> source devel/setup.bash


## to run the code
(launch file to be taken from the zip folder; path: turtlebot_rl_ws/src/elevation_mapping/elevation_mapping_demos/launch/turtlesim3_waffle_demo.launch)

> roslaunch elevation_mapping_demos turtlesim3_waffle_demo.launch

> rosnode turtlebot_training test.py