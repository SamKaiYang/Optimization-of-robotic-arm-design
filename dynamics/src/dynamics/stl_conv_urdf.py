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
        self.axis_2_length = 0.0
        self.axis_3_length = 0.0
        self.arm_weight = 0.0
        self.payload = 0.0
        self.DoF = 6
        self.sub_parameter_design = rospy.Subscriber("/parameter_design",parameter_design, self.parameter_design_callback)
        self.robot_name = robot_name
        self.robot_parameter = robot_parameter
        self.robot_stl_axis_2 = None
        self.robot_stl_axis_3 = None
        self.robot_urdf = URDF.from_xml_file(path.dirname(path.realpath(__file__)) + "/urdf/" + robot_name + ".urdf")
        self.lines = []
        self.J3_line = 0
        self.J4_line = 0
        self.L2_line = 0
        self.L3_line = 0
        self.L2_volume = 0.0
        self.L3_volume = 0.0
        self.L2_cog = []
        self.L3_cog = []
        self.L2_inertia = []
        self.L3_inertia = []
        # self.robot_stl = mesh.Mesh.from_file(robot_name + ".stl")
        # self.robot_stl.points = self.robot_stl.points * self.robot_parameter.stl_scale
        # self.robot_stl.update_normals()

    def stl_read_file(self):
        self.robot_stl_axis_2 = mesh.Mesh.from_file(path.dirname(path.realpath(__file__))+"/meshes/" + self.robot_name + "_2_"+ str(self.axis_2_length) + ".STL")
        self.robot_stl_axis_3 = mesh.Mesh.from_file(path.dirname(path.realpath(__file__))+"/meshes/" + self.robot_name + "_3_"+ str(self.axis_3_length) + ".STL")


        self.L2_volume, self.L2_cog, self.L2_inertia = self.robot_stl_axis_2.get_mass_properties()
        self.L2_volume = self.L2_volume*1000
        self.L2_inertia = self.L2_inertia*1000
        print("============================================================")
        print("Volume                                  = {0}".format(self.L2_volume))
        print("Position of the center of gravity (COG) = {0}".format(self.L2_cog))
        print("Inertia matrix at expressed at the COG  = {0}".format(self.L2_inertia[0,:]))
        print("                                          {0}".format(self.L2_inertia[1,:]))
        print("                                          {0}".format(self.L2_inertia[2,:]))

        self.L3_volume, self.L3_cog, self.L3_inertia = self.robot_stl_axis_3.get_mass_properties()
        self.L3_volume = self.L3_volume*1000
        self.L3_inertia = self.L3_inertia*1000
        print("============================================================")
        print("Volume                                  = {0}".format(self.L3_volume))
        print("Position of the center of gravity (COG) = {0}".format(self.L3_cog))
        print("Inertia matrix at expressed at the COG  = {0}".format(self.L3_inertia[0,:]))
        print("                                          {0}".format(self.L3_inertia[1,:]))
        print("                                          {0}".format(self.L3_inertia[2,:]))
        print("============================================================")
    def read_check_urdf(self):
        
        with open(path.dirname(path.realpath(__file__)) + "/urdf/" + self.robot_name + ".urdf",'r',encoding='utf-8') as urdf_config:
            self.lines = urdf_config.readlines()
            size = urdf_config.read()
            # print(urdf_config.read())
            flen=len(self.lines)
            print("line count:", flen)

            for i in range(flen):
                if self.lines[i].startswith("    name=\"2\"") and self.lines[i+2].startswith("      <origin"):
                    self.L2_line = i+1
                    print("link 2 line number:", self.L2_line)
                elif self.lines[i].startswith("    name=\"3\"") and self.lines[i+2].startswith("      <origin"):
                    self.L3_line = i+1
                    print("link 3 line number:", self.L3_line)
                elif self.lines[i].startswith("    name=\"j3\"") and self.lines[i+2].startswith("      <origin"):
                    self.J3_line = i+1
                    print("joint 3 line number:", self.J3_line)
                elif self.lines[i].startswith("    name=\"j4\"") and self.lines[i+2].startswith("      <origin"):
                    self.J4_line = i+1
                    print("joint 4 line number:", self.J4_line)
                    print("read urdf data no problem")
                    print("============================================================")
                    break
                else:
                    continue

    def data_write_urdf(self):
        with open(path.dirname(path.realpath(__file__)) + "/urdf/" + self.robot_name + ".urdf",'w',encoding='utf-8') as urdf_config:
            cog_lines = int(self.L2_line + 2)
            mass_lines = int(self.L2_line + 5)
            inertia_lines = int(self.L2_line + 7)
            joint_pos = int(self.J3_line + 2)

            self.axis_2_length = 281.5 - self.axis_2_length*10
            joint3_pos_y = 0.408000000000056 - self.axis_2_length

            self.lines[cog_lines] = ("        xyz=\"{0[0]} {0[1]} {0[2]}\"\n".format(self.L2_cog))
            self.lines[mass_lines] = ("        value=\"{0}\"  />\n".format(self.L2_volume))
            self.lines[inertia_lines] = ("        ixx=\"{0[0][0]}\"\n".format(self.L2_inertia))
            self.lines[inertia_lines+1] = ("        ixy=\"{0[0][1]}\"\n".format(self.L2_inertia))
            self.lines[inertia_lines+2] = ("        ixz=\"{0[0][2]}\"\n".format(self.L2_inertia))
            self.lines[inertia_lines+3] = ("        iyy=\"{0[1][1]}\"\n".format(self.L2_inertia))
            self.lines[inertia_lines+4] = ("        iyz=\"{0[1][2]}\"\n".format(self.L2_inertia))
            self.lines[inertia_lines+5] = ("        izz=\"{0[2][2]}\" />\n".format(self.L2_inertia))
            self.lines[joint_pos] = ("        xyz=\"0 {0} 0\"\n".format(joint3_pos_y))
            # xyz="0 0.408000000000056 0"
            for data in self.lines:
                urdf_config.write(data)
            urdf_config.flush()

        with open(path.dirname(path.realpath(__file__)) + "/urdf/" + self.robot_name + ".urdf",'w',encoding='utf-8') as urdf_config:
            cog_lines = int(self.L3_line + 2)
            mass_lines = int(self.L3_line + 5)
            inertia_lines = int(self.L3_line + 7)
            joint_pos = int(self.J4_line + 2)

            self.axis_3_length = 265 - self.axis_3_length*10
            joint4_pos_y = 0.372499999999936 - self.axis_3_length

            self.lines[cog_lines] = ("        xyz=\"{0[0]} {0[1]} {0[2]}\"\n".format(self.L3_cog))
            self.lines[mass_lines] = ("        value=\"{0}\"  />\n".format(self.L3_volume))
            self.lines[inertia_lines] = ("        ixx=\"{0[0][0]}\"\n".format(self.L3_inertia))
            self.lines[inertia_lines+1] = ("        ixy=\"{0[0][1]}\"\n".format(self.L3_inertia))
            self.lines[inertia_lines+2] = ("        ixz=\"{0[0][2]}\"\n".format(self.L3_inertia))
            self.lines[inertia_lines+3] = ("        iyy=\"{0[1][1]}\"\n".format(self.L3_inertia))
            self.lines[inertia_lines+4] = ("        iyz=\"{0[1][2]}\"\n".format(self.L3_inertia))
            self.lines[inertia_lines+5] = ("        izz=\"{0[2][2]}\" />\n".format(self.L3_inertia))
            self.lines[joint_pos] = ("        xyz=\"0 {0} 0.0109000000011954\"\n".format(joint4_pos_y))
            # xyz="0 0.372499999999936 0.0109000000011954"
            for data in self.lines:
                urdf_config.write(data)
            urdf_config.flush()
        print("URDF write down.")
        print("============================================================")

    def task_set(self):
        pass

    def parameter_design_callback(self, data):
        self.axis_2_length = data.axis_2_length
        self.axis_3_length = data.axis_3_length
        self.arm_weight = data.arm_weight
        self.payload = data.payload
        self.DoF = data.DoF
        rospy.loginfo("I heard command is %s", self.axis_2_length)
        rospy.loginfo("I heard command is %s", self.axis_3_length)
        rospy.loginfo("I heard command is %s", self.arm_weight)
        rospy.loginfo("I heard command is %s", self.payload)
        rospy.loginfo("I heard command is %s", self.DoF)

        self.stl_read_file()
        self.read_check_urdf()
        self.data_write_urdf()

if __name__ == '__main__':

    rospy.init_node('stl_cal')
    stl_cal = stl_conv_urdf("random","test")

    while not rospy.is_shutdown():
        stl_cal.task_set()


    