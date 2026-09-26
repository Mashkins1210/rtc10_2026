cmake_minimum_required(VERSION 3.8)
project(arena_disaster_pkg)

find_package(ament_cmake REQUIRED)



ament_package()

install(DIRECTORY config scripts DESTINATION share/${PROJECT_NAME}/)
install(DIRECTORY launch worlds models materials DESTINATION share/${PROJECT_NAME}/)

install(PROGRAMS
  arena_disaster_pkg/mecanum_drive.py
  DESTINATION lib/${PROJECT_NAME}
)
