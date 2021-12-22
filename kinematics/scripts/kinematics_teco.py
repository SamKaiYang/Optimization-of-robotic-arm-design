#!/usr/bin/env python3
# coding: utf-8

# # Robot Kinematics

# ## Initialize Robot Model
# - A robot model, at a very minimum, is a kinematic chain
# - The kinematic chain is defined by a series of parameters
#     - See [Modified DH parameters](https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters#Modified_DH_parameters) for more info

# In[1]:

from IPython.display import display
from pybotics.robot import Robot
from pybotics.predefined_models import teco

robot = Robot.from_parameters(teco())


# ## Forward Kinematics
# - The forward kinematics (FK) refer to the use of the kinematic equations of a robot to compute the pose of the end-effector (i.e., 4x4 transform matrix) from specified values for the joint parameters (i.e., joint angles)
# - ELI5: Where am I with the given joint angles?

# In[2]:


import numpy as np
np.set_printoptions(suppress=True)

joints = np.deg2rad([5,5,5,5,5,5])
pose = robot.fk(joints)
display(pose)


# ## Inverse Kinematics
# - The inverse kinematics (IK) makes use of the kinematics equations to determine the joint parameters that provide a desired position for the robot's end-effector
# - The default internal IK implementation uses scipy.optimize.least_squares with joint limit bounds
# - ELI5: What joint angles do I need to have this position?

# In[3]:


solved_joints = robot.ik(pose)
display(np.rad2deg(solved_joints))

