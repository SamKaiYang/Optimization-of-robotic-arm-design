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

from dynamics.arm_workspace import arm_workspace_plane
# from robot_urdf import RandomRobot
from dynamics.motor_module import mootor_data
from dynamics.random_robot import RandomRobot

# DRL_optimization api
import sys,os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
curr_path = os.path.dirname(os.path.abspath(__file__)) # 当前文件所在绝对路径
parent_path = os.path.dirname(curr_path) # 父路径
sys.path.append(parent_path) # 添加路径到系统路径sys.path

import datetime
import gym
import torch

from env import NormalizedActions,OUNoise
from ddpg import DDPG
from common.utils import save_results,make_dir
from common.utils import plot_rewards

import matplotlib.pyplot as plt
from RobotOptEnv import RobotOptEnv

curr_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")  # 获取当前时间

class drl_optimization:
    def __init__(self):
        self.test = 0
        self.robot = RandomRobot()
        # callback:Enter the parameters of the algorithm to be optimized on the interface
        self.sub_optimal_design = rospy.Subscriber(
            "/optimal_design", optimal_design, self.optimal_design_callback
        )
        # callback:Randomly generated shaft length due to optimization algorithm
        # self.sub_optimal_random = rospy.Subscriber(
        #     "/optimal_random", optimal_random, self.optimal_random_callback
        # )

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

        # res = motor.TECO_member.append(other=motor.Kollmorgen_member, ignore_index=True)
        # print(res)

        # res = motor.TECO_member.append(
        #     [motor.Kollmorgen_member, motor.UR_member, motor.TM_member],
        #     ignore_index=True,
        # )
        # print(res)

        # self.robot.plot(self.qn)

    def env_agent_config(self, cfg, seed=1):
        # original
        # env = NormalizedActions(gym.make(cfg.env_name)) # 装饰action噪声
        # add create new env
        env = NormalizedActions(RobotOptEnv()) # 傳輸目標設計參數
        # env = Car2DEnv()
        env.seed(seed) # 随机种子
        n_states = env.observation_space.shape[0]
        n_actions = env.action_space.shape[0]
        agent = DDPG(n_states,n_actions,cfg)
        return env,agent
    
    def train(self, cfg, env, agent):
        print('开始训练！')
        print(f'环境：{cfg.env_name}，算法：{cfg.algo_name}，设备：{cfg.device}')
        ou_noise = OUNoise(env.action_space)  # 动作噪声
        rewards = [] # 记录所有回合的奖励
        ma_rewards = []  # 记录所有回合的滑动平均奖励
        for i_ep in range(cfg.train_eps):
            state = env.reset()
            ou_noise.reset()
            done = False
            ep_reward = 0
            i_step = 0
            while not done:
                # env.render()
                i_step += 1
                action = agent.choose_action(state)
                # print(action)
                action = ou_noise.get_action(action, i_step) 
                next_state, reward, done, _ = env.step(action)
                ep_reward += reward
                agent.memory.push(state, action, reward, next_state, done)
                agent.update()
                state = next_state
                
            if (i_ep+1)%10 == 0:
                print('回合：{}/{}，奖励：{:.2f}'.format(i_ep+1, cfg.train_eps, ep_reward))
            rewards.append(ep_reward)
            if ma_rewards:
                ma_rewards.append(0.9*ma_rewards[-1]+0.1*ep_reward)
            else:
                ma_rewards.append(ep_reward)
        print('完成训练！')
        return rewards, ma_rewards

    def test(self, cfg, env, agent):
        print('开始测试！')
        print(f'环境：{cfg.env_name}, 算法：{cfg.algo_name}, 设备：{cfg.device}')
        rewards = [] # 记录所有回合的奖励
        ma_rewards = []  # 记录所有回合的滑动平均奖励
        for i_ep in range(cfg.test_eps):
            state = env.reset() 
            done = False
            ep_reward = 0
            i_step = 0
            while not done:
                env.render()
                i_step += 1
                action = agent.choose_action(state)
                next_state, reward, done, _ = env.step(action)
                ep_reward += reward
                state = next_state
                # print(action)
            print('回合：{}/{}, 奖励：{}'.format(i_ep+1, cfg.train_eps, ep_reward))
            rewards.append(ep_reward)
            if ma_rewards:
                ma_rewards.append(0.9*ma_rewards[-1]+0.1*ep_reward)
            else:
                ma_rewards.append(ep_reward)
            print(f"回合：{i_ep+1}/{cfg.test_eps}，奖励：{ep_reward:.1f}")
        print('完成测试！')
        return rewards, ma_rewards


    def optimal_design_callback(self, data):
        # print(data.data)
        # TODO: 目標構型
        self.op_dof = data.dof
        self.op_payload = data.payload
        self.op_payload_position = data.payload_position
        self.op_vel = data.vel
        self.op_acc = data.acc
        self.op_radius = data.radius
        

        rospy.loginfo("I heard op_dof is %s", self.op_dof)
        rospy.loginfo("I heard op_payload is %s", self.op_payload)
        rospy.loginfo("I heard op_payload_position is %s", self.op_payload_position)
        rospy.loginfo("I heard op_vel is %s", self.op_vel)
        rospy.loginfo("I heard op_acc is %s", self.op_acc)
        rospy.loginfo("I heard op_radius is %s", self.op_radius)


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
        
        # cal max torque
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


