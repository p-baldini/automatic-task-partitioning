/**
 * @file <argos3/plugins/robots/thymio/simulator/thymio_range_and_bearing_sensor.h>
 *
 * LOCAL CHANGE (not in upstream): range-and-bearing sensor restricted to the Thymio's IR coverage.
 *
 * The real Thymio has no range-and-bearing board: robots talk through the horizontal IR proximity
 * sensors (prox.comm), which both emit and receive, and only look forward and backward. The generic
 * ARGoS range_and_bearing sensor is omnidirectional, so two Thymios side by side would communicate.
 *
 * This sensor is the generic "medium" one (same XML attributes, same reading format) plus one rule:
 * a message from robot S is received by robot R only if
 *   - R lies within `aperture` of one of S's proximity sensor directions (S can emit towards R), and
 *   - S lies within `aperture` of one of R's proximity sensor directions (R can receive from S).
 * Directions are taken from the robot centres and compared with PROXIMITY_SENSOR_ANGLES.
 */

#ifndef THYMIO_RANGE_AND_BEARING_SENSOR_H
#define THYMIO_RANGE_AND_BEARING_SENSOR_H

namespace argos
{
    class CThymioRangeAndBearingSensor;
    class CRABEquippedEntity;
    class CControllableEntity;
    class CRABMedium;
}

#include <argos3/core/simulator/sensor.h>
#include <argos3/core/utility/math/rng.h>
#include <argos3/plugins/robots/generic/control_interface/ci_range_and_bearing_sensor.h>

namespace argos
{
    class CThymioRangeAndBearingSensor : public CSimulatedSensor, public CCI_RangeAndBearingSensor
    {
        public:
            void SetRobot(CComposableEntity& c_entity) override;
            void Init(TConfigurationNode& t_tree) override;
            void Update() override;
            void Reset() override;
            void Destroy() override;
            void Enable() override;
            void Disable() override;

        private:
            /* True if the direction of c_target, seen from c_source, falls within one of its IR sensor cones */
            bool IsInIRCone(const CRABEquippedEntity& c_source, const CRABEquippedEntity& c_target) const;

            CRABEquippedEntity*  m_pcRAB = nullptr;
            CControllableEntity* m_pcControllable = nullptr;
            CRABMedium*          m_pcMedium = nullptr;
            CRandom::CRNG*       m_pcRNG = nullptr;
            Real                 m_fDistanceNoiseStdDev = 0.0;
            Real                 m_fPacketDropProb = 0.0;
            CRadians             m_cAperture = CRadians(ARGOS_PI / 9.0);  // 20 degrees
            bool                 m_bShowRays = false;
    };
}

#endif
