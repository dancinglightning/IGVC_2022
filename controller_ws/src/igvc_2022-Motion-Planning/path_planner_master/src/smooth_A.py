#!/usr/bin/env python
import numpy as np
import math
from scipy import interpolate
from scipy.interpolate import interp1d

import rospy
import roslib 
from nav_msgs.msg import Path
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped


path = Path()
path.header = Header()
path.header.frame_id = "/map"

    # for i in range(len(msg.poses)):
for i in range(len(y_org2)):
      
    vertex = PoseStamped()
      # vertex.header = std_msgs.msg.Header()
    vertex.header = Header()
    vertex.header.stamp = rospy.Time.now()
    vertex.header.frame_id="/map"

    vertex.pose.position.x= 250.0
    vertex.pose.position.y= 250.0
    vertex.pose.position.z= 0.0

    vertex.pose.orientation.x= 1.0
    vertex.pose.orientation.y= 1.0
    vertex.pose.orientation.z= 1.0
    vertex.pose.orientation.w= 0.0

    path.poses.append(vertex)
        
  pub.publish(path)


def main():
  global pub

  pub = rospy.Publisher("/initialpose", Path, queue_size=10)
  rate = rospy.Rate(10) # 10hz
  rate.sleep()
  rospy.spin()

if __name__ == '__main__':
  try:
    main()
  except rospy.ROSInterruptException:
    Pass
