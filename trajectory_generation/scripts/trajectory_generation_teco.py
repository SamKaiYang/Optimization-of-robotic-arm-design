#!/usr/bin/env python3
# coding: utf-8
import rospy
import roboticstoolbox as rtb
from spatialmath import *   # lgtm [py/polluting-import]
import argparse
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

class Trajectory_generation():
    def __init__(self):
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

        self.qt = None
        self.interval = range(200)
        
    def trajectory_planning(self):
        print(self.robot)
        self.qt = rtb.tools.trajectory.jtraj(self.robot.qz, self.robot.qr, 200)
    def trajectory_plot(self):
        # 軌跡規劃後的各軸角度
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
        # rtb.tools.trajectory.plot()
        # tg = rtb.tools.trajectory.lspb(robot.qz[0], robot.qr[0], 200)

        # t = rtb.tools.trajectory.lspb(robot.qz[1], robot.qr[1], 50)
        # t.plot()
        self.robot.plot(self.qt.q, backend=self.args.backend)

if __name__=="__main__":
    rospy.init_node("trajectory_generation")

    tra = Trajectory_generation()
    # tra.init()

    tra.trajectory_planning()
    tra.trajectory_plot()
    tra.trajectory_planning_plot()
    # while not rospy.is_shutdown():
    #     nex.arm_task_sub()
    #     pass