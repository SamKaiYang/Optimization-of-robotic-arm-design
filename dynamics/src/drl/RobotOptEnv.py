#!/usr/bin/env python3
# coding: utf-8
import gym
from gym import spaces
import numpy as np
from math import pi

from sympy import false
# from torch import R

from dynamics.arm_workspace import arm_workspace_plane
# from robot_urdf import RandomRobot
from dynamics.motor_module import mootor_data
from dynamics.random_robot import RandomRobot
from dynamics.stl_conv_6dof_urdf import stl_conv_urdf
import rospy
# TODO: 整合機器人重製生成 與 動力學計算
# TODO: 初版 只考慮 6 dof 機器人的關節長度變化, 觀察各軸馬達極限之輸出最大torque值
class RobotOptEnv(gym.Env):
    """
    ### Description
    This environment corresponds to the version of the cart-pole problem described by Barto, Sutton, and Anderson in
    ["Neuronlike Adaptive Elements That Can Solve Difficult Learning Control Problem"](https://ieeexplore.ieee.org/document/6313077).
    A pole is attached by an un-actuated joint to a cart, which moves along a frictionless track.
    The pendulum is placed upright on the cart and the goal is to balance the pole by applying forces
     in the left and right direction on the cart.
    ### Action Space
    The action is a `ndarray` with shape `(1,)` which can take values `{0, 1}` indicating the direction
     of the fixed force the cart is pushed with.
    | Num | Action                 |
    |-----|------------------------|
    | 0   | length add 1 cm  |
    | 1   | length del 1 cm |
    **Note**: The velocity that is reduced or increased by the applied force is not fixed and it depends on the angle
     the pole is pointing. The center of gravity of the pole varies the amount of energy needed to move the cart underneath it
    ### Observation Space
    The observation is a `ndarray` with shape `(4,)` with the values corresponding to the following positions and velocities:
    | Num | Observation           | Min                 | Max               |
    |-----|-----------------------|---------------------|-------------------|
    | 0   | Cart Position         | -4.8                | 4.8               |
    | 1   | Cart Velocity         | -Inf                | Inf               |
    | 2   | Pole Angle            | ~ -0.418 rad (-24°) | ~ 0.418 rad (24°) |
    | 3   | Pole Angular Velocity | -Inf                | Inf               |
    **Note:** While the ranges above denote the possible values for observation space of each element,
        it is not reflective of the allowed values of the state space in an unterminated episode. Particularly:
    -  The cart x-position (index 0) can be take values between `(-4.8, 4.8)`, but the episode terminates
       if the cart leaves the `(-2.4, 2.4)` range.
    -  The pole angle can be observed between  `(-.418, .418)` radians (or **±24°**), but the episode terminates
       if the pole angle is not in the range `(-.2095, .2095)` (or **±12°**)
    ### Rewards
    Since the goal is to keep the pole upright for as long as possible, a reward of `+1` for every step taken,
    including the termination step, is allotted. The threshold for rewards is 475 for v1.
    ### Starting State
    All observations are assigned a uniformly random value in `(-0.05, 0.05)`
    ### Episode End
    The episode ends if any one of the following occurs:
    1. Termination: Pole Angle is greater than ±12°
    2. Termination: Cart Position is greater than ±2.4 (center of the cart reaches the edge of the display)
    3. Truncation: Episode length is greater than 500 (200 for v0)
    """

    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 2
    }
    def __init__(self):
        self.robot = RandomRobot()
        self.robot_urdf = stl_conv_urdf("random","test")
        self.payload = 5.0
        self.payload_position = np.array([0, 0, 0.04])
        self.vel = np.array([2.356194, 2.356194, 2.356194, 2.356194, 2.356194, 2.356194])
        self.acc = np.array([2.356194, 2.356194, 2.356194, 2.356194, 2.356194, 2.356194])
        self.std_L2 = 35 # 預設標準值 第二軸 35 cm
        self.std_L3 = 35 # 預設標準值 第三軸 35 cm
        self.high_torque = 120.0 # 預設標準值 馬達極限 120.0 N max
        self.low_torque = 70.0 # 預設標準值 馬達極限 60.0 N rated
        self.done = np.array([false, false, false, false, false, false])
        high = np.array([self.high_torque], dtype=np.float32)
        # TODO: action space for length change
        self.action_space = spaces.Discrete(5) # 0, 1: 不动，長度增加，長度減少
        # TODO: observation space for torque, motor cost, workspace, weight
        # self.observation_space = spaces.Box(low=-high, high=high, dtype=np.float32)
        self.observation_space = spaces.Box(np.array([self.low_torque,self.low_torque,self.low_torque,self.low_torque,self.low_torque,self.low_torque]), 
                                            np.array([self.high_torque,self.high_torque,self.high_torque,self.high_torque,self.high_torque,self.high_torque]), 
                                            dtype=np.float32)
        self.state = None
    
    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        state_torque = self.state 
        if action == 0: # 不改變
            state_torque = state_torque
        if action == 1: # 加長 第二軸
            self.std_L2 += 1
            self.robot_urdf.specified_generate_write_urdf(self.std_L2, self.std_L3)
            self.robot.__init__() # 重製機器人
            torque = self.dynamics_torque_limit()
            state_torque = torque
        if action == 2: # 縮短 第二軸
            self.std_L2 -= 1
            self.robot_urdf.specified_generate_write_urdf(self.std_L2, self.std_L3)
            self.robot.__init__() # 重製機器人
            torque = self.dynamics_torque_limit()
            state_torque = torque
        if action == 3: # 加長 第三軸
            self.std_L3 += 1
            self.robot_urdf.specified_generate_write_urdf(self.std_L2, self.std_L3)
            self.robot.__init__() # 重製機器人
            torque = self.dynamics_torque_limit()
            state_torque = torque
        if action == 4: # 縮短 第三軸
            self.std_L3 -= 1
            self.robot_urdf.specified_generate_write_urdf(self.std_L2, self.std_L3)
            self.robot.__init__() # 重製機器人
            torque = self.dynamics_torque_limit()
            state_torque = torque

        self.state = state_torque # 1*6 array
        self.counts += 1
        
        # TODO: 設定 reward
        # if down 完成任务 
        # 終止條件: 趨近於各軸馬達最小torque 範圍 or 超出各軸馬達最大torque 範圍 
        for i in range(6):
            if np.abs(state_torque[i]) < self.low_torque or np.abs(state_torque[i]) > self.high_torque:
                self.done[i] = True # 已經完成任務
            else:
                self.done[i] = False

        # TODO: 陣列搜索
        # 如果所有軸已經完成任務，則結束
        false_done = False in self.done 
        # result = np.where(self.done == True)
        # 走一步修正, 但還未最佳化完成
        if false_done:
            reward = -1.0
        # down 完成後, 定義所計算出的torque值, 分數加多少
        else:
            reward = 0
            rospy.loginfo("fffffffffffffffffuuuuuuuuuuuuuuuuuuuuuuuucccccccccccccccccccccckkkkkkkkkkkkkkkkkkkkk")
            for i in range(6):
                # 趨近於各軸馬達 rated torque 範圍
                if np.abs(state_torque[i]) <= self.low_torque:
                    reward += 10.0
                # 即torque, 超過最大torque 
                elif np.abs(state_torque[i]) > self.high_torque:
                    reward += -30.0
                else:
                    reward += 0.0
        done = not false_done # 取bool 反向值
        return self.state, reward, done, {}

    # reset环境状态 
    def reset(self):
        self.robot_urdf.opt_generate_write_urdf() # 啟用標準的L2,L3長度urdf
        self.robot.__init__() # 重製機器人
        torque = self.dynamics_torque_limit()
        self.state = torque
        self.counts = 0
        return self.state    
    
    # 視覺化呈現，它只會回應出呼叫那一刻的畫面給你，要它持續出現，需要寫個迴圈
    def render(self, mode='human'):
        return None
        
    def close(self):
        return None
        
    def dynamics_torque_limit(self):
        """
        Calculate the maximum torque required by

        each axis when the arm of each axis is the longest and the acceleration is the highest
        """
        torque = np.array([np.zeros(shape=6)])
        # axis_angle = np.array([np.zeros(shape=6)])
        axis_angle = []
        append_torque_limit_list = []
        temp_torque_max = []
        temp_torque_min = []
        Torque_Max = []
        # 角度轉換
        du = pi / 180
        # 度
        # radian = 180 / pi
        # 弧度
        self.robot.payload(self.payload, self.payload_position)  # set payload
        torque = np.array([np.zeros(shape=6)])
        q_list = [0, 90, -90, 180, -180]
        T_cell = (
            len(q_list)
            * len(q_list)
            * len(q_list)
            * len(q_list)
            * len(q_list)
            * len(q_list)
        )
        # T = np.zeros((3, 1))
        # T_x = np.zeros(T_cell)
        # T_y = np.zeros(T_cell)
        # T_z = np.zeros(T_cell)

        for i in range(len(q_list)):
            q1 = q_list[i]
            percent = i / T_cell * 100
            for j in range(len(q_list)):
                q2 = q_list[j]
                for k in range(len(q_list)):
                    q3 = q_list[k]
                    for l in range(len(q_list)):
                        q4 = q_list[l]
                        for m in range(len(q_list)):
                            q5 = q_list[m]
                            for n in range(len(q_list)):
                                q6 = q_list[n]
                                axis_angle.append([q1, q2, q3, q4, q5, q6])
                                load = np.array(
                                    [
                                        self.robot.rne(
                                            [
                                                q1 * du,
                                                q2 * du,
                                                q3 * du,
                                                q4 * du,
                                                q5 * du,
                                                q6 * du,
                                            ],
                                            self.vel,
                                            self.acc
                                        )
                                    ]
                                )
                                torque = np.append(torque, load, axis=0)

        for i in range(6):
            axis = i
            toque_max_index = np.argmax(torque[:, axis])
            toque_min_index = np.argmin(torque[:, axis])

            temp_torque_max = torque[toque_max_index].tolist()
            temp_torque_max.extend(axis_angle[toque_max_index])
            temp_torque_min = torque[toque_min_index].tolist()
            temp_torque_min.extend(axis_angle[toque_min_index])
            append_torque_limit_list.append(temp_torque_max)
            append_torque_limit_list.append(temp_torque_min)
            Torque_Max.append(abs(torque[toque_max_index][i]))
            self.torque_dynamics_limit = Torque_Max


        # print("torque_dynamics_limit: ", self.torque_dynamics_limit)
        return self.torque_dynamics_limit

if __name__ == '__main__':
    env = RobotOptEnv()
    
    # env.dynamics_torque_limit()
    env.reset()
    env.step(env.action_space.sample())
    print(env.state)
    env.step(env.action_space.sample())
    print(env.state)
