import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('arena_disaster_pkg')
    
    # КРИТИЧЕСКИ ВАЖНО: Указываем Gazebo, где искать модели
    models_path = os.path.join(pkg_share, 'models')
    set_env_vars_resources = SetEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.environ.get('GZ_SIM_RESOURCE_PATH', '') + ':' + models_path
    )

    # Запуск Gazebo
    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', os.path.join(pkg_share, 'worlds', 'disaster_arena.world')],
        output='screen',
        additional_env={'GZ_SIM_RESOURCE_PATH': models_path}
    )

    return LaunchDescription([
        set_env_vars_resources,
        gazebo
    ])
