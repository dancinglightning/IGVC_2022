#!/usr/bin/env python2
import numpy as np
import rospy
from geometry_msgs.msg import Pose
from nav_msgs.msg import Path
from std_msgs.msg import Float64MultiArray
rospy.init_node("MP_mock")

# generate a numpy array for y ranging form 0-40 unofrormly having 1000 points
x = np.zeros([1000,1])
y = np.linspace(-20,20,1000)

#maximum allowable ranges on the right and left
max_r = 1.5
max_l = 1.5

#velocity array
vel = 1.5

#publishers for vel, limits and path
pub_path = rospy.Publisher('/Smooth_Hybrid_node', Path, queue_size=10)
pub_vel = rospy.Publisher('/velocity_array2', Float64MultiArray, queue_size=10)
pub_width = rospy.Publisher('/safewidth_node', Path, queue_size=10)

while True:
	try:
		path = Path()
		width = Path()
		Vel= []
		velocity = Float64MultiArray()
		pose1 = Pose()
		pose2 = Pose()
		for i in range(1000):
		    pose1.position.x = x[i]
		    pose1.position.y = y[i]
		    # path.poses.append(pose1)
		    pose2.position.x = max_r
		    pose2.position.y = max_l
		    width.poses.append(pose2)
		    Vel.append(vel)

		velocity.data = Vel
		# pub_path.publish(path)
		pub_vel.publish(velocity)
		pub_width.publish(width)
	except KeyboardInterrupt:
		break