class Config:
    '''超参数
    '''

    def __init__(self):
        ################################## 环境超参数 ###################################
        self.algo_name = 'DDPG'  # 算法名称
        self.env_name = 'Pendulum-v0'  # 环境名称，gym新版本（约0.21.0之后）中Pendulum-v0改为Pendulum-v1
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")  # 检测GPUgjgjlkhfsf风刀霜的撒发十
        self.seed = 10 # 随机种子，置0则不设置随机种子
        self.train_eps = 300 # 训练的回合数
        self.test_eps = 20 # 测试的回合数
        ################################################################################
        
        ################################## 算法超参数 ###################################
        self.gamma = 0.99 # 折扣因子
        self.critic_lr = 1e-3 # 评论家网络的学习率
        self.actor_lr = 1e-4 # 演员网络的学习率
        self.memory_capacity = 8000 # 经验回放的容量
        self.batch_size = 128 # mini-batch SGD中的批量大小
        self.target_update = 2 # 目标网络的更新频率
        self.hidden_dim = 256 # 网络隐藏层维度
        self.soft_tau = 1e-2 # 软更新参数
        ################################################################################
        
        ################################# 保存结果相关参数 ################################
        self.result_path = curr_path + "/outputs/" + self.env_name + \
            '/' + curr_time + '/results/'  # 保存结果的路径
        self.model_path = curr_path + "/outputs/" + self.env_name + \
            '/' + curr_time + '/models/'  # 保存模型的路径
        self.save = True # 是否保存图片
        ################################################################################
        # self.result_path = curr_path + "/outputs/" + self.env_name + \
        #     '/' + '20220712-085524' + '/results/'  # 保存结果的路径
        # self.model_path = curr_path + "/outputs/" + self.env_name + \
        #     '/' + '20220712-085524' + '/models/'  # 保存模型的路径
        # self.save = True # 是否保存图片
        



if __name__ == "__main__":
    rospy.init_node("optimization")
    a = 0
    drl = drl_optimization()
    while not rospy.is_shutdown():
        if a == 1:
            cfg = Config()
            # 训练
            env,agent = drl.env_agent_config(cfg,seed=1)
            rewards, ma_rewards = drl.train(cfg, env, agent)
            make_dir(cfg.result_path, cfg.model_path)
            agent.save(path=cfg.model_path)
            save_results(rewards, ma_rewards, tag='train', path=cfg.result_path)
            plot_rewards(rewards, ma_rewards, cfg, tag="train")  # 画出结果
            # 测试
            env,agent = drl.env_agent_config(cfg,seed=10)
            agent.load(path=cfg.model_path)
            rewards,ma_rewards = drl.test(cfg,env,agent)
            save_results(rewards,ma_rewards,tag = 'test',path = cfg.result_path)
            plot_rewards(rewards, ma_rewards, cfg, tag="test")  # 画出结果
            break
        else:
            pass