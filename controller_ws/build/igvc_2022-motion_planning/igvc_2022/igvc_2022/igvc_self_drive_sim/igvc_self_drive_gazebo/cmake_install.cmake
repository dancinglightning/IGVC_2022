# Install script for directory: /home/student/Documents/IGVC_2022_Controls/controller_ws/src/igvc_2022-motion_planning/igvc_2022/igvc_2022/igvc_self_drive_sim/igvc_self_drive_gazebo

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/student/Documents/IGVC_2022_Controls/controller_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
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
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/student/Documents/IGVC_2022_Controls/controller_ws/build/igvc_2022-motion_planning/igvc_2022/igvc_2022/igvc_self_drive_sim/igvc_self_drive_gazebo/catkin_generated/installspace/igvc_self_drive_gazebo.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/igvc_self_drive_gazebo/cmake" TYPE FILE FILES
    "/home/student/Documents/IGVC_2022_Controls/controller_ws/build/igvc_2022-motion_planning/igvc_2022/igvc_2022/igvc_self_drive_sim/igvc_self_drive_gazebo/catkin_generated/installspace/igvc_self_drive_gazeboConfig.cmake"
    "/home/student/Documents/IGVC_2022_Controls/controller_ws/build/igvc_2022-motion_planning/igvc_2022/igvc_2022/igvc_self_drive_sim/igvc_self_drive_gazebo/catkin_generated/installspace/igvc_self_drive_gazeboConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/igvc_self_drive_gazebo" TYPE FILE FILES "/home/student/Documents/IGVC_2022_Controls/controller_ws/src/igvc_2022-motion_planning/igvc_2022/igvc_2022/igvc_self_drive_sim/igvc_self_drive_gazebo/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/igvc_self_drive_gazebo" TYPE DIRECTORY FILES
    "/home/student/Documents/IGVC_2022_Controls/controller_ws/src/igvc_2022-motion_planning/igvc_2022/igvc_2022/igvc_self_drive_sim/igvc_self_drive_gazebo/launch"
    "/home/student/Documents/IGVC_2022_Controls/controller_ws/src/igvc_2022-motion_planning/igvc_2022/igvc_2022/igvc_self_drive_sim/igvc_self_drive_gazebo/models"
    "/home/student/Documents/IGVC_2022_Controls/controller_ws/src/igvc_2022-motion_planning/igvc_2022/igvc_2022/igvc_self_drive_sim/igvc_self_drive_gazebo/worlds"
    REGEX "/[^/]*\\.tar\\.gz$" EXCLUDE)
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/student/Documents/IGVC_2022_Controls/controller_ws/build/igvc_2022-motion_planning/igvc_2022/igvc_2022/igvc_self_drive_sim/igvc_self_drive_gazebo/tests/cmake_install.cmake")

endif()

