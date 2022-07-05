#!/usr/bin/env python3
# coding: utf-8
import importlib
import sys

import rospy

importlib.reload(sys)
import argparse
import csv
import math
import time
from collections import namedtuple
from math import pi
from os import path

import geometry_msgs.msg
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import plotly.graph_objs as go
import plotly.offline as py
import roboticstoolbox as rtb
import sympy as sp
# import dyna_space
from interface_control.msg import (cal_cmd, cal_process, cal_result, dyna_data,
                                   dyna_space_data, optimal_design,
                                   optimal_random, specified_parameter_design)
from matplotlib import cm
from moveit_msgs.msg import DisplayTrajectory, RobotTrajectory
from mpl_toolkits.mplot3d import Axes3D
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, Font, colors
from openpyxl.utils import get_column_letter
from plotly.offline import download_plotlyjs, iplot, plot
from scipy.interpolate import make_interp_spline  # draw smooth
from spatialmath import *
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

np.set_printoptions(
    linewidth=100,
    formatter={"float": lambda x: f"{x:8.4g}" if abs(x) > 1e-10 else f"{0:8.4g}"},
)

import pandas as pd

from arm_workspace import arm_workspace_plane
# from robot_urdf import RandomRobot
from motor_module import mootor_data
from random_robot import RandomRobot

class drl_optimization:
    def __init__(self):
        self.test = 0
    
        # callback:Enter the parameters of the algorithm to be optimized on the interface
        self.sub_optimal_design = rospy.Subscriber(
            "/optimal_design", optimal_design, self.optimal_design_callback
        )
        # callback:Randomly generated shaft length due to optimization algorithm
        self.sub_optimal_random = rospy.Subscriber(
            "/optimal_random", optimal_random, self.optimal_random_callback
        )

    def robot_motor_random_build(self):
        self.robot.__init__()
        print("robot rebuild")
        motor = mootor_data()
        # print(motor.TECO_member.head())
        # print(motor.TECO_member.groupby("rated_torque").mean())
        print(
            pd.concat(
                [
                    motor.TECO_member,
                    motor.Kollmorgen_member,
                    motor.UR_member,
                    motor.TM_member,
                ],
                axis=0,
            )
        )

        res = motor.TECO_member.append(other=motor.Kollmorgen_member, ignore_index=True)
        print(res)

        res = motor.TECO_member.append(
            [motor.Kollmorgen_member, motor.UR_member, motor.TM_member],
            ignore_index=True,
        )
        print(res)

        self.robot.plot(self.qn)



    def optimal_design_callback(self, data):
        # print(data.data)
        self.op_payload = data.payload
        self.op_payload_position = data.payload_position
        self.op_vel = data.vel
        self.op_acc = data.acc
        self.op_radius = data.radius

        rospy.loginfo("I heard op_payload is %s", self.op_payload)
        rospy.loginfo("I heard op_payload_position is %s", self.op_payload_position)
        rospy.loginfo("I heard op_vel is %s", self.op_vel)
        rospy.loginfo("I heard op_acc is %s", self.op_acc)
        rospy.loginfo("I heard op_radius is %s", self.op_radius)

        # print(self.optimal_design_flag)

    def optimal_random_callback(self, data):
        self.op_axis_2_length = data.axis_2_length
        self.op_axis_3_length = data.axis_3_length

        rospy.loginfo("I heard op_axis_2_length is %s", self.op_axis_2_length)
        rospy.loginfo("I heard op_axis_3_length is %s", self.op_axis_3_length)

    # TODO: optimization_algorithm: use Random forest
    def optimization_algorithm(self):
        # input data: random axis2,3 length, robot workspace, robot payload, robot joint velocity, robot joint acceleration, motor data
        """
        Agent :
            robot payload set
            robot velocity
            robot acceleration

        Action :
            axis 2 length increase
            axis 2 length reduce
            axis 3 length increase
            axis 3 length reduce
            Change the motor configuration of each axis

        Rewards :
            torque
            motor cost
            robot workspace
            robot weight

        Status :
            After the parameter of action is changed, the torque value of each axis
        """

        """ transfer the data to the dataframe
        agent:
            self.op_payload
            self.op_payload_position
            self.op_vel
            self.op_acc
            self.op_radius
        """
        # TODO: axis2,3 length change
        """ receive the data from the topic
        action:
            axis 2 length increase
            axis 2 length reduce
            axis 3 length increase
            axis 3 length reduce
            Change the motor configuration of each axis
        """
        # TODO: rebuild robot
        self.robot_motor_random_build()
        # update dynamics torque calculation parameters
        self.payload = self.op_payload
        self.payload_position = self.op_payload_position
        self.vel = self.op_vel
        self.acc = self.op_acc
        # calculate the robotic arm workspace
        self.Workspace_cal_Monte_Carlo()
        # Compare ideal radius with the workspace radius
        print("T_x:", self.T_x[0, :].max() - self.T_x[0, :].min())
        print("T_y:", self.T_y[0, :].max() - self.T_y[0, :].min())
        print("T_z:", self.T_z[0, :].max() - self.T_z[0, :].min())
        radius_max = self.T_x[0, :].max() - self.T_x[0, :].min()
        radius_reward = self.op_radius - radius_max
        # TODO: before reward
        # output data: robot torque, robot module, motor select
        # TODO: use dynamics to calculate torque
        self.dynamics_torque_limit()
        """ transfer the data to the topic
        rewards:
            torque : Use torque reduction
            motor cost
            robot workspace
            robot weight
        """
        # Use torque reduction, motor score (the higher the cost, the lower the score),
        # Motor score (the higher the cost, the lower the score)
        # Scope of work (the larger the scope of work, the higher the score)
        """ transfer the data to the topic
        state:
        After the parameter of action is changed, the torque value of each axis
        """
        # TODO: through optimization algorithm to find the best solution

if __name__ == "__main__":
    rospy.init_node("optimization")

    drl = drl_optimization()
    while not rospy.is_shutdown():
        pass