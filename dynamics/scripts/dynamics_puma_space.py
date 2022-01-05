#!/usr/bin/env python3
# coding: utf-8

# In[1]:


import numpy as np
import roboticstoolbox as rtb
from spatialmath import *
from math import pi
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import time
np.set_printoptions(linewidth=100, formatter={'float': lambda x: f"{x:8.4g}" if abs(x) > 1e-10 else f"{0:8.4g}"})

p560 = rtb.models.DH.Puma560()

# p560.plot(p560.qn, block=False)

p560.gravload(p560.qn)

p560.inertia(p560.qn)

N = 100
(Q2, Q3) = np.meshgrid(np.linspace(-pi, pi, N), np.linspace(-pi, pi, N))
M11 = np.zeros((N,N))
M12 = np.zeros((N,N))
for i in range(N):
    for j in range(N):
        M = p560.inertia(np.r_[0, Q2[i,j], Q3[i,j], 0, 0, 0])
        M11[i,j] = M[0,0]
        M12[i,j] = M[0,1]

p560.payload(20, [0, 0, 0]) # set payload 

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


qd = np.r_[0, 1, 0, 0, 0, 0]
# print("qd:",qd)
p560.coriolis(p560.qn, qd) @ qd

p560.rne(p560.qn, np.zeros((6,)), np.zeros((6,)))

# 角度轉換
du=pi/180;  #度
radian=180/pi; #弧度
## 數值法 求取工作空間
# 關節角限位
q1_s=-160
q1_end=160
q2_s=-160
q2_end=160
q3_s=-160
q3_end=160
q4_s=-160
q4_end=160
q5_s=-160
q5_end=160
q6_s=-160
q6_end=160

# 計算參數
step=40 #計算步距 % 解析度   # original = 20
# t=0:1:(q5_end-q5_s)/step # 產生時間向量 
step1 = (q1_end - q1_s)/step 
step2 = (q2_end - q2_s)/step 
step3 = (q3_end - q3_s)/step 
step4 = (q4_end - q4_s)/step 
step5 = (q5_end - q5_s)/step
step6 = (q6_end - q6_s)/step 

T_cell=step1*step2*step3*step4*step5
# 窮舉法正運動學計算工作空間
start = time.time()

print("The time used to execute this is given below")

torque = np.array([np.zeros(shape=6)])
i = 0
T = np.zeros((3,1))
step_num = int(step1*step2*step3*step4*step5)
T_x = np.zeros((1,step_num))
T_y = np.zeros((1,step_num))
T_z = np.zeros((1,step_num))

fig = plt.figure()
ax = plt.subplot(111, projection='3d')

p560.payload(20, [0, 0, 1]) # set payload 

for q1 in range(q1_s, q1_end, step):
    for q2 in range(q2_s, q2_end, step):
        percent = i/T_cell*100
        print("percent:{:.0f}%".format(percent), end="\r")
        for q3 in range(q3_s, q3_end, step):
            for q4 in range(q4_s, q4_end, step):
                for q5 in range(q5_s, q5_end, step):
                    T = p560.fkine([q1*du, q2*du, q3*du, q4*du, q5*du, 0*du])
                    load = np.array([p560.gravload([q1*du, q2*du, q3*du, q4*du, q5*du, 0*du])])
                    torque = np.append(torque,load,axis=0)
                    T_x[0,i] = T.t[0]
                    T_y[0,i] = T.t[1]
                    T_z[0,i] = T.t[2]
                    i=i+1
                    
end = time.time()
print("繪製工作空間運行時間：%f sec" % (end - start))

print(torque)
print("torque type:",type(torque))
print("torque size:",len(torque))

print("軸1 torque正最大值:",np.max(torque[:,0]))
print("軸2 torque正最大值:",np.max(torque[:,1]))
print("軸3 torque正最大值:",np.max(torque[:,2]))
print("軸4 torque正最大值:",np.max(torque[:,3]))
print("軸5 torque正最大值:",np.max(torque[:,4]))
print("軸6 torque正最大值:",np.max(torque[:,5]))

print("軸1 torque負最大值:",np.min(torque[:,0]))
print("軸2 torque負最大值:",np.min(torque[:,1]))
print("軸3 torque負最大值:",np.min(torque[:,2]))
print("軸4 torque負最大值:",np.min(torque[:,3]))
print("軸5 torque負最大值:",np.min(torque[:,4]))
print("軸6 torque負最大值:",np.min(torque[:,5]))

print("軸2 torque正最大值時, 各軸torque, 末端位置, 各軸角度")
torque_where = np.where(torque==np.max(torque[:,1]))
for i in range(len(torque_where[0])):
    print(torque_where[0][i])
    max_torque = torque_where[0][i]
    print("torque:",torque[max_torque])
    print("末端位置",[T_x[0,i], T_y[0,i], T_z[0,i]])
    # TODO: 求解逆運動學 各軸角度p560.ikine_a()

ax.scatter(T_x[0,:], T_y[0,:], T_z[0,:], c='r', marker='o')

# # 顯示圖例
# ax.legend()
ax.set_xlabel("x")
ax.set_ylabel("y") 
ax.set_zlabel("z")
# 顯示圖形
plt.show()
plt.pause(0)