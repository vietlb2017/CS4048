#! /usr/bin/env python

import rospy
import sys
#linear and angular velocity
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped

from nav_msgs.msg import Path
from nav_msgs.msg import Odometry

rospy.init_node('vac_bot',anonymous = False)
true_path = Path()
beli_path = Path()

def big_brain():
	rate = rospy.Rate(10)	#10Hz
	while not rospy.is_shutdown():
		move_bot(-0.05,0.2)
		rate.sleep()
def move_bot(lin_vel,ang_vel):
	cmd_vel = rospy.Publisher('cmd_vel',Twist,queue_size=10)
	rate = rospy.Rate(10)	#10Hz

	#Creating Twist message instance
	vel = Twist()
	vel.linear.x = lin_vel
	vel.linear.y = 0
	vel.linear.z = 0

	vel.angular.x = 0
	vel.angular.y = 0
	vel.angular.z = ang_vel

	rospy.loginfo("Linear Vel = %f: Angular Vel = %f", lin_vel,ang_vel)
	#Publishing Twist message
	cmd_vel.publish(vel)

def true_path_cb(data):
	global true_path
	true_path.header = data.header
	pose = PoseStamped()
	pose.header = data.header
	pose.pose = data.pose.pose
	true_path.poses.append(pose)
	path_truth.publish(true_path)

def beli_path_cb(data):
	global beli_path
	beli_path.header = data.header
	pose = PoseStamped()
	pose.header = data.header
	pose.pose = data.pose.pose
	beli_path.poses.append(pose)
	path_truth.publish(beli_path)

sub_odom = rospy.Subscriber('/odom', Odometry, true_path_cb)
sub_truth = rospy.Subscriber('base_pose_ground_truth', Odometry, beli_path_cb)
path_odom = rospy.Publisher('/odom_path',Path,queue_size=10)
path_truth = rospy.Publisher('/truth_path',Path,queue_size=10)

if __name__ == '__main__':
	try:
		#Providing linear and angular velocity through command line
		big_brain()
	except rospy.ROSInterruptException:
		pass

