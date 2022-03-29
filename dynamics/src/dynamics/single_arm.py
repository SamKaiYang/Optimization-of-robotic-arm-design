#!/usr/bin/env python3
import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
from spatialmath import SE3
from urdf_parser_py.urdf import URDF
import os


class single_arm(DHRobot):
    """
    Class that models a TECO TECOARM1 manipulator

    :param symbolic: use symbolic constants
    :type symbolic: bool

    describes its kinematic and dynamic characteristics using standard DH
    conventions.

    .. runblock:: pycon

        >>> import roboticstoolbox as rtb
        >>> robot = rtb.models.DH.TECOARM1()
        >>> print(robot)

    Defined joint configurations are:

    - qz, zero joint angle configuration
    - qr, arm horizontal along x-axis

    .. note::
        - SI units are used.

    :References:

    .. codeauthor:: Yi He Yang
    """  # noqa

    def __init__(self, symbolic=False):
        path = os.path.dirname(os.path.realpath(__file__))+"/single_arm.urdf"
        print(path)
        robot = URDF.from_xml_file(path)
        if symbolic:
            import spatialmath.base.symbolic as sym
            zero = sym.zero()
            pi = sym.pi()
        else:
            from math import pi
            zero = 0.0

        deg = pi / 180
        inch = 0.0254

        # robot length values (metres)
        # a = [0, -0.314, -0.284, 0, 0, 0] #m # teco
        a = [0, -robot.joints[3].origin.xyz[1], -robot.joints[4].origin.xyz[1], 0, 0, 0]
        # a = [0, -j3.y, -j4.y, 0, 0, 0]
        # d = [0.1301, 0, 0, 0.1145, 0.090, 0.048] #m # teco 
        d = [robot.joints[1].origin.xyz[2],
            0,
            0,
            robot.joints[2].origin.xyz[1]-robot.joints[4].origin.xyz[2], 
            robot.joints[5].origin.xyz[2],
            robot.joints[6].origin.xyz[2]
        ]
        # d = [j1.z, 0, 0, j2.y-j4.z , j5.z, j6.z] #m
        alpha = [pi/2, zero, zero, pi/2, -pi/2, zero]

        
        # mass data, no inertia available
        # mass = [3.7000, 8.3930, 2.33, 1.2190, 1.2190, 0.1897]
        mass = [robot.links[2].inertial.mass, 
                robot.links[3].inertial.mass,
                robot.links[4].inertial.mass,
                robot.links[5].inertial.mass,
                robot.links[6].inertial.mass,
                robot.links[7].inertial.mass
            ]
        
        G= [-80,-80,-80,-50,-50,-50]   # gear ratio

        # center_of_mass = [
        #         [-1.55579201081481E-05, 0.00265005484815443, -0.00640979059142413],
        #         [4.90637956589368E-11, 0.205571973027702, -0.003359898058563426],
        #         [-9.75479428030767E-05, 0.271025707847572, 0.111573843205116],
        #         [-0.000181761828397664, 0.00219045749084071, -0.000800397394362884],
        #         [-0.000192919655058627, -0.00232492307126431, 0.00352418959262345],
        #         [-4.4856E-13 ,0 ,0.025]
        #     ]

        center_of_mass = [
                robot.links[2].inertial.origin.xyz,
                robot.links[3].inertial.origin.xyz,
                robot.links[4].inertial.origin.xyz,
                robot.links[5].inertial.origin.xyz,
                robot.links[6].inertial.origin.xyz,
                robot.links[7].inertial.origin.xyz
            ]

        links = []

        for j in range(6):
            link = RevoluteDH(
                d=d[j],
                a=a[j],
                alpha=alpha[j],
                m=mass[j],
                r=center_of_mass[j],
                G=G[j]
            )
            links.append(link)
    
        super().__init__(
            links,
            name="robot",
            manufacturer="Robotics",
            keywords=('dynamics', 'symbolic'),
            symbolic=symbolic
        )
    
        # zero angles
        self.addconfiguration("qz", np.array([0, 0, 0, 0, 0, 0]))
        # horizontal along the x-axis
        self.addconfiguration("qr", np.r_[180, 0, 0, 0, 90, 0]*deg)

        # nominal table top picking pose
        self.addconfiguration("qn", np.array([0, 0, 0, 0, 0, 0]))
if __name__ == '__main__':    # pragma nocover

    robot = single_arm(symbolic=False)
    print(robot)
    print(robot.dynamics())
