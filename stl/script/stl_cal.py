#!/usr/bin/env python3
# coding: utf-8
import numpy
import rospy
from stl import mesh
from os import path
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

    your_mesh = mesh.Mesh.from_file('../meshes/1.STL')
    your_mesh = mesh.Mesh.from_file('../combined.STL')
    volume, cog, inertia = your_mesh.get_mass_properties()
    print("Volume                                  = {0}".format(volume))
    print("Position of the center of gravity (COG) = {0}".format(cog))
    print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0,:]))
    print("                                          {0}".format(inertia[1,:]))
    print("                                          {0}".format(inertia[2,:]))
