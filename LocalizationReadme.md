# Localization Readme

Follow the given instruction to make use the features added by Locallizatio Subsystem for your subsystem.

Clone changes done in the remote repo/branch since your last pull.
```
git fetch
```
Checkout to the localization branch
```
git checkout localization_subsystem
```
Build the package again
```bash
catkin_make
```
To convert pointclound to Laserscan run the command
```
roslaunch pointcloud_to_laserscan pointcloud_to_laserscan_node.launch
```
Get the laserscan on `/laserscan` topic.



