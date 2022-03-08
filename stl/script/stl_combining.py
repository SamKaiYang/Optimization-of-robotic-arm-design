#!/usr/bin/env python3
# coding: utf-8
import rospy
import math
import stl
from stl import mesh
import numpy
from os import path

# find the max dimensions, so we can know the bounding box, getting the height,
# width, length (because these are the step size)...
def find_mins_maxs(obj):
    minx = obj.x.min()
    maxx = obj.x.max()
    miny = obj.y.min()
    maxy = obj.y.max()
    minz = obj.z.min()
    maxz = obj.z.max()
    return minx, maxx, miny, maxy, minz, maxz


def translate(_solid, step, padding, multiplier, axis):
    if 'x' == axis:
        items = 0, 3, 6
    elif 'y' == axis:
        items = 1, 4, 7
    elif 'z' == axis:
        items = 2, 5, 8
    else:
        raise RuntimeError('Unknown axis %r, expected x, y or z' % axis)

    # _solid.points.shape == [:, ((x, y, z), (x, y, z), (x, y, z))]
    _solid.points[:, items] += (step * multiplier) + (padding * multiplier)


def copy_obj(obj, dims, num_rows, num_cols, num_layers):
    w, l, h = dims
    copies = []
    for layer in range(num_layers):
        for row in range(num_rows):
            for col in range(num_cols):
                # skip the position where original being copied is
                if row == 0 and col == 0 and layer == 0:
                    continue
                _copy = mesh.Mesh(obj.data.copy())
                # pad the space between objects by 10% of the dimension being
                # translated
                if col != 0:
                    translate(_copy, w, w / 10., col, 'x')
                if row != 0:
                    translate(_copy, l, l / 10., row, 'y')
                if layer != 0:
                    translate(_copy, h, h / 10., layer, 'z')
                copies.append(_copy)
    return copies

# Using an existing stl file:
main_body = mesh.Mesh.from_file('../meshes/base_link.STL')
twist_lock = mesh.Mesh.from_file('../meshes/1.STL')

# # rotate along Y
# main_body.rotate([0.5, 0.0 , 0.0], math.radians(180))
# main_body.rotate([0.0, 0.0 , 0.5], math.radians(-180))
# main_body.z += 0.130100000000606
# # translate(main_body, 0, 0, 0.130100000000606, 'x')
# # <joint
# #     name="j1"
# #     type="revolute">
# #     <origin
# #       xyz="0 0 0.130100000000606"
# #       rpy="3.14159265358979 0 0" />
# #     <parent
# #       link="base_link" />
# #     <child
# #       link="1" />
# #     <axis
# #       xyz="0 0 -1" />
# #     <limit
# #       lower="-6.28"
# #       upper="6.28"
# #       effort="1000"
# #       velocity="1.0" />
# #   </joint>

# # I wanted to add another related STL to the final STL


# twist_lock.rotate([0.5, 0.0 , 0.0], math.radians(-90)) # 輸入徑度 三座標資訊, 最後為旋轉最大角度
# twist_lock.rotate([0.0, 0.0 , 0.5], math.radians(180)) # 輸入徑度 三座標資訊, 最後為旋轉最大角度
# main_body.rotate([0.0, 0.0 , 0.5], math.radians(-180))
# twist_lock.y += 0.11115
# # twist_lock.rotate([0.0, 0.0 , 0.0], math.radians(90))

# # <joint
# #     name="j2"
# #     type="revolute">
# #     <origin
# #       xyz="0 0.11115 0"
# #       rpy="-1.5708 0 3.1416" />
# #     <parent
# #       link="1" />
# #     <child
# #       link="2" />
# #     <axis
# #       xyz="0 0 -1" /> # 旋轉方向向量
# #     <limit
# #       lower="-6.28"
# #       upper="6.28"
# #       effort="1000"
# #       velocity="1.0" />
# #   </joint>

# link
# main_body.x += -5.89241082937383E-08
# main_body.y += -0.000607195511176322
# main_body.z += 0.0324652849797199


twist_lock.z += -0.130100000000606
twist_lock.rotate([0.5, 0.0 , 0.0], math.radians(180))
# link
# twist_lock.x += -1.55579201081481E-05
# twist_lock.y += 0.00265005484815443
# twist_lock.z += -0.00640979059142413
# joint


# # joint
# twist_lock.y += 0.11115
# twist_lock.rotate([0.5, 0.0 , 0.0], math.radians(-90)) # 輸入徑度 三座標資訊, 最後為旋轉最大角度
# twist_lock.rotate([0.0, 0.0 , 0.5], math.radians(180)) # 輸入徑度 三座標資訊, 最後為旋轉最大角度
combined = mesh.Mesh(numpy.concatenate([main_body.data, twist_lock.data]))

combined.save('../combined.STL', mode=stl.Mode.ASCII)  # save as ASCII
print("combine success")