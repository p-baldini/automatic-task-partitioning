#ifndef ROS_THYMIO_HPP
#define ROS_THYMIO_HPP

#include <argos3/core/control_interface/ci_controller.h>
#include <argos3/plugins/robots/generic/control_interface/ci_differential_steering_actuator.h>
#include <argos3/plugins/robots/thymio/control_interface/ci_thymio_proximity_sensor.h>
#include <argos3/plugins/robots/thymio/control_interface/ci_thymio_ground_sensor.h>

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <std_msgs/msg/float32_multi_array.hpp>

/**
 * Thymio controller that exposes the robot to ROS 2.
 *
 * Each robot gets its own node, namespaced by its (sanitized) ARGoS id:
 *   publishes  /<id>/proximity  std_msgs/Float32MultiArray  (7 readings, [0,1]:
 *                                 [0..4] front left -> front right, [5] rear left, [6] rear right)
 *   publishes  /<id>/ground     std_msgs/Float32MultiArray  (2 readings, [0,1] grayscale: [0] left, [1] right)
 *                                 only if the Thymio_ground sensor is declared
 *   subscribes /<id>/cmd_vel    geometry_msgs/Twist         (linear.x [m/s], angular.z [rad/s])
 *
 * XML params (all optional):
 *   <params max_wheel_speed="10" />   wheel speed clamp [cm/s] (real Thymio tops out around 20)
 */
class CRosThymio : public argos::CCI_Controller
{
    public:
        void Init(argos::TConfigurationNode& t_node) override;
        void ControlStep() override;
        void Reset() override;
        void Destroy() override;

    private:
        argos::CCI_DifferentialSteeringActuator* m_pcWheels = nullptr;
        argos::CCI_ThymioProximitySensor*        m_pcProximity = nullptr;
        argos::CCI_ThymioGroundSensor*           m_pcGround = nullptr;

        rclcpp::Node::SharedPtr m_pcNode;
        rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr m_pcProximityPub;
        rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr m_pcGroundPub;
        rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr     m_pcCmdVelSub;

        geometry_msgs::msg::Twist m_cCmdVel;
        argos::Real m_fMaxWheelSpeed = 10.0;  // cm/s
};

#endif
