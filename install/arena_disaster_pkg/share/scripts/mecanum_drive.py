#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

class MecanumDrive(Node):
    def __init__(self):
        super().__init__('mecanum_drive')
        self.declare_parameter('wheel_radius', 0.05)
        self.declare_parameter('half_base', 0.15)
        self.r = self.get_parameter('wheel_radius').value
        self.L = self.get_parameter('half_base').value
        self.pub_fl = self.create_publisher(Float64, '/omnimen/revolute_4/cmd_vel', 10)
        self.pub_fr = self.create_publisher(Float64, '/omnimen/revolute_3/cmd_vel', 10)
        self.pub_rl = self.create_publisher(Float64, '/omnimen/revolute_2/cmd_vel', 10)
        self.pub_rr = self.create_publisher(Float64, '/omnimen/revolute_1/cmd_vel', 10)
        self.sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_cb, 10)
        self.get_logger().info(f'Mecanum drive: r={self.r}, L={self.L}')

    def cmd_cb(self, msg):
        vx = msg.linear.x
        vy = msg.linear.y
        wz = msg.angular.z
        r = self.r
        L = self.L
        w_fl = (vx - vy - wz * L) / r
        w_fr = (vx + vy + wz * L) / r
        w_rl = (vx + vy - wz * L) / r
        w_rr = (vx - vy + wz * L) / r
        from std_msgs.msg import Float64
        m = Float64()
        m.data = w_fl; self.pub_fl.publish(m)
        m.data = w_fr; self.pub_fr.publish(m)
        m.data = w_rl; self.pub_rl.publish(m)
        m.data = w_rr; self.pub_rr.publish(m)

def main():
    rclpy.init()
    node = MecanumDrive()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
