#cython: language_level=3
import sys 
import numpy as np
import roboticstoolbox as rtb
from spatialmath import *
from math import pi
import matplotlib.pyplot as plt
from matplotlib import cm
import argparse
import time
np.set_printoptions(linewidth=100, formatter={'float': lambda x: f"{x:8.4g}" if abs(x) > 1e-10 else f"{0:8.4g}"})


def dyna_space_cal(robot, payload_space, payload_postition,q1_s,q1_end,q2_s,q2_end,q3_s,q3_end,q4_s,q4_end,q5_s,q5_end):
    # 計算參數
    step= 20 #計算步距 % 解析度   # original = 20
    # t=0:1:(q5_end-q5_s)/step # 產生時間向量 
    step1 = (q1_end - q1_s)/step 
    step2 = (q2_end - q2_s)/step 
    step3 = (q3_end - q3_s)/step 
    step4 = (q4_end - q4_s)/step 
    step5 = (q5_end - q5_s)/step
    step6 = (q6_end - q6_s)/step 
    step_num = int(step1*step2*step3*step4*step5)
    T_cell=step1*step2*step3*step4*step5
    T = np.zeros((3,1))
    T_x = np.zeros((1,step_num))
    T_y = np.zeros((1,step_num))
    T_z = np.zeros((1,step_num))
    qd = np.r_[0, 1, 0, 0, 0, 0]
    robot.coriolis(robot.qn, qd) 
    # TODO:  rne 逆動力學 add vel & acc analyses
    robot.rne(robot.qn, np.zeros((6,)), np.zeros((6,)))
    # 窮舉法正運動學計算工作空間
    start = time.time()
    print("The time used to execute this is given below")
    i = 0
    # 角度轉換
    du=pi/180;  #度
    radian=180/pi; #弧度

    fig = plt.figure()
    ax = plt.subplot(111, projection='3d')


    robot.payload(payload_space, payload_position_space) # set payload 

    for q1 in range(q1_s, q1_end, step):
        for q2 in range(q2_s, q2_end, step):
            percent = i/T_cell*100
            print("percent:{:.0f}%".format(percent), end="\r")
            for q3 in range(q3_s, q3_end, step):
                for q4 in range(q4_s, q4_end, step):
                    for q5 in range(q5_s, q5_end, step):
                        T = robot.fkine([q1*du, q2*du, q3*du, q4*du, q5*du, 0*du])
                        load = np.array([robot.gravload([q1*du, q2*du, q3*du, q4*du, q5*du, 0*du])])
                        torque = np.append(torque,load,axis=0)
                        T_x[0,i] = T.t[0]
                        T_y[0,i] = T.t[1]
                        T_z[0,i] = T.t[2]
                        i=i+1
                        
    end = time.time()
    print("繪製工作空間運行時間：%f sec" % (end - start))
