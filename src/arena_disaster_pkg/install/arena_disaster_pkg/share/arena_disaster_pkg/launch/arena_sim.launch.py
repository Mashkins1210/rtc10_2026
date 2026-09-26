import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_arena = get_package_share_directory('arena_disaster_pkg')
    
    # Прямой путь к папке models
    models_path = os.path.join(pkg_arena, 'models')

    world_arg = DeclareLaunchArgument(
        'world',
        default_value='disaster_arena.world',
        description='Path to world file'
    )

    world_path = PathJoinSubstitution([pkg_arena, 'worlds', LaunchConfiguration('world')])

    env = os.environ.copy()
    # Устанавливаем ОБЕ переменные для совместимости с Gazebo 6 (Garden)
    env['GZ_SIM_RESOURCE_PATH'] = models_path
    env['IGN_GAZEBO_RESOURCE_PATH'] = models_path

    gz_sim_process = ExecuteProcess(
        cmd=['ign', 'gazebo', '-v', '4', '-r', world_path],
        output='screen',
        name='gazebo_sim',
        env=env
    )

    return LaunchDescription([
        world_arg,
        gz_sim_process,
    ])
