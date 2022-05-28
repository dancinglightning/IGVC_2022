#include "ros/ros.h"
#include "std_msgs/String.h"

#include <sstream>


int main(int argc, char **argv)
{
 
  ros::init(argc, argv, "initialPos");

  
  ros::NodeHandle n;

  
  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("/initialpose", 1000);

  //ros::Rate loop_rate(10);

 float x, y;
 x = 250;
 y = 250;
 
 


  return 0;
}