#The code pulls the data points from the Wspace_mod function, with inputs
#here on Link lengths and respective joint actuation domains. The output
#array from Wspace_mod is an array CA contatining workspace span coordinates
#at the input resolution and the column vector maxmin containing the boundary
#coordinates of the span which is then simulated with the joints in the
#code below.

#Personally, I would recommend utilising resolutions in the range of 10<res<30.
#Any more will absolutely work at the cost of more
#time, but this code hasn't been designed for that degree of analysis and
#just for mere eye leve observation. Please do feel free to contact me with
#doubts or errors at "jeano5326@gmail.com" I will be more than glad to
#hear any input on these.
#Coded in/for MATLAB R2021a

# https://www.linkedin.com/in/jeanojoseph/
# https://www.behance.net/jeanojoseph
# https://github.com/jeanbuntu
# @ - jeano5326@gmail.com

##
#constant inputs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import math
from scipy.spatial import Delaunay
import alphashape
from shapely.ops import cascaded_union, polygonize
import shapely.geometry as geometry


fig, ax = plt.subplots(2,figsize=(10,10))
# ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1))

def alpha_shape(points, alpha, only_outer=True):
    """
    Compute the alpha shape (concave hull) of a set of points.
    :param points: np.array of shape (n,2) points.
    :param alpha: alpha value.
    :param only_outer: boolean value to specify if we keep only the outer border
    or also inner edges.
    :return: set of (i,j) pairs representing edges of the alpha-shape. (i,j) are
    the indices in the points array.
    """
    assert points.shape[0] > 3, "Need at least four points"

    def add_edge(edges, i, j):
        """
        Add an edge between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            assert (j, i) in edges, "Can't go twice over same directed edge right?"
            if only_outer:
                # if both neighboring triangles are in shape, it's not a boundary edge
                edges.remove((j, i))
            return
        edges.add((i, j))

    tri = Delaunay(points)
    edges = set()
    # Loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.vertices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]
        # Computing radius of triangle circumcircle
        # www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
        a = np.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
        b = np.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
        c = np.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)
        s = (a + b + c) / 2.0
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        circum_r = a * b * c / (4.0 * area)
        if circum_r < alpha:
            add_edge(edges, ia, ib)
            add_edge(edges, ib, ic)
            add_edge(edges, ic, ia)
    return edges

def find_edges_with(i, edge_set):
    i_first = [j for (x,j) in edge_set if x==i]
    i_second = [j for (j,x) in edge_set if x==i]
    return i_first,i_second

def stitch_boundaries(edges):
    edge_set = edges.copy()
    boundary_lst = []
    while len(edge_set) > 0:
        boundary = []
        edge0 = edge_set.pop()
        boundary.append(edge0)
        last_edge = edge0
        while len(edge_set) > 0:
            i,j = last_edge
            j_first, j_second = find_edges_with(j, edge_set)
            if j_first:
                edge_set.remove((j, j_first[0]))
                edge_with_j = (j, j_first[0])
                boundary.append(edge_with_j)
                last_edge = edge_with_j
            elif j_second:
                edge_set.remove((j_second[0], j))
                edge_with_j = (j, j_second[0])  # flip edge rep
                boundary.append(edge_with_j)
                last_edge = edge_with_j

            if edge0[0] == last_edge[1]:
                break

        boundary_lst.append(boundary)
    return boundary_lst

def Wspace_mod(A_arr = None,theta_arr = None,res = None): 
    ##
    aone = A_arr[0]
    a2 = A_arr[1]
    a3 = A_arr[2]
    ##
    numPt = res
    numPt_3 = numPt * numPt * numPt
    ##
    q1 = np.linspace(theta_arr[0],theta_arr[1],numPt)
    
    q2 = np.linspace(theta_arr[2],theta_arr[3],numPt)
    
    q3 = np.linspace(theta_arr[4],theta_arr[5],numPt)
    
    #declaring array size for final storage before push
    x_stor = np.ones((1,numPt_3))
    y_stor = np.ones((1,numPt_3))
    angle_stor = np.ones((numPt_3,3))
    storage_i = 0
    for i in np.arange(0,numPt).reshape(-1):
        for j in np.arange(0,numPt).reshape(-1):
            for k in np.arange(0,numPt).reshape(-1):
    
                #X,Y coordinates calculated by the projections of the
    #instantaneous joint positions for respective angles.
                xcord = aone * math.cos(q1[i]) + a2 * math.cos(q1[i] + q2[j]) + a3 * math.cos(q1[i] + q2[j] + q3[k])
                ycord = aone * math.sin(q1[i]) + a2 * math.sin(q1[i] + q2[j]) + a3 * math.sin(q1[i] + q2[j] + q3[k])
                x_stor[0][storage_i] = xcord
                y_stor[0][storage_i] = ycord
                angle_stor[storage_i,:] = np.array([q1[i],q2[j],q3[k]])
                #columns 3,4 and 5.
                storage_i = storage_i + 1
    xytheta_arr1 = np.stack((np.transpose(x_stor[0]),np.transpose(y_stor[0])),axis = 1)
    xytheta_arr = np.concatenate((xytheta_arr1,angle_stor),axis = 1)
    # TODO: fixed the shape issue

    # TODO: fixed the boundary issue
    points = np.vstack([xytheta_arr[:,0],xytheta_arr[:,1]]).T
    edges = alpha_shape(points, alpha=0.05)
    k = stitch_boundaries(edges)
    ax[0].plot(xytheta_arr[:,1],xytheta_arr[:,0],'c.')
    for i, j in edges:
        ax[0].plot(points[[i, j], 1], points[[i, j], 0], linewidth=3)

    return xytheta_arr,edges



def xy_Wspace_mod(A_arr = None,theta_arr = None,res = None): 
    ##
    aone = A_arr[0]
    ##
    numPt = res
    ##
    q1 = np.linspace(theta_arr[0],theta_arr[1],numPt)

    #declaring array size for final storage before push
    x_stor = np.ones((1,numPt))
    y_stor = np.ones((1,numPt))
    angle_stor = np.ones((numPt,3))
    storage_i = 0
    for i in np.arange(0,numPt).reshape(-1):
        xcord = aone * math.cos(q1[i])
        ycord = aone * math.sin(q1[i])
        x_stor[0][storage_i] = xcord
        y_stor[0][storage_i] = ycord
        angle_stor[storage_i,:] = np.array([q1[i]])
        #columns 3,4 and 5.
        storage_i = storage_i + 1
    xytheta_arr1 = np.stack((np.transpose(x_stor[0]),np.transpose(y_stor[0])),axis = 1)
    xytheta_arr = np.concatenate((xytheta_arr1,angle_stor),axis = 1)
    # TODO: fixed the shape issue

    # TODO: fixed the boundary issue
    points = np.vstack([xytheta_arr[:,0],xytheta_arr[:,1]]).T
    edges = alpha_shape(points, alpha=0.05)
    k = stitch_boundaries(edges)
    ax[1].plot(xytheta_arr[:,1],xytheta_arr[:,0],'c.')

    p1 = [xytheta_arr[len(xytheta_arr[:,1])-1,1],xytheta_arr[len(xytheta_arr[:,0])-1,0]]
    p2 = [xytheta_arr[0,1], xytheta_arr[0,0]]
    p3 = [0,0]
    ax[1].plot([p1[0],p3[0]],[p1[1],p3[1]],'c', linewidth=3)
    ax[1].plot([p2[0],p3[0]],[p2[1],p3[1]],'c', linewidth=3)

    # ax.plot(p1, p3, 'r-', 
    #         p2, p3, 'b-',  linewidth=3, 
    #         animated=False) #animated is associated with blit
    
    # for i, j in edges:
    #     ax.plot(points[[i, j], 1], points[[i, j], 0], linewidth=3)
    #     print("i:", i)
    #     print("j:", j)
    return xytheta_arr,edges

rse = 15

Ang_arr = np.array([- math.pi * 125 / 180, math.pi * 85 / 180, -math.pi * 145 / 180, math.pi * 95 / 180, -math.pi * 115 / 180, math.pi * 115 / 180])
Ang_arr_angle1 = np.array([- math.pi * 170 / 180, math.pi * 170 / 180])
#[j1_tmin j1_tmax j2_tmin j2_tmax j3_tmin j3_tmax]
#angular domain in radians

L_arr = np.array([0.335,0.335,0.045])

#[len1 len2 len3]
bb,aa = xy_Wspace_mod(L_arr,Ang_arr_angle1,360)
CA,maxmin = Wspace_mod(L_arr,Ang_arr,rse)

numPt = len(maxmin)
print(numPt)
X_base = 0
Y_base = 0

ln1, ln2, ln3, ln4 = ax[0].plot([], [], 'r-', 
                        [], [], 'b-', 
                        [], [], 'y-',  
                        [], [], 'c-', linewidth=3, 
                        animated=False) #animated is associated with blit

xdata1, ydata1 = [], []
xdata2, ydata2 = [], []
xdata3, ydata3 = [], []
xdata4, ydata4 = [], []

# function that draws each frame of the animation
def update(i): #i is an int from 0 to frames-1, and keep looping
    ln1.set_data(xdata1[i], ydata1[i])
    ln2.set_data(xdata2[i], ydata2[i])
    ln3.set_data(xdata3[i], ydata3[i])
    ln4.set_data(xdata4[i], ydata4[i])
    return ln1, ln2, ln3, ln4



for i, j in maxmin:
    q1 = CA[[i, j], 2]
    q2 = CA[[i, j], 3]
    q3 = CA[[i, j], 4]
    #declaring X,Y coordinates for Joint 1 wrt base
    A1_x_tip = 0 + (L_arr[0] * np.cos(q1))
    A1_y_tip = 0 + (L_arr[0] * np.sin(q1))
    # L1 = plt.plot(np.array([Y_base,A1_y_tip[0]]),np.array([X_base,A1_x_tip[0]]),'r')
    #declaring X,Y coordinates for Joint 2 wrt base(i.e. joint 1)
    A2_x_tip = A1_x_tip + (L_arr[1] * np.cos(q1 + q2))
    A2_y_tip = A1_y_tip + (L_arr[1] * np.sin(q1 + q2))
    # L2 = plt.plot(np.array([A1_y_tip,A2_y_tip]),np.array([A1_x_tip,A2_x_tip]),'g')
    #declaring X,Y coordinates for Joint 3 wrt base(i.e. joint 2)
    A3_x_tip = A2_x_tip + (L_arr[2] * np.cos(q1 + q2 + q3))
    A3_y_tip = A2_y_tip + (L_arr[2] * np.sin(q1 + q2 + q3))
    # L3 = plt.plot(np.array([A2_y_tip,A3_y_tip]),np.array([A2_x_tip,A3_x_tip]),'b')
    #Marking the End Effector separately  
    # E_eff = plt.plot(A3_y_tip[0],A3_x_tip[0],'.')

    ydata1.append(np.array([X_base,A1_x_tip[0]]))
    xdata1.append(np.array([Y_base,A1_y_tip[0]]))
    ydata2.append(np.array([A1_x_tip,A2_x_tip]))
    xdata2.append(np.array([A1_y_tip,A2_y_tip]))
    ydata3.append(np.array([A2_x_tip,A3_x_tip]))
    xdata3.append(np.array([A2_y_tip,A3_y_tip]))
    ydata4.append(A3_x_tip[0])
    xdata4.append(A3_y_tip[0])
# run the animation

ax[0].set_title("Joints 1 workspace")
ax[1].set_title("Workspace Perimeter Sweep")
ax[0].set_xlabel("Y")
ax[0].set_ylabel("Z")
ax[1].set_xlabel("X")
ax[1].set_ylabel("Y")

# # plt.title('Workspace Perimeter Sweep')
# plt.xlabel('X Coordinates')
# plt.ylabel('Y Coordinates')
ani = FuncAnimation(fig, update, frames=numPt, interval=1, repeat=False)
plt.show()
    #a simple clause to prevent the arms from being deleted from the
#figure in the final iteration
    # if i < numPt(1):
    #     os.delete(L1)
    #     os.delete(L2)
    #     os.delete(L3)
    #     os.delete(base)