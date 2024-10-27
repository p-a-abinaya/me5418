#include <ros/ros.h>
#include <grid_map_msgs/GridMap.h>

ros::Publisher trial_pub;

void gridMapCallback(const grid_map_msgs::GridMap& msg) {
    // Directly publish the received message to the /trial topic
    trial_pub.publish(msg);
}

int main(int argc, char** argv) {
    // Initialize the ROS node
    ros::init(argc, argv, "elevation_map_republisher");
    ros::NodeHandle nh;

    // Publisher for the /trial topic
    trial_pub = nh.advertise<grid_map_msgs::GridMap>("/trial", 1);

    // Subscriber for the /elevation_mapping/elevation_map topic
    ros::Subscriber sub = nh.subscribe("/elevation_mapping/elevation_map", 1, gridMapCallback);

    // Spin to keep the node alive and responsive to callbacks
    ros::spin();
    return 0;
}
