# Optimization-of-robotic-arm-design
## References
###  UR5
1. https://github.com/tku-iarc/UR5_control
2. https://github.com/UniversalRobots/Universal_Robots_ROS_Driver
### Python code 
1. [https://petercorke.github.io/robotics-toolbox-python/intro.html#robotics-toolbox](https://petercorke.github.io/robotics-toolbox-python/intro.html#robotics-toolbox)
2. [https://github.com/petercorke/robotics-toolbox-python](https://github.com/petercorke/robotics-toolbox-python)
3. [http://motion.cs.illinois.edu/software/klampt/latest/pyklampt_docs/index.html](http://motion.cs.illinois.edu/software/klampt/latest/pyklampt_docs/index.html)
4. https://github.com/cdsousa/SymPyBotics
5. [https://github.com/pydy/pydy](https://github.com/pydy/pydy)
6. [https://github.com/Sarrasor/RoboticManipulators](https://github.com/Sarrasor/RoboticManipulators)[https://petercorke.github.io/robotics-toolbox-python/intro.html#robotics-toolbox](https://petercorke.github.io/robotics-toolbox-python/intro.html#robotics-toolbox)
### C code
1. [https://github.com/dartsim/dart](https://github.com/dartsim/dart)
2. https://github.com/CNR-STIIMA-IRAS/rosdyn
3. [https://github.com/roboticslibrary/rl](https://github.com/roboticslibrary/rl)

## Solves
1. https://blog.csdn.net/gyxx1998/article/details/118153079
2. https://blog.csdn.net/zxxxiazai/article/details/103568577


# 範例程式
==================
## 運行動力學分析(靜態),求取torque 
```bash
rosrun dynamics dynamics_teco.py
```
## 運行手臂軌跡規劃,求取各軸角度,速度,加速度
```bash
rosrun trajectory_generation trajectory_generation_teco.py 
```
## 運行動力學手臂全工作空間分析(靜態),求取最大torque 
```bash
rosrun dynamics dynamics_teco_space_ex.py
```

# 顯示與操作介面
```bash
rosrun interface_control interface_GUI.py
rosrun dynamics dynamics_function_teco.py 

```
# 執行moveit demo
```bash
roslaunch teco_config demo.launch
##moveit python interface 
rosrun teco_config move_group_python_interface_tutorial.py 
```

```bash
roslaunch teco_config demo.launch
##moveit c++ interface launch
roslaunch moveit_tutorials move_group_interface_teco.launch 
```


>>2022/01/04 更新
1. 新增工作空間分析
2. 新增軌跡規劃求取各軸角度,速度,加速度

