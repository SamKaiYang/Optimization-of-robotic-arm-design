import roboticstoolbox as rtb
from spatialmath import *   # lgtm [py/polluting-import]
import argparse
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Puma trajectory demo")
parser.add_argument(
    '--backend',
    '-b',
    dest='backend',
    default='pyplot',
    help='choose backend: pyplot (default), swift, vpython',
    action='store')
parser.add_argument(
    '--model',
    '-m',
    dest='model',
    default='DH',
    action='store',
    help='choose model: DH (default), URDF')
args = parser.parse_args()

if args.model.lower() == 'dh':
    robot = rtb.models.DH.Puma560()
elif args.model.lower() == 'urdf':
    robot = rtb.models.URDF.Puma560()
else:
    raise ValueError('unknown model')

print(robot)
interval = range(200)
qt = rtb.tools.trajectory.jtraj(robot.qz, robot.qr, 200)
# print(qt.qdd)
# rtb.tools.trajectory.qplot(qt.q)

# 'b' as blue

# 'g' as green

# 'r' as red

# 'c' as cyan

# 'm' as magenta

# 'y' as yellow

# 'k' as black

# 'w' as white
# linestyle=['-', '--', ':', '-.']
# 軌跡規劃後的各軸角度
plt.subplot(221)
# plt.scatter(interval, qt.q[:,0], 'r-', alpha=0.5,
#             label='r-')
plt.plot(interval, qt.q[:,0], 'r-')
plt.plot(interval, qt.q[:,1], 'b--')
plt.plot(interval, qt.q[:,2], 'g-.')
plt.plot(interval, qt.q[:,3], 'c-')
plt.plot(interval, qt.q[:,4], 'k--')
plt.plot(interval, qt.q[:,5], 'm-')
# plt.show()
plt.legend(['q0','q1','q2','q3','q4','q5'])
# 軌跡規劃後的各軸速度
plt.subplot(222)
plt.plot(interval, qt.qd[:,0], 'r-')
plt.plot(interval, qt.qd[:,1], 'b--')
plt.plot(interval, qt.qd[:,2], 'g-.')
plt.plot(interval, qt.qd[:,3], 'c-')
plt.plot(interval, qt.qd[:,4], 'k--')
plt.plot(interval, qt.qd[:,5], 'm-')
plt.legend(['qd0','qd1','qd2','qd3','qd4','qd5'])
# plt.show()
# 軌跡規劃後的各軸加速度
plt.subplot(212)
plt.plot(interval, qt.qdd[:,0], 'r-')
plt.plot(interval, qt.qdd[:,1], 'b--')
plt.plot(interval, qt.qdd[:,2], 'g-.')
plt.plot(interval, qt.qdd[:,3], 'c-')
plt.plot(interval, qt.qdd[:,4], 'k--')
plt.plot(interval, qt.qdd[:,5], 'm-')
plt.legend(['qdd0','qdd1','qdd2','qdd3','qdd4','qdd5'])
plt.show()

if args.backend.lower() == 'pyplot':
    if args.model.lower() != 'dh':
        print('PyPlot only supports DH models for now')
        sys.exit(1)
elif args.backend.lower() == 'vpython':
    if args.model.lower() != 'dh':
        print('VPython only supports DH models for now')
        sys.exit(1)
elif args.backend.lower() == 'swift':
    if args.model.lower() != 'urdf':
        print('Swift only supports URDF models for now')
        sys.exit(1)
else:
    raise ValueError('unknown backend')
# rtb.tools.trajectory.plot()
# tg = rtb.tools.trajectory.lspb(robot.qz[0], robot.qr[0], 200)

# t = rtb.tools.trajectory.lspb(robot.qz[1], robot.qr[1], 50)
# t.plot()
robot.plot(qt.q, backend=args.backend)
