import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
from spatialmath import SE3

# TODO:fixed TM robot data 
class TM5_700(DHRobot):
    """
    Class that models a Techman Robot TM5 700 manipulator

    :param symbolic: use symbolic constants
    :type symbolic: bool

    - qz, zero joint angle configuration
    - qr, arm horizontal along x-axis

    .. note::
        - SI units are used.

    .. codeauthor:: Yi He Yang
    """

    def __init__(self, symbolic=False):

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
        a = [0, -0.42500, -0.39225, 0, 0, 0]
        d = [0.089459, 0, 0, 0.10915, 0.09465, 0.0823]

        alpha = [pi/2, zero, zero, pi/2, -pi/2, zero]

        # mass data, no inertia available
        mass = [3.7000, 8.3930, 2.33, 1.2190, 1.2190, 0.1897]
        center_of_mass = [
                [0,     -0.02561,  0.00193],
                [0.2125, 0,        0.11336],
                [0.15,   0,        0.0265],
                [0,     -0.0018,   0.01634],
                [0,     -0.0018,   0.01634],
                [0,      0,       -0.001159]
            ]
        links = []

        for j in range(6):
            link = RevoluteDH(
                d=d[j],
                a=a[j],
                alpha=alpha[j],
                m=mass[j],
                r=center_of_mass[j],
                G=1
            )
            links.append(link)
    
        super().__init__(
            links,
            name="TM5_700",
            manufacturer="Techman Robot",
            keywords=('dynamics', 'symbolic'),
            symbolic=symbolic
        )
    
        # zero angles
        self.addconfiguration("qz", np.array([0, 0, 0, 0, 0, 0]))
        # horizontal along the x-axis
        self.addconfiguration("qr", np.r_[180, 0, 0, 0, 90, 0]*deg)

        # nominal table top picking pose
        self.addconfiguration("qn", np.array([0, 0, 0, 0, 0, 0]))

class TM5_900(DHRobot):
    """
    Class that models a Techman Robot TM5 900 manipulator

    :param symbolic: use symbolic constants
    :type symbolic: bool

    - qz, zero joint angle configuration
    - qr, arm horizontal along x-axis

    .. note::
        - SI units are used.

    .. codeauthor:: Yi He Yang
    """
    def __init__(self, symbolic=False):

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
        a = [0, -0.42500, -0.39225, 0, 0, 0]
        d = [0.089459, 0, 0, 0.10915, 0.09465, 0.0823]

        alpha = [pi/2, zero, zero, pi/2, -pi/2, zero]

        # mass data, no inertia available
        mass = [3.7000, 8.3930, 2.33, 1.2190, 1.2190, 0.1897]
        center_of_mass = [
                [0,     -0.02561,  0.00193],
                [0.2125, 0,        0.11336],
                [0.15,   0,        0.0265],
                [0,     -0.0018,   0.01634],
                [0,     -0.0018,   0.01634],
                [0,      0,       -0.001159]
            ]
        links = []

        for j in range(6):
            link = RevoluteDH(
                d=d[j],
                a=a[j],
                alpha=alpha[j],
                m=mass[j],
                r=center_of_mass[j],
                G=1
            )
            links.append(link)
        super().__init__(
            links,
            name="TM5_900",
            manufacturer="Techman Robot",
            keywords=('dynamics', 'symbolic'),
            symbolic=symbolic
        )
    
        # zero angles
        self.addconfiguration("qz", np.array([0, 0, 0, 0, 0, 0]))
        # horizontal along the x-axis
        self.addconfiguration("qr", np.r_[180, 0, 0, 0, 90, 0]*deg)

        # nominal table top picking pose
        self.addconfiguration("qn", np.array([0, 0, 0, 0, 0, 0]))

class TM12(DHRobot):
    """
    Class that models a Techman Robot TM12 manipulator

    :param symbolic: use symbolic constants
    :type symbolic: bool

    - qz, zero joint angle configuration
    - qr, arm horizontal along x-axis

    .. note::
        - SI units are used.

    .. codeauthor:: Yi He Yang
    """
    def __init__(self, symbolic=False):

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
        a = [0, -0.42500, -0.39225, 0, 0, 0]
        d = [0.089459, 0, 0, 0.10915, 0.09465, 0.0823]

        alpha = [pi/2, zero, zero, pi/2, -pi/2, zero]

        # mass data, no inertia available
        mass = [3.7000, 8.3930, 2.33, 1.2190, 1.2190, 0.1897]
        center_of_mass = [
                [0,     -0.02561,  0.00193],
                [0.2125, 0,        0.11336],
                [0.15,   0,        0.0265],
                [0,     -0.0018,   0.01634],
                [0,     -0.0018,   0.01634],
                [0,      0,       -0.001159]
            ]
        links = []

        for j in range(6):
            link = RevoluteDH(
                d=d[j],
                a=a[j],
                alpha=alpha[j],
                m=mass[j],
                r=center_of_mass[j],
                G=1
            )
            links.append(link)
        super().__init__(
            links,
            name="TM12",
            manufacturer="Techman Robot",
            keywords=('dynamics', 'symbolic'),
            symbolic=symbolic
        )
    
        # zero angles
        self.addconfiguration("qz", np.array([0, 0, 0, 0, 0, 0]))
        # horizontal along the x-axis
        self.addconfiguration("qr", np.r_[180, 0, 0, 0, 90, 0]*deg)

        # nominal table top picking pose
        self.addconfiguration("qn", np.array([0, 0, 0, 0, 0, 0]))

class TM14(DHRobot):
    """
    Class that models a Techman Robot TM14 manipulator

    :param symbolic: use symbolic constants
    :type symbolic: bool

    - qz, zero joint angle configuration
    - qr, arm horizontal along x-axis

    .. note::
        - SI units are used.

    .. codeauthor:: Yi He Yang
    """
    def __init__(self, symbolic=False):

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
        a = [0, -0.42500, -0.39225, 0, 0, 0]
        d = [0.089459, 0, 0, 0.10915, 0.09465, 0.0823]

        alpha = [pi/2, zero, zero, pi/2, -pi/2, zero]

        # mass data, no inertia available
        mass = [3.7000, 8.3930, 2.33, 1.2190, 1.2190, 0.1897]
        center_of_mass = [
                [0,     -0.02561,  0.00193],
                [0.2125, 0,        0.11336],
                [0.15,   0,        0.0265],
                [0,     -0.0018,   0.01634],
                [0,     -0.0018,   0.01634],
                [0,      0,       -0.001159]
            ]
        links = []

        for j in range(6):
            link = RevoluteDH(
                d=d[j],
                a=a[j],
                alpha=alpha[j],
                m=mass[j],
                r=center_of_mass[j],
                G=1
            )
            links.append(link)
        super().__init__(
            links,
            name="TM14",
            manufacturer="Techman Robot",
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

    TM5 = TM5_700(symbolic=False)
    print(TM5_700)
    # print(TM5.dyntable())
