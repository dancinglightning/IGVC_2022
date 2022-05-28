#include <bits/stdc++.h>
#include <fstream>
#include <algorithm>
#include <math.h>
#include "ros/ros.h"
#include <gazebo_msgs/ModelStates.h>
#include <nav_msgs/Path.h>
#include <std_msgs/Float64MultiArray.h>
#include <std_msgs/Bool.h>
#include <std_msgs/Float64.h>
using namespace std;

int a = 0.1;          // max accl; unit not sure
float vmax = 2.2;   // in m/s unit from 5mph

std_msgs::Float64MultiArray Vel;
float currentvel;
float MapRes = 0.3; // current map resolution in hyb a*

ros::Publisher pub_vel_arr;

void CurrentVel(const gazebo_msgs::ModelStates::ConstPtr& msg)
{
    currentvel = msg->twist[11].linear.x;
    
    //cout<<currentvel<<endl;
    
    
}

void PathCallback(const nav_msgs::Path::ConstPtr& msg)
{
    int NumData = msg->poses.size();
    vector<double> PathDis;
    PathDis.push_back(0.0);
    for(int i=1; i<=NumData; i++)
    {
        double x1 = msg->poses[i-1].pose.position.x ,x2 = msg->poses[i].pose.position.x;
        double y1 = msg->poses[i-1].pose.position.y ,y2 = msg->poses[i].pose.position.y;
        PathDis.push_back(PathDis[i-1]+MapRes*sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1))));
    }
    
    Vel.data.push_back(currentvel);
    //cout<< "currentvel_path: "<<currentvel<<endl;
    float u = Vel.data[0]; 
    for(int i=1; i<=NumData; i++)
    {
        float v = sqrt((u*u) + (2*a*PathDis[i]));
        if(v < vmax)
        {        
            Vel.data.push_back(v);
        }
        else
        {
            Vel.data.push_back(vmax);
        }
    }
	pub_vel_arr.publish(Vel);	
    Vel.data.clear();
}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "vel_arr_basic");
	ros::NodeHandle RosNodeH;

    ros::Subscriber something = RosNodeH.subscribe("/gazebo/model_states",1,CurrentVel);
	ros::Subscriber sub_path = RosNodeH.subscribe("/path",1,PathCallback); 

    pub_vel_arr = RosNodeH.advertise<std_msgs::Float64MultiArray>("/best_velocity", 1);			

	ros::Rate loop_rate(200);

	while (ros::ok())
	{
		ros::spinOnce();
		loop_rate.sleep();
	}
	return 0;
}