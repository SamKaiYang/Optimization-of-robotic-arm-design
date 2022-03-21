#!/usr/bin/env python3
# coding: utf-8
import numpy
import rospy
from stl import mesh
from os import path
from urdf_parser_py.urdf import URDF, Robot
from interface_control.msg import parameter_design

class stl_conv_urdf():
    def __init__(self, robot_name, robot_parameter):
        self.robot_name = robot_name
        self.robot_parameter = robot_parameter
        self.robot_urdf = URDF.from_xml_file(robot_name)
        self.robot_stl = mesh.Mesh.from_file(robot_name + ".stl")
        self.robot_stl.points = self.robot_stl.points * self.robot_parameter.stl_scale
        self.robot_stl.update_normals()
        self.robot_stl.save(robot_name + ".stl")
        self.robot_stl = mesh.Mesh.from_file(robot_name + ".stl")
        self.robot_stl.points = self.robot_stl.points * self.robot_parameter.stl_scale
        self.robot_stl.update_normals()
        self.robot_stl.save(robot_name + ".stl")
        self.robot_stl = mesh.Mesh.from_file(robot_name + ".stl")
        self.robot_stl.points = self.robot_stl.points * self.robot_parameter.stl_scale
        self.robot_stl.update_normals()
        self.robot_stl.save(robot_name + ".stl")
        self.robot_stl = mesh.Mesh.from_file(robot_name + ".stl")
        self.robot_stl.points = self.robot_stl.points * self.robot_parameter.stl_scale
        self.robot_stl.update_normals()
        self.robot_stl.save(robot_name + ".stl")
        self.robot_stl = mesh.Mesh.from_file(robot_name + ".stl")
        self.robot_stl.points = self.robot_stl.points * self.robot_parameter.stl_scale


if __name__ == '__main__':

    rospy.init_node('stl_cal')
    # sub_dyna_space = rospy.Subscriber("/dynamics_space_data",dyna_space_data, self.dyna_space_callback)

    # your_mesh = mesh.Mesh.from_file('../meshes/1.STL')
    your_mesh = mesh.Mesh.from_file('combined.STL')
    volume, cog, inertia = your_mesh.get_mass_properties()
    print("Volume                                  = {0}".format(volume*1000))
    print("Position of the center of gravity (COG) = {0}".format(cog))
    print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0,:]))
    print("                                          {0}".format(inertia[1,:]))
    print("                                          {0}".format(inertia[2,:]))

    lines = []
    with open('tecobot_sample.urdf','r',encoding='utf-8') as urdf_config:
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

    
    with open('tecobot_sample.urdf','w',encoding='utf-8') as urdf_config:
        lines[154] = ("      xyz=\"0 0.11115 {0}\"\n".format(cog[0]))
        for data in lines:
            urdf_config.write(data)
        urdf_config.flush()
        
    
    # robot = URDF.from_xml_file("../tecobot_test.urdf")
    # print(robot)
        # for line in urdf_config.readlines():
        #     print(line.strip()) # 把末尾的'\n'删掉