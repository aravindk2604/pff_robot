#!/usr/bin/env python

import rospy, sys
from geometry_msgs.msg import Twist

def talker(diameter):
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    twist = Twist()

    # Angular velocity = linear velocity / radius
    radius = diameter/2;
    twist.linear.x = 2.0
    twist.angular.z = twist.linear.x/radius 
    while not rospy.is_shutdown():
        pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    diameter = float(sys.argv[1])
    if diameter <= 0:
        raise ValueError('Enter a positive value for radius!')
    talker(diameter)
