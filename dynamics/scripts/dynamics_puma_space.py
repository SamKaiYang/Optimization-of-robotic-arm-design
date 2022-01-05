#!/usr/bin/env python3
# coding: utf-8
import rospy
import numpy as np
import roboticstoolbox as rtb
from spatialmath import *
from math import pi
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import time
np.set_printoptions(linewidth=100, formatter={'float': lambda x: f"{x:8.4g}" if abs(x) > 1e-10 else f"{0:8.4g}"})



class Dynamics_space():
    def __init__(self):
        self.p560 = rtb.models.DH.Puma560()
        # self.p560.plot(self.p560.qn, block=False)
        self.p560.gravload(self.p560.qn)
        self.p560.inertia(self.p560.qn)
        self.torque = np.array([np.zeros(shape=6)])
        ## 數值法 求取工作空間
        # 關節角限位
        self.q1_s=-160
        self.q1_end=160
        self.q2_s=-160
        self.q2_end=160
        self.q3_s=-160
        self.q3_end=160
        self.q4_s=-160
        self.q4_end=160
        self.q5_s=-160
        self.q5_end=160
        self.q6_s=-160
        self.q6_end=160
        # 計算參數
        self.step=40 #計算步距 % 解析度   # original = 20
        # t=0:1:(q5_end-q5_s)/step # 產生時間向量 
        step1 = (self.q1_end - self.q1_s)/self.step 
        step2 = (self.q2_end - self.q2_s)/self.step 
        step3 = (self.q3_end - self.q3_s)/self.step 
        step4 = (self.q4_end - self.q4_s)/self.step 
        step5 = (self.q5_end - self.q5_s)/self.step
        step6 = (self.q6_end - self.q6_s)/self.step 
        self.step_num = int(step1*step2*step3*step4*step5)
        self.T_cell=step1*step2*step3*step4*step5
        self.T = np.zeros((3,1))
        self.T_x = np.zeros((1,self.step_num))
        self.T_y = np.zeros((1,self.step_num))
        self.T_z = np.zeros((1,self.step_num))
        
        N = 100
        (Q2, Q3) = np.meshgrid(np.linspace(-pi, pi, N), np.linspace(-pi, pi, N))
        M11 = np.zeros((N,N))
        M12 = np.zeros((N,N))
        for i in range(N):
            for j in range(N):
                M = self.p560.inertia(np.r_[0, Q2[i,j], Q3[i,j], 0, 0, 0])
                M11[i,j] = M[0,0]
                M12[i,j] = M[0,1]

    def payload_set(self):
        self.p560.payload(20, [0, 0, 0]) # set payload 

# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# surf = ax.plot_surface(Q2, Q3, M11, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# fig.colorbar(surf, shrink=0.9, aspect=10, pad=0.12)
# ax.set_xlabel('$q_2$ (rad)')
# ax.set_ylabel('$q_3$ (rad)')
# ax.set_zlabel('$M_{11}$ ($kg.m^2$)')
# plt.show()

# M11.max() / M11.min()

# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# surf = ax.plot_surface(Q2, Q3, M12, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# fig.colorbar(surf, shrink=0.9, aspect=10, pad=0.12)
# ax.set_xlabel('$q_2$ (rad)')
# ax.set_ylabel('$q_3$ (rad)')
# ax.set_zlabel('$M_{12}$ ($kg.m^2$)')
# plt.show()
    def dynamics_cal(self):
        qd = np.r_[0, 1, 0, 0, 0, 0]
        # print("qd:",qd)
        self.p560.coriolis(self.p560.qn, qd) @ qd
        self.p560.rne(self.p560.qn, np.zeros((6,)), np.zeros((6,)))
        # 窮舉法正運動學計算工作空間
        start = time.time()
        print("The time used to execute this is given below")
        i = 0
        # 角度轉換
        du=pi/180;  #度
        radian=180/pi; #弧度

        fig = plt.figure()
        self.ax = plt.subplot(111, projection='3d')

        self.p560.payload(20, [0, 0, 1]) # set payload 

        for q1 in range(self.q1_s, self.q1_end, self.step):
            for q2 in range(self.q2_s, self.q2_end, self.step):
                percent = i/self.T_cell*100
                print("percent:{:.0f}%".format(percent), end="\r")
                for q3 in range(self.q3_s, self.q3_end, self.step):
                    for q4 in range(self.q4_s, self.q4_end, self.step):
                        for q5 in range(self.q5_s, self.q5_end, self.step):
                            self.T = self.p560.fkine([q1*du, q2*du, q3*du, q4*du, q5*du, 0*du])
                            load = np.array([self.p560.gravload([q1*du, q2*du, q3*du, q4*du, q5*du, 0*du])])
                            self.torque = np.append(self.torque,load,axis=0)
                            self.T_x[0,i] = self.T.t[0]
                            self.T_y[0,i] = self.T.t[1]
                            self.T_z[0,i] = self.T.t[2]
                            i=i+1
                            
        end = time.time()
        print("繪製工作空間運行時間：%f sec" % (end - start))
        
    def plot_space_scan(self):
        self.ax.scatter(self.T_x[0,:], self.T_y[0,:], self.T_z[0,:], c='r', marker='o')

        # # 顯示圖例
        # ax.legend()
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y") 
        self.ax.set_zlabel("z")
        # 顯示圖形
        plt.show()
        plt.pause(0)

    def sol_output(self):
        print(self.torque)
        print("torque type:",type(self.torque))
        print("torque size:",len(self.torque))

        print("軸1 torque正最大值:",np.max(self.torque[:,0]))
        print("軸2 torque正最大值:",np.max(self.torque[:,1]))
        print("軸3 torque正最大值:",np.max(self.torque[:,2]))
        print("軸4 torque正最大值:",np.max(self.torque[:,3]))
        print("軸5 torque正最大值:",np.max(self.torque[:,4]))
        print("軸6 torque正最大值:",np.max(self.torque[:,5]))

        print("軸1 torque負最大值:",np.min(self.torque[:,0]))
        print("軸2 torque負最大值:",np.min(self.torque[:,1]))
        print("軸3 torque負最大值:",np.min(self.torque[:,2]))
        print("軸4 torque負最大值:",np.min(self.torque[:,3]))
        print("軸5 torque負最大值:",np.min(self.torque[:,4]))
        print("軸6 torque負最大值:",np.min(self.torque[:,5]))

        print("軸2 torque正最大值時, 各軸torque, 末端位置, 各軸角度")
        torque_where = np.where(self.torque==np.max(self.torque[:,1]))
        for i in range(len(torque_where[0])):
            print(torque_where[0][i])
            max_torque = torque_where[0][i]
            print("torque:",self.torque[max_torque])
            print("末端位置",[self.T_x[0,i], self.T_y[0,i], self.T_z[0,i]])
            # TODO: 求解逆運動學 各軸角度self.p560.ikine_a()
            self.T.t[0] = self.T_x[0,i]
            self.T.t[1] = self.T_y[0,i]
            self.T.t[2] = self.T_z[0,i]
            sol = self.p560.ikine_a(self.T, "lun")
            print("sol:",sol)
            self.p560.plot(sol.q, dt=0.1 )
            # plt.show()

    def sol_output_axis(self,axis):
        axis = axis-1
        print("軸%d torque正最大值:%f" %(axis, np.max(self.torque[:,axis])))
        print("軸%d torque負最大值:%f" %(axis, np.min(self.torque[:,axis])))

        print("軸%d torque正最大值時, 各軸torque, 末端位置, 各軸角度" %(axis+1))
        torque_where = np.where(self.torque==np.max(self.torque[:,axis]))
        for i in range(len(torque_where[0])):
            print(torque_where[0][i])
            max_torque = torque_where[0][i]
            print("torque:",self.torque[max_torque])
            print("末端位置",[self.T_x[0,i], self.T_y[0,i], self.T_z[0,i]])
            # TODO: 求解逆運動學 各軸角度self.p560.ikine_a()
            self.T.t[0] = self.T_x[0,i]
            self.T.t[1] = self.T_y[0,i]
            self.T.t[2] = self.T_z[0,i]
            sol = self.p560.ikine_a(self.T, "lun")
            print("sol:",sol)
            self.p560.plot(sol.q, dt=0.1 )

        print("軸%d torque負最大值時, 各軸torque, 末端位置, 各軸角度" %(axis+1))
        torque_where = np.where(self.torque==np.min(self.torque[:,axis]))
        for i in range(len(torque_where[0])):
            print(torque_where[0][i])
            max_torque = torque_where[0][i]
            print("torque:",self.torque[max_torque])
            print("末端位置",[self.T_x[0,i], self.T_y[0,i], self.T_z[0,i]])
            # TODO: 求解逆運動學 各軸角度self.p560.ikine_a()
            self.T.t[0] = self.T_x[0,i]
            self.T.t[1] = self.T_y[0,i]
            self.T.t[2] = self.T_z[0,i]
            sol = self.p560.ikine_a(self.T, "lun")
            print("sol:",sol)
            self.p560.plot(sol.q, dt=0.1 )


if __name__=="__main__":
    rospy.init_node("dynamics_space")

    Dya = Dynamics_space()
    # tra.init()
    Dya.payload_set()
    Dya.dynamics_cal()
    # Dya.sol_output()
    Dya.sol_output_axis(2)
    Dya.plot_space_scan() 
    