#!/usr/bin/env python3
# coding: utf-8

# # Robot Dynamics
# 
# - How is the motion of a manipulator affected by external forces?
# - What joints torques are generated from external forces applied to the manipulator?
# - The following example will demonstrate how to calculate the joint torques required to counteract a given TCP wrench.

# ## Create the Robot Model

# In[3]:


from pybotics.robot import Robot
from pybotics.predefined_models import ur10

robot = Robot.from_parameters(ur10())


# ## Define the Forces/Torques Acting on the TCP
# 
# - Aka the "wrench"

# In[4]:


forces = [0, 0, 10]
torques = [0, 0, 0]
wrench = [*forces, *torques]


# ## Calculate Joint Torques
# 
# - What are the joint torques required to counteract this payload?
# - This calculation can be repeated at each discrete pose in a trajectory for trajectory dynamics

# In[5]:


import numpy as np

robot.joints = np.deg2rad([0, 0, 0, 0, 0, 0])
j_torques = robot.compute_joint_torques(wrench)
print(f'Robot Joints: {robot.joints}')
print(f'Joint Torques: {j_torques}')

robot.joints = np.deg2rad([0, -90, -90, 0, -90, 0])
j_torques = robot.compute_joint_torques(wrench)
print(f'Robot Joints: {robot.joints}')
print(f'Joint Torques: {j_torques}')


# In[ ]:





# In[ ]:





# In[ ]:




