"""Launches ARGoS plus the gossip, policy and evaluation nodes of every robot.

Usage: ros2 launch ros_experiment experiment.launch.py [n_robots:=10] [arena:=/path/to/arena.argos]
The number of robots must match the quantity of Thymios in the arena file (namespaces are thymio_0 ... thymio_N-1).
"""
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction, RegisterEventHandler, Shutdown
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def _launch_setup(context, *args, **kwargs):
    n_robots = int(LaunchConfiguration("n_robots").perform(context))
    argos = ExecuteProcess(cmd=["argos3", "-c", LaunchConfiguration("arena")], output="screen")
    actions = [argos]
    for i in range(n_robots):
        for package in ("ros_gossip", "ros_policy", "ros_evaluation"):
            actions.append(Node(package=package, executable=package.removeprefix("ros_"),
                                namespace=f"thymio_{i}", output="screen"))
    # The experiment ends when ARGoS exits
    actions.append(RegisterEventHandler(OnProcessExit(target_action=argos, on_exit=[Shutdown()])))
    return actions


def generate_launch_description() -> LaunchDescription:
    root = os.environ.get("PIXI_PROJECT_ROOT", os.getcwd())
    return LaunchDescription([
        DeclareLaunchArgument("n_robots", default_value="10"),
        DeclareLaunchArgument("arena", default_value=os.path.join(root, "exp", "arena.argos")),
        OpaqueFunction(function=_launch_setup),
    ])
