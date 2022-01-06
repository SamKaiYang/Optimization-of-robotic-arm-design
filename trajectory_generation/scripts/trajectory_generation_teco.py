#!/usr/bin/env python3
# coding: utf-8
import rospy
import numpy as np
import roboticstoolbox as rtb
from spatialmath import *   # lgtm [py/polluting-import]
import argparse
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class Trajectory_generation():
    def __init__(self):
        self.qt = None
        self.interval = range(200)

        self.t = np.arange(0, 2, 0.010)
        self.T0 = SE3(-0.494, -0.045, 0.259)
        self.T1 = SE3(0.4, 0.5, 0.2)
        print(self.T0)
        print(self.T1)
        self.Tc = None

        parser = argparse.ArgumentParser(description="Puma trajectory demo")
        parser.add_argument(
            '--backend',
            '-b',
            dest='backend',
            default='pyplot',
            help='choose backend: pyplot (default), swift, vpython',
            action='store')
        parser.add_argument(
            '--model',
            '-m',
            dest='model',
            default='DH',
            action='store',
            help='choose model: DH (default), URDF')
        self.args = parser.parse_args()

        if self.args.model.lower() == 'dh':
            self.robot = rtb.models.DH.Puma560()
        elif self.args.model.lower() == 'urdf':
            self.robot = rtb.models.URDF.Puma560()
        else:
            raise ValueError('unknown model')

        

    def trajectory_planning(self, space):
        print(self.robot)
        if space == "ctraj":
            self.T0 = self.robot.fkine(self.robot.qz)
            self.T1 = self.robot.fkine(self.robot.qr)
            # self.T0 = SE3(-0.494, -0.045, 0.259)
            # self.T1 = SE3(0.452, -0.572, 0.798)
            print(self.T0)
            print(self.T1)

            self.Tc = rtb.tools.trajectory.ctraj(self.T0, self.T1, self.t)
            sol = self.robot.ikine_LM(self.Tc, mask = [1, 1, 1, 1, 0, 1])
            print(sol.q)
            print(sol.q.shape)
            
            self.robot.plot(sol.q, backend=self.args.backend)
            plt.pause(0)

        elif space == "jtraj":
            self.qt = rtb.tools.trajectory.jtraj(self.robot.qz, self.robot.qr, 200)
            
            self.trajectory_planning_plot()
            self.trajectory_plot()

            # TODO:  rne 逆動力學 add vel & acc analyses
            torque = self.robot.rne(self.qt.q, self.qt.qd, self.qt.qdd)
            fig = plt.figure()
            plt.plot(self.interval, torque[:,0], 'r-')
            plt.plot(self.interval, torque[:,1], 'b--')
            plt.plot(self.interval, torque[:,2], 'g-.')
            plt.plot(self.interval, torque[:,3], 'c-')
            plt.plot(self.interval, torque[:,4], 'k--')
            plt.plot(self.interval, torque[:,5], 'm-')
            plt.legend(['torque0','torque1','torque2','torque3','torque4','torque5'])
            plt.show()
            plt.pause(0)

    def trajectory_plot(self):
        # 軌跡規劃後的各軸角度
        fig = plt.figure()
        plt.subplot(221)
        plt.plot(self.interval, self.qt.q[:,0], 'r-')
        plt.plot(self.interval, self.qt.q[:,1], 'b--')
        plt.plot(self.interval, self.qt.q[:,2], 'g-.')
        plt.plot(self.interval, self.qt.q[:,3], 'c-')
        plt.plot(self.interval, self.qt.q[:,4], 'k--')
        plt.plot(self.interval, self.qt.q[:,5], 'm-')
        plt.legend(['q0','q1','q2','q3','q4','q5'])
        # 軌跡規劃後的各軸速度
        plt.subplot(222)
        plt.plot(self.interval, self.qt.qd[:,0], 'r-')
        plt.plot(self.interval, self.qt.qd[:,1], 'b--')
        plt.plot(self.interval, self.qt.qd[:,2], 'g-.')
        plt.plot(self.interval, self.qt.qd[:,3], 'c-')
        plt.plot(self.interval, self.qt.qd[:,4], 'k--')
        plt.plot(self.interval, self.qt.qd[:,5], 'm-')
        plt.legend(['qd0','qd1','qd2','qd3','qd4','qd5'])
        # 軌跡規劃後的各軸加速度
        plt.subplot(212)
        plt.plot(self.interval, self.qt.qdd[:,0], 'r-')
        plt.plot(self.interval, self.qt.qdd[:,1], 'b--')
        plt.plot(self.interval, self.qt.qdd[:,2], 'g-.')
        plt.plot(self.interval, self.qt.qdd[:,3], 'c-')
        plt.plot(self.interval, self.qt.qdd[:,4], 'k--')
        plt.plot(self.interval, self.qt.qdd[:,5], 'm-')
        plt.legend(['qdd0','qdd1','qdd2','qdd3','qdd4','qdd5'])
        plt.show()

    def trajectory_planning_plot(self):
        if self.args.backend.lower() == 'pyplot':
            if self.args.model.lower() != 'dh':
                print('PyPlot only supports DH models for now')
                sys.exit(1)
        elif self.args.backend.lower() == 'vpython':
            if self.args.model.lower() != 'dh':
                print('VPython only supports DH models for now')
                sys.exit(1)
        elif self.args.backend.lower() == 'swift':
            if self.args.model.lower() != 'urdf':
                print('Swift only supports URDF models for now')
                sys.exit(1)
        else:
            raise ValueError('unknown backend')

        self.robot.plot(self.qt.q, backend=self.args.backend, block=False, movie="trajectory_generation.gif", vellipse=False, fellipse=False)
        plt.show()

if __name__=="__main__":
    rospy.init_node("trajectory_generation")
    tra = Trajectory_generation()
    tra.trajectory_planning("jtraj")
    tra.trajectory_planning("ctraj")

    # while not rospy.is_shutdown():
    #     nex.arm_task_sub()
    #     pass