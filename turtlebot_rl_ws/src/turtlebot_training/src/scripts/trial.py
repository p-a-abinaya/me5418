#!/usr/bin/env python3

import rospy
from grid_map_msgs.msg import GridMap

class ElevationMapListener:
    def __init__(self):
        # Subscribe to the elevation map topic
        self.subscriber = rospy.Subscriber('/elevation_mapping/elevation_map', GridMap, self.callback)
        self.message_received = False

    def callback(self, msg):
        # Store and print the message content once
        if not self.message_received:
            rospy.loginfo("Received an elevation map message:")
            rospy.loginfo(msg)
            self.message_received = True
            rospy.signal_shutdown("Message received, shutting down.")

    def listen(self):
        # Initialize the ROS node
        rospy.init_node('elevation_map_listener', anonymous=True)
        rospy.loginfo("Waiting for one message from /elevation_mapping/elevation_map...")
        
        # Spin until the message is received and processed
        rospy.spin()

if __name__ == '__main__':
    listener = ElevationMapListener()
    listener.listen()

