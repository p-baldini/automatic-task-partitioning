#include "ros_thymio.hpp"

#include <algorithm>
#include <cctype>

using namespace argos;

namespace
{
    // Distance between the wheels [m]. Must match the kinematics of the simulated
    // Thymio (Thymio_WHEEL_DISTANCE in thymio_measures.cpp).
    constexpr Real INTERWHEEL_DISTANCE = 0.08;

    /* ROS names allow only [A-Za-z0-9_] and must not start with a digit */
    std::string ToRosName(std::string str_id)
    {
        auto isInvalidChar = [](unsigned char c){ return !std::isalnum(c) && c != '_'; };
        std::replace_if(str_id.begin(), str_id.end(), isInvalidChar, '_');
        if (str_id.empty() || std::isdigit(static_cast<unsigned char>(str_id[0])))
        {
            str_id.insert(0, "robot_");
        }
        return str_id;
    }

    // The simulated ground sensor returns CColor::ToGrayScale(), i.e., a value in [0, 255].
    constexpr Real GROUND_MAX_READING = 255.0;

    /* Packs a sensor's readings into a Float32MultiArray message */
    template <typename TReadings>
    std_msgs::msg::Float32MultiArray ToMultiArray(const TReadings& t_readings)
    {
        std_msgs::msg::Float32MultiArray cMsg;
        for (const auto& sReading : t_readings)
        {
            cMsg.data.push_back(static_cast<float>(sReading.Value));
        }
        return cMsg;
    }

    /* Packs the ground readings into a Float32MultiArray message, normalized in [0, 1] (0 black, 1 white) */
    template <typename TReadings>
    std_msgs::msg::Float32MultiArray ToNormalizedGround(const TReadings& t_readings)
    {
        auto cMsg = ToMultiArray(t_readings);
        auto normalize = [](float f_value){ return std::clamp(f_value / GROUND_MAX_READING, 0.0, 1.0); };
        std::transform(cMsg.data.begin(), cMsg.data.end(), cMsg.data.begin(), normalize);
        return cMsg;
    }
}

void CRosThymio::Init(TConfigurationNode& t_node)
{
    /* All robots live in the same process: initialize the ROS context only once */
    if (!rclcpp::ok())
    {
        rclcpp::init(0, nullptr, rclcpp::InitOptions(), rclcpp::SignalHandlerOptions::None);
    }

    m_pcWheels = GetActuator<CCI_DifferentialSteeringActuator>("differential_steering");
    m_pcProximity = GetSensor<CCI_ThymioProximitySensor>("Thymio_proximity");
    m_pcGround = GetSensor<CCI_ThymioGroundSensor>("Thymio_ground");
    GetNodeAttributeOrDefault(t_node, "max_wheel_speed", m_fMaxWheelSpeed, m_fMaxWheelSpeed);

    m_pcNode = std::make_shared<rclcpp::Node>("controller", ToRosName(GetId()));
    m_pcProximityPub = m_pcNode->create_publisher<std_msgs::msg::Float32MultiArray>("proximity", 10);
    m_pcGroundPub = m_pcNode->create_publisher<std_msgs::msg::Float32MultiArray>("ground", 10);

    auto cCmdVelCallback = [this](const geometry_msgs::msg::Twist::SharedPtr pc_msg){ m_cCmdVel = *pc_msg; };
    m_pcCmdVelSub = m_pcNode->create_subscription<geometry_msgs::msg::Twist>("cmd_vel", 10, cCmdVelCallback);
}

void CRosThymio::ControlStep()
{
    /* Process pending callbacks (non-blocking) */
    rclcpp::spin_some(m_pcNode);

    /* Publish sensor readings */
    m_pcProximityPub->publish(ToMultiArray(m_pcProximity->GetReadings())); // TODO: make it a custom message type
    m_pcGroundPub->publish(ToNormalizedGround(m_pcGround->GetReadings()));

    /* Twist -> wheel speeds; ARGoS wants cm/s */
    const Real fV = m_cCmdVel.linear.x;
    const Real fW = m_cCmdVel.angular.z;
    Real fLeft = (fV - fW * INTERWHEEL_DISTANCE / 2.0) * 100.0;
    Real fRight = (fV + fW * INTERWHEEL_DISTANCE / 2.0) * 100.0;
    fLeft = std::clamp(fLeft, -m_fMaxWheelSpeed, m_fMaxWheelSpeed);
    fRight = std::clamp(fRight, -m_fMaxWheelSpeed, m_fMaxWheelSpeed);
    m_pcWheels->SetLinearVelocity(fLeft, fRight);
}

void CRosThymio::Reset()
{
    m_cCmdVel = geometry_msgs::msg::Twist();
}

void CRosThymio::Destroy()
{
    m_pcCmdVelSub.reset();
    m_pcGroundPub.reset();
    m_pcProximityPub.reset();
    m_pcNode.reset();
}

REGISTER_CONTROLLER(CRosThymio, "ros_thymio_controller")
