import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, SetEnvironmentVariable

def generate_launch_description():
    pkg_share = get_package_share_directory('arena_disaster_pkg')
    
    # Настраиваем путь к моделям для Gazebo
    models_path = os.path.join(pkg_share, 'models')
    set_env_vars = SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', models_path)

    # Запуск Gazebo С GUI (убран флаг -s)
    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', os.path.join(pkg_share, 'worlds', 'disaster_arena.world')],
        output='screen',
        additional_env={'GZ_SIM_RESOURCE_PATH': models_path}
    )

    return LaunchDescription([
        set_env_vars,
        gazebo
    ])
