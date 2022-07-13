#!/usr/bin/env python3
# coding: utf-8
"""
Created on 20220713

@author: Yang Yi He
"""

import gym
from gym import spaces
import numpy as np

from dynamics.arm_workspace import arm_workspace_plane
# from robot_urdf import RandomRobot
from dynamics.motor_module import mootor_data
from dynamics.random_robot import RandomRobot

# TODO: 整合機器人重製生成 與 動力學計算
class RobotOptEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 2
    }
    def __init__(self):
        self.robot = RandomRobot()
        self.xth = 0
        self.target_x = 0
        self.target_y = 0
        self.L = 10
        self.actionL = 0
        self.actionH = 50
        # self.action_space = spaces.Box(np.array([self.actionL, self.actionL]), np.array([self.actionH, self.actionH])) # 0, 1, 2，3，4: 不动，上下左右
        # TODO: continuous action space for length change
        self.action_space = spaces.Box(
                low=self.actionL, high=self.actionH, shape=(1,), dtype=np.float32)
        # TODO: observation space for torque, motor cost, workspace, weight
        self.observation_space = spaces.Box(np.array([np.float32(-self.L), np.float32(-self.L)]), np.array([np.float32(self.L), np.float32(self.L)]))
        self.state = None
    
    def step(self, action):
        # assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        # action axis length change && motor module change
        x, y = self.state
        if action <= 0 and action < 1:
            x = x
            y = y
        if action <= 1 and action <2:
            x = x
            y = y + 1
        if action <= 2 and action <3:
            x = x
            y = y - 1
        if action <= 3 and action <4:
            x = x - 1
            y = y
        if action <= 4 and action <5:
            x = x + 1
            y = y
        self.state = np.array([x, y])
        self.counts += 1
        
        # if down 完成任务 
        done = (np.abs(x)+np.abs(y) <= 1) or (np.abs(x)+np.abs(y) >= 2*self.L+1)
        done = bool(done)
        
        # 走一步修正, 但還未最佳化完成
        if not done:
            reward = -0.1
        # down 完成後, 定義所計算出的torque值, 分數加多少
        else:
            if np.abs(x)+np.abs(y) <= 1:
                reward = 10
            # 即torque, 超過最大torque 
            else:
                reward = -50
            
        return self.state, reward, done, {}
    
    def reset(self):
        self.robot.__init__() # 重製機器人
        # self.state 觀測 torque, motor cost, workspace, weight
        # torque state
        torque = self.dynamics_torque_limit()
        
        # self.state = np.ceil(np.random.rand(2)*2*self.L)-self.L # 動力學 推導torque
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
        radian = 180 / pi
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
        T = np.zeros((3, 1))
        T_x = np.zeros(T_cell)
        T_y = np.zeros(T_cell)
        T_z = np.zeros(T_cell)

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
                                            self.acc,
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

        return self.torque_dynamics_limit

if __name__ == '__main__':
    env = RobotOptEnv()
    # env.reset()
    # env.step(env.action_space.sample())
    # print(env.state)
    # env.step(env.action_space.sample())
    # print(env.state)
