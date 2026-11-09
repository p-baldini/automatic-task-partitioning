cmake_minimum_required(VERSION 3.22)
project(task_specialization LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# ARGoS (ARGoS_DIR is exported by the argos3 package's pixi activation script)
find_package(ARGoS REQUIRED COMPONENTS entities genericrobot dynamics2d)
include_directories(${ARGOS_INCLUDE_DIRS})
link_directories(${ARGOS_LIBRARY_DIR})

# ROS 2
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

add_subdirectory(thymio_model)
add_subdirectory(ros_thymio)
add_subdirectory(loopfunctions)
