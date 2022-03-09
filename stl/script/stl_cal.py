#!/usr/bin/env python3
# coding: utf-8
import numpy
import rospy
from stl import mesh
from os import path
from urdf_parser_py.urdf import URDF, Robot
# # Using an existing stl file:
# # your_mesh = mesh.Mesh.from_file('meshes/6.STL')
# your_mesh = mesh.Mesh.from_file('combined.STL')
# # Or creating a new mesh (make sure not to overwrite the `mesh` import by
# # naming it `mesh`):
# VERTICE_COUNT = 100
# data = numpy.zeros(VERTICE_COUNT, dtype=mesh.Mesh.dtype)
# your_mesh = mesh.Mesh(data, remove_empty_areas=False)

# # The mesh normals (calculated automatically)
# your_mesh.normals
# # The mesh vectors
# your_mesh.v0, your_mesh.v1, your_mesh.v2
# # Accessing individual points (concatenation of v0, v1 and v2 in triplets)
# assert (your_mesh.points[0][0:3] == your_mesh.v0[0]).all()
# assert (your_mesh.points[0][3:6] == your_mesh.v1[0]).all()
# assert (your_mesh.points[0][6:9] == your_mesh.v2[0]).all()
# assert (your_mesh.points[1][0:3] == your_mesh.v0[1]).all()

# your_mesh.save('new_base_link.STL')

# Using an existing closed stl file:
# xlsx_outpath = "./xlsx/"


if __name__ == '__main__':

    rospy.init_node('stl_cal')

    # your_mesh = mesh.Mesh.from_file('../meshes/1.STL')
    your_mesh = mesh.Mesh.from_file('../combined.STL')
    volume, cog, inertia = your_mesh.get_mass_properties()
    print("Volume                                  = {0}".format(volume*1000))
    print("Position of the center of gravity (COG) = {0}".format(cog))
    print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0,:]))
    print("                                          {0}".format(inertia[1,:]))
    print("                                          {0}".format(inertia[2,:]))

    lines = []
    with open('../tecobot_test.urdf','r',encoding='utf-8') as urdf_config:
        lines = urdf_config.readlines()
        size = urdf_config.read()
        # print(urdf_config.read())
        flen=len(lines)
        print("line count:", flen)

        line_content = lines[151]
        print("line content:", line_content)

        for i in range(flen):
            if lines[i].startswith("    name=\"j2\""):
                print("j2 line number:", i+1)
            elif lines[i].startswith("    name=\"j3\""):
                print("j3 line number:", i+1)
                break
            else:
                continue

    
    with open('../tecobot_test.urdf','w',encoding='utf-8') as urdf_config:
        lines[154] = ("      xyz=\"0 0.11115 {0}\"\n".format(cog[0]))
        for data in lines:
            urdf_config.write(data)
        urdf_config.flush()
        
    
    robot = URDF.from_xml_file("../tecobot_test.urdf")
    print(robot)
        # for line in urdf_config.readlines():
        #     print(line.strip()) # 把末尾的'\n'删掉