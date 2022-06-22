#!/usr/bin/env python
import numpy as np
import rospy
from geometry_msgs.msg import Pose,  PoseStamped
from nav_msgs.msg import Path
from std_msgs.msg import Float64MultiArray, Float64
from gazebo_msgs.msg import ModelStates
from math import *
import matplotlib.pyplot as plt


class MP():
	def __init__(self):
		# generate a numpy array for y ranging form 0-40 unofrormly having 1000 points
		self.x = np.linspace(-50, 50, 500)

		#maximum allowable ranges on the right and left
		self.max_r = 1.5
		self.max_l = 1.5

		self.vel = 20
		self.car_x = 0
		self.car_y = 0
	
		rospy.init_node('MP_mock', anonymous=True)
		self.sub_car = rospy.Subscriber('/gazebo/model_states', ModelStates, self.car_callback)

		#publishers for vel, limits and path
		self.pub_path = rospy.Publisher('/path', Path, queue_size=10)
		self.pub_vel = rospy.Publisher('/velocity_array2', Float64MultiArray, queue_size=10)
		self.pub_width = rospy.Publisher('/safewidth_node', Path, queue_size=10)

		self.path = Path()
		self.path.header.frame_id = "map"
		self.path.header.stamp = rospy.Time.now()
		self.width = Path()
		self.width.header.frame_id = "map"
		self.width.header.stamp = rospy.Time.now()
		self.Vel= []
		self.velocity = Float64MultiArray()

		for i in range(len(self.x)):
			self.pose1 = PoseStamped()
			
			self.pose1.pose.position.x = self.x[i]
			self.pose1.pose.position.y = 2*sin(self.x[i])
			self.path.poses.append(self.pose1)

			self.pose2 = PoseStamped()
			self.pose2.pose.position.x = self.max_r
			self.pose2.pose.position.y = self.max_l
			self.width.poses.append(self.pose2)

		self.Vel.append(self.vel)
		self.velocity.data = self.Vel

		rospy.spin()

	def car_callback(self, car):
		self.car_x = car.pose[11].position.x
		self.car_y = car.pose[11].position.y

		# self.path = Path()
		# self.path.header.frame_id = "map"
		# self.path.header.stamp = rospy.Time.now()
		# for i in range(len(self.x)):
		# 	self.pose1 = PoseStamped()
		# 	self.pose2 = PoseStamped()
		# 	self.pose1.pose.position.x = self.car_x + 1
		# 	self.pose1.pose.position.y = self.car_y + 1
		# 	self.path.poses.append(self.pose1)

		# 	self.pose2.pose.position.x = self.max_r
		# 	self.pose2.pose.position.y = self.max_l
		# 	self.width.poses.append(self.pose2)

		# print(self.path)
		self.pub_path.publish(self.path)
		self.pub_vel.publish(self.velocity)
		self.pub_width.publish(self.width)


if __name__ == '__main__':
	mp_mock = MP()


