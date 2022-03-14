#!/usr/bin/env python3

import numpy as np
from roboticstoolbox.robot.ERobot import ERobot
from urdf_parser_py.urdf import URDF
import os

class RandomRobot(ERobot):
    """
    Class that imports a UR5 URDF model

    ``UR3()`` is a class which imports a Universal Robotics UR5 robot
    definition from a URDF file.  The model describes its kinematic and
    graphical characteristics.

    .. runblock:: pycon

        >>> import roboticstoolbox as rtb
        >>> robot = rtb.models.URDF.UR5()
        >>> print(robot)

    Defined joint configurations are:

    - qz, zero joint angle configuration, 'L' shaped configuration
    - qr, vertical 'READY' configuration

    .. codeauthor:: Jesse Haviland
    .. sectionauthor:: Peter Corke
    """

    def __init__(self):

        links, name, urdf_string, urdf_filepath = self.URDF_read(
            os.path.dirname(os.path.realpath(__file__))+"/tecobot.urdf"
        )

        super().__init__(
            links,
            name=name.upper(),
            manufacturer="RandomRobot",
            # gripper_links=links[7],
            urdf_string=urdf_string,
            urdf_filepath=urdf_filepath,
        )

        self.addconfiguration("qz", np.array([0, 0, 0, 0, 0, 0]))
        self.addconfiguration("qr", np.array([np.pi, 0, 0, 0, np.pi / 2, 0]))


        
        # sol=robot.ikine_LM(SE3(0.5, -0.2, 0.2)@SE3.OA([1,0,0],[0,0,-1]))
        # self.addconfiguration(
        #     "qn",
        #     np.array(
        #         [
        #             -7.052413e-01,
        #             3.604328e-01,
        #             -1.494176e00,
        #             1.133744e00,
        #             -7.052413e-01,
        #             0,
        #         ]
        #     ),
        # )
        self.addconfiguration("qn", np.array([0, 0, 0, 0, 0, 0]))


if __name__ == "__main__":  # pragma nocover
    print(os.path.dirname(os.path.realpath(__file__)))
    robot = RandomRobot()
    # print("==========================================================")
    # print(robot.links[0:1])
    # print("==========================================================")
    # print(robot.links[1:2])
    # # TODO: 刪除dummy, base link link.m & r 
    # print("==========================================================")
    # print(robot.links)
    # # print("==========================================================")
    # # print(robot.name)
    # # print("==========================================================")
    # # print(robot.urdf_string)
    # # print("==========================================================")
    # # print(robot.urdf_filepath)
    # print("==========================================================")
    # print(robot)
    # print("==========================================================")
    # print(robot.ets())
    robot = URDF.from_xml_file(os.path.dirname(os.path.realpath(__file__))+"/tecobot.urdf")
    print(robot)
    print("==========================================================")
    # print(robot.joints[0].name)
    # print("==========================================================")
    # print(robot.joints[0].limit)
    # print("==========================================================")
    # print(robot.joints[0].origin.xyz)
    print("==========================================================")
    print(robot.joints[1].name)
    print("==========================================================")
    print(robot.joints[1].limit)
    print("==========================================================")
    print(robot.joints[1].origin.xyz)
    print("==========================================================")
    print(robot.joints[2].name)
    print("==========================================================")
    print(robot.joints[2].limit)
    print("==========================================================")
    print(robot.joints[2].origin.xyz)
    print("==========================================================")
    print(robot.joints[3].name)
    print("==========================================================")
    print(robot.joints[3].limit)
    print("=========================================================")
    print(robot.joints[3].origin.xyz)
    print("==========================================================")
    print(robot.joints[4].name)
    print("==========================================================")
    print(robot.joints[4].limit)
    print("==========================================================")
    print(robot.joints[4].origin.xyz)
    print("==========================================================")
    print(robot.joints[5].name)
    print("==========================================================")
    print(robot.joints[5].limit)
    print("==========================================================")
    print(robot.joints[5].origin.xyz)
    print("==========================================================")
    print(robot.joints[6].name)
    print("==========================================================")
    print(robot.joints[6].limit)
    print("==========================================================")
    print(robot.joints[6].origin.xyz)
    # print(robot.joints[2].name)
    # print(robot.joints[2].name)