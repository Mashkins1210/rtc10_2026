import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
def generate_launch_description():
    pkg_arena = get_package_share_directory('arena_disaster_pkg')
    models_path = os.path.join(pkg_arena, 'models')
    set_env = SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', models_path)
    urdf_path = os.path.join(pkg_arena, 'models', 'omnimen', 'urdf', 'omnimen.urdf')
    with open(urdf_path, 'r', encoding='utf-8') as f:
        robot_desc = f.read()
    rsp = Node(package='robot_state_publisher', executable='robot_state_publisher', name='robot_state_publisher', output='screen', parameters=[{'robot_description': robot_desc, 'use_sim_time': True}])
    jsp = Node(package='joint_state_publisher', executable='joint_state_publisher', name='joint_state_publisher', output='screen', parameters=[{'use_sim_time': True}])
    spawn = Node(package='ros_gz_sim', executable='create', arguments=['-name', 'omnimen', '-topic', 'robot_description', '-x', '0.0', '-y', '0.0', '-z', '0.2'], output='screen')
    bridge = Node(package='ros_gz_bridge', executable='parameter_bridge', arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock', '/model/omnimen/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan', '/model/omnimen/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image'], output='screen', remappings=[('/model/omnimen/scan', '/omnimen/scan'), ('/model/omnimen/camera/image_raw', '/omnimen/camera/image_raw')])
    mecanum = Node(package='arena_disaster_pkg', executable='mecanum_drive.py', name='mecanum_drive', output='screen', parameters=[{'wheel_radius': 0.05}, {'base_half_size': 0.15}])
    arena = IncludeLaunchDescription(PythonLaunchDescriptionSource(os.path.join(pkg_arena, 'launch', 'arena_sim.launch.py')))
    return LaunchDescription([set_env, arena, rsp, jsp, spawn, bridge, mecanum])
