# ARGoS loads this with library="ros_thymio/libros_thymio.so" (resolved via ARGOS_PLUGIN_PATH=build)
add_library(ros_thymio MODULE
    ros_thymio.hpp
    ros_thymio.cpp
)

target_link_libraries(ros_thymio
    argos3core_simulator
    argos3plugin_simulator_genericrobot
    argos3plugin_simulator_thymio
    rclcpp::rclcpp
    ${std_msgs_TARGETS}
    ${geometry_msgs_TARGETS}
)
