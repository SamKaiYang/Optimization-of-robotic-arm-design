execute_process(COMMAND "/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/iclab/Documents/teco_ws/src/build/pilz_industrial_motion/pilz_robot_programming/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
