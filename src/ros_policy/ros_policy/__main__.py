"""ros_policy ROS 2 node: random walk with collision avoidance.

One instance controls one robot; select it by namespace, e.g.:
    python -m ros_policy --ros-args -r __ns:=/thymio_0
"""
import random

import rclpy
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray


class RandomWalkPolicy(Node):
    """Moves straight for a random time, then turns in place for a random time; front obstacles override the walk."""

    def __init__(self) -> None:
        super().__init__("policy")
        self.linear_speed = self.declare_parameter("linear_speed", 0.08).value         # m/s
        self.angular_speed = self.declare_parameter("angular_speed", 1.5).value        # rad/s
        self.obstacle_threshold = self.declare_parameter("obstacle_threshold", 0.1).value  # proximity in [0,1]
        self.max_straight_time = self.declare_parameter("max_straight_time", 5.0).value  # s
        self.max_turn_time = self.declare_parameter("max_turn_time", 2.0).value          # s
        control_period = self.declare_parameter("control_period", 0.1).value          # s

        self.proximity = [0.0] * 7
        self.turning = False
        self.turn_direction = 1.0
        self.avoid_direction = 0.0  # 0 = not avoiding; otherwise sign of the avoidance rotation
        self.phase_end = self._now()

        self.cmd_vel_pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.create_subscription(Float32MultiArray, "proximity", self._on_proximity, 10)
        self.create_timer(control_period, self._step)

    def _now(self) -> float:
        return self.get_clock().now().nanoseconds * 1e-9

    def _on_proximity(self, msg: Float32MultiArray) -> None:
        self.proximity = list(msg.data)

    def _step(self) -> None:
        cmd = Twist()
        front = self.proximity[:5]

        if max(front) > self.obstacle_threshold:
            # Pick a direction once per avoidance maneuver, so the robot does not oscillate in front of obstacles
            if self.avoid_direction == 0.0:
                left = front[0] + front[1] + 0.5 * front[2]
                right = front[4] + front[3] + 0.5 * front[2]
                if left != right:
                    self.avoid_direction = -1.0 if left > right else 1.0
                else:
                    self.avoid_direction = random.choice((-1.0, 1.0))
            cmd.angular.z = self.avoid_direction * self.angular_speed
        else:
            if self.avoid_direction != 0.0:
                # Obstacle cleared: resume walking straight
                self.avoid_direction = 0.0
                self._start_phase(turning=False)
            elif self._now() >= self.phase_end:
                self._start_phase(turning=not self.turning)

            if self.turning:
                cmd.angular.z = self.turn_direction * self.angular_speed
            else:
                cmd.linear.x = self.linear_speed

        self.cmd_vel_pub.publish(cmd)

    def _start_phase(self, turning: bool) -> None:
        self.turning = turning
        if turning:
            self.turn_direction = random.choice((-1.0, 1.0))
            self.phase_end = self._now() + random.uniform(0.0, self.max_turn_time)
        else:
            self.phase_end = self._now() + random.uniform(0.0, self.max_straight_time)

    def stop(self) -> None:
        self.cmd_vel_pub.publish(Twist())


def main() -> None:
    # Keep the context alive on Ctrl+C, so the final stop command can still be published
    rclpy.init(signal_handler_options=SignalHandlerOptions.NO)
    node = RandomWalkPolicy()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
