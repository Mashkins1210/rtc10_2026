#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

class MecanumDrive(Node):
    def __init__(self):
        super().__init__('mecanum_drive')
        self.declare_parameter('wheel_radius', 0.05)
        self.declare_parameter('base_half_size', 0.15)
        self.r = self.get_parameter('wheel_radius').value
        self.L = self.get_parameter('base_half_size').value
        self.subscription = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.pubs = {}
        for joint in ['revolute_1', 'revolute_2', 'revolute_3', 'revolute_4']:
            self.pubs[joint] = self.create_publisher(
                Float64, f'{joint}/cmd_vel', 10)
        self.get_logger().info(f'Mecanum drive started. r={self.r}, L={self.L}')

    def cmd_vel_callback(self, msg):
        vx = msg.linear.x
        vy = msg.linear.y
        wz = msg.angular.z
        omega_FL = (vx - vy - wz * self.L) / self.r
        omega_FR = (vx + vy + wz * self.L) / self.r
        omega_RL = (vx + vy - wz * self.L) / self.r
        omega_RR = (vx - vy + wz * self.L) / self.r
        mapping = {
            'revolute_4': omega_FL,
            'revolute_3': omega_FR,
            'revolute_2': omega_RL,
            'revolute_1': omega_RR,
        }
        for joint, omega in mapping.items():
            msg_out = Float64()
            msg_out.data = omega
            self.pubs[joint].publish(msg_out)

def main(args=None):
    rclpy.init(args=args)
    node = MecanumDrive()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
