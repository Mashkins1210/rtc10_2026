import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg = get_package_share_directory("arena_disaster_pkg")
    urdf_path = os.path.join(pkg, "models", "omnimen", "urdf", "omnimen.urdf")
    bridge_yaml = os.path.join(pkg, "config", "bridge.yaml")
    with open(urdf_path, "r") as f:
        robot_desc = f.read()
    return LaunchDescription([
        Node(
            package="ros_gz_sim", executable="create",
            arguments=["-topic", "robot_description", "-name", "omnimen",
                       "-x", "0.5", "-y", "0.5", "-z", "0.3"],
            output="screen"),
        Node(
            package="robot_state_publisher", executable="robot_state_publisher",
            parameters=[{"robot_description": robot_desc, "use_sim_time": True}],
            output="screen"),
        Node(
            package="ros_gz_bridge", executable="parameter_bridge",
            arguments=["--ros-args", "-p", "config_file:=" + bridge_yaml],
            output="screen"),
    ])
