#!/usr/bin/env python
import rospy, sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


def callback(data):
	# Saving initial pose at each corner
	global x0, y0, theta0
	global first, length
    	if(first):
    		x0 = data.pose.pose.position.x
    		y0 = data.pose.pose.position.y
    		theta0 = toEulerianAngle(data)
    		first = False

	# Get current pose
    	x = data.pose.pose.position.x
    	y = data.pose.pose.position.y
        theta = toEulerianAngle(data)
	
	# Check if side-length is covered
   	if abs(x - x0) >= length or abs(y - y0) >= length:
   		twist.linear.x = 0.0
   		twist.angular.z = 0.5		
		
		# Turn left by 90 degrees
	   	if abs(theta - theta0) >= 1.57:
            		twist.angular.z = 0
            		twist.linear.x = 0.5
            		first = True
        	else:
	   		twist.angular.z = 0.5
            		twist.linear.x = 0
    	# Move forward if side-length is not covered yet	
    	else:		
    		twist.linear.x = 0.5
   		twist.angular.z = 0

	pub.publish(twist)


def toEulerianAngle(data):
    '''Converts quaternion orientation to angle in radians'''
    q_x = data.pose.pose.orientation.x
    q_y = data.pose.pose.orientation.y
    q_z = data.pose.pose.orientation.z
    q_w = data.pose.pose.orientation.w
    t3 = 2.0 * (q_w * q_z + q_x * q_y)
    t4 = 1.0 - 2.0 * ((q_y * q_y) + q_z * q_z)
    theta = math.atan2(t3, t4)
    return theta

if __name__ == '__main__':
    global length
    length = float(sys.argv[1])
    if length <= 0:
        raise ValueError('Enter a positive value for side-length!')
    global first
    first = True

    global x0, y0
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/odom", Odometry, callback)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10) # 10hz

    global twist
    twist = Twist()

    while not rospy.is_shutdown():
	    rate.sleep()
