"""Predefined robot models.

These models correspond to the Modified Denavit–Hartenberg parameters:
https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters
"""
import numpy as np  # type: ignore


def kuka_lbr_iiwa_7() -> np.ndarray:  # pragma: no cover
    """Get KUKA LBR iiwa 7 MDH model."""
    return np.array(
        [
            [0, 0, 0, 340],
            [-np.pi / 2, 0, 0, 0],
            [np.pi / 2, 0, 0, 400],
            [np.pi / 2, 0, 0, 0],
            [-np.pi / 2, 0, 0, 400],
            [-np.pi / 2, 0, 0, 0],
            [np.pi / 2, 0, 0, 126],
        ]
    )


def mecademic_meca500() -> np.ndarray:  # pragma: no cover
    """Get Meca500 MDH model."""
    return np.array(
        [
            [0, 0, 0, 135],
            [-np.pi / 2, 0, -np.pi / 2, 0],
            [0, 135, 0, 0],
            [-np.pi / 2, 38, 0, 120],
            [np.pi / 2, 0, 0, 0],
            [-np.pi / 2, 0, np.pi, 72],
        ]
    )


def puma560() -> np.ndarray:  # pragma: no cover
    """Get PUMA560 MDH model."""
    return np.array(
        [
            [0, 0, 0, 0],
            [-np.pi / 2, 0, 0, 0],
            [0, 612.7, 0, 0],
            [0, 571.6, 0, 163.9],
            [-np.pi / 2, 0, 0, 115.7],
            [np.pi / 2, 0, np.pi, 92.2],
        ]
    )


def ur10() -> np.ndarray:  # pragma: no cover
    """Get UR10 MDH model."""
    return np.array(
        [

        #  alpha   a  theta    d               
            [0, 0, 0, 118],
            [np.pi / 2, 0, np.pi, 0],
            [0, 612.7, 0, 0],
            [0, 571.6, 0, 163.9],
            [-np.pi / 2, 0, 0, 115.7],
            [np.pi / 2, 0, np.pi, 92.2],
        ]
    )


def abb_irb120() -> np.ndarray:  # pragma: no cover
    """Get ABB irb120 MDH model."""
    return np.array(
        [
            [0, 0, 0, 290],
            [-np.pi / 2, 0, -np.pi / 2, 0],
            [0, 270, 0, 0],
            [-np.pi / 2, 70, 0, 302],
            [np.pi / 2, 0, 0, 0],
            [-np.pi / 2, 0, np.pi, 72],
        ]
    )

def teco() -> np.ndarray:  # pragma: no cover
    """Get teco MDH model."""
    return np.array(
        [

            #  alpha   a        theta     d 
            [np.pi/2,  0,      0,     89.16],
            [0,        425,    0,     0],
            [0,        392.25, 0,     0],
            [np.pi/2,  0,      0,     109.15],
            [-np.pi/2, 0,      0,     94.56],
            [0,        0,      0,     82.3],

            #          theta    d         a        alpha     offset
            # L1=Link([0       0.08916    0        pi/2      0     ],'standard'); 
            # L2=Link([0       0        0.425     0         0     ],'standard');
            # L3=Link([0       0        0.39225   0         0     ],'standard');
            # L4=Link([0       0.10915   0        pi/2      0     ],'standard');
            # L5=Link([0       0.09456    0        -pi/2     0     ],'standard');
            # L6=Link([0       0.0823     0        0         0     ],'standard');
        ]
    )
