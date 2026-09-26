import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_arena = get_package_share_directory('arena_disaster_pkg')
    
    models_path = os.path.join(pkg_arena, 'models')
    set_env_vars = SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', models_path)

    urdf_file = os.path.join(pkg_arena, 'models', 'omnimen', 'urdf', 'omnimen.urdf')
    with open(urdf_file, 'r', encoding='utf-8') as f:
        robot_desc = f.read()

    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    # Спавн робота с нужными координатами
    spawn_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'omnimen',
            '-file', os.path.join(pkg_arena, 'models', 'omnimen_with_sensors', 'omnimen_final.sdf'),
            '-x', '-1.5587', '-y', '-1.4865', '-z', '0.15',
            '-R', '0.0', '-P', '0.0', '-Y', '1.5698'
        ],
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/model/omnimen/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/model/omnimen/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        ],
        output='screen',
        remappings=[
            ('/model/omnimen/scan', '/omnimen/scan'),
            ('/model/omnimen/camera/image_raw', '/omnimen/camera/image_raw'),
        ],
        parameters=[{'use_sim_time': True}]
    )

    arena_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_arena, 'launch', 'arena_sim.launch.py')
        )
    )

    return LaunchDescription([
        set_env_vars,
        arena_launch,
        rsp_node,
        spawn_node,
        bridge_node
    ])
