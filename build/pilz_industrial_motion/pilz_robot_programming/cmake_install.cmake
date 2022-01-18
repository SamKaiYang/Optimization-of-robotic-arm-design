# Install script for directory: /home/iclab/Documents/teco_ws/src/pilz_industrial_motion/pilz_robot_programming

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Debug")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/x86_64-linux-gnu-objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/pilz_robot_programming.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pilz_robot_programming/cmake" TYPE FILE FILES
    "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/pilz_robot_programmingConfig.cmake"
    "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/pilz_robot_programmingConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/pilz_robot_programming" TYPE FILE FILES "/home/iclab/Documents/teco_ws/src/pilz_industrial_motion/pilz_robot_programming/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/safe_execute_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pilz_robot_programming" TYPE PROGRAM FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/demo_program.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pilz_robot_programming" TYPE PROGRAM FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/demo_gripper_program.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pilz_robot_programming" TYPE PROGRAM FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/demo_brake_test_program.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pilz_robot_programming" TYPE PROGRAM FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/acceptance_test_api_cmd.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pilz_robot_programming" TYPE PROGRAM FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/acceptance_test_blending.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pilz_robot_programming" TYPE PROGRAM FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/acceptance_test_brake_test.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pilz_robot_programming" TYPE PROGRAM FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/acceptance_test_circ.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pilz_robot_programming" TYPE PROGRAM FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/acceptance_test_goal_already_reached.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pilz_robot_programming" TYPE PROGRAM FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/acceptance_test_gripper_cmd.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pilz_robot_programming" TYPE PROGRAM FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/acceptance_test_move_ctrl.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pilz_robot_programming" TYPE PROGRAM FILES "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/installspace/acceptance_test_manual_move_ctrl.py")
endif()

