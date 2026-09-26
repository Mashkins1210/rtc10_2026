#!/bin/bash
sleep 5  # Ждём, пока робот заспавнится

# Перемещаем робота через сервис Gazebo
gz service -s /world/disaster_arena/set_pose \
  --reqtype gz.msgs.Pose \
  --reptype gz.msgs.Boolean \
  --timeout 1000 \
  --req "name: 'omnimen', position: {x: -1.5587, y: -1.4865, z: 0.15}, orientation: {x: 0, y: 0, z: 0.9999, w: 0.01}"

echo "✅ Робот перемещён"
