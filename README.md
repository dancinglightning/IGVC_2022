# IGVC 2022 

This repo will be used for testing various tasks on the [igvc self-drive simulator](https://github.com/robustify/igvc_self_drive_sim). 

Just cross-check the branch in which you want to commit before pushing your code. 

## Installation steps:

> Directions for installing the simulator on **ubuntu 18.04** and **ros-melodic**:

Clone the repo:
```bash
cd ~/
cd catkin_ws/src
git clone https://github.com/Innovation-Cell/igvc_2022.git
cd igvc_2022
git checkout simulation_subsystem
```
After cloning into a ROS workspace, run the following command from the root of the workspace to install the necessary ROS package dependencies to make everything work correctly:
```bash
cd ../..
rosdep install --from-paths src --ignore-src -r
```
Build the repo using:
```bash
catkin_make
```

Test the installation:

source all the terminals using: `source devel/setup.bash`

1. To just spawn the vehicle do
```
roslaunch igvc_self_drive_gazebo load_task_world.launch
roslaunch igvc_self_drive_gazebo spawn_gem.launch
```

2. Just to check if vehicle could be controlled with throttle
```
rostopic pub /throttle_cmd std_msgs/Float64 "data: 0.5" -r 2
```

3. Encouraged to visualize/ echo rostopics for sensor values

Note: install the opencv-contrib library
```
pip uninstall opencv-contrib-python opencv-python
pip install opencv-contrib-python
```

4. To check the lane detection module use this:
```
rosrun igvc_self_drive_gazebo lane_det2.py
```
You can find the code script for `lanedet2.py` [here](https://github.com/Innovation-Cell/igvc_2022/blob/localization_subsystem/igvc_self_drive_sim/igvc_self_drive_gazebo/scripts/lane_det2.py). <br>
The script publishes Lane Occ Grid(on `/cv/laneoccgrid`) and local goal(on `/move_base_simple/goal`)

<br>

> Directions for installing the simulator on **ubuntu 20.04** and **ros-noetic**:

Install this library and follow similar steps as that of ros melodic
```bash
sudo apt install python-is-python3
```

## Organization of the repository

1. `igvc_self_drive_description` is the package for the vehicle xacro files
2. `igvc_self_drive_gazebo` package contains the various launch files for the IGVC specific tasks, model sdf files for obstacles & traffic signs and the world file
3. `igvc_self_drive_gazebo_plugins` contains customs plugins made to control the vehicle
Further detaiils of the same could be found [here](https://github.com/robustify/igvc_self_drive_sim/blob/master/README.md#controlling-the-simulated-vehicle) 
4. To know more about the topics in the simulation, refer to this [document](https://docs.google.com/document/d/1TG5LesTlsqQAeXfDH4BbXMnDPJmeLvAt34RsU-IX9L8/edit?usp=sharing)
