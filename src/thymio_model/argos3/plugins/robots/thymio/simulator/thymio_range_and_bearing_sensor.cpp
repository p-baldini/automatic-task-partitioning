/**
 * @file <argos3/plugins/robots/thymio/simulator/thymio_range_and_bearing_sensor.cpp>
 *
 * LOCAL CHANGE (not in upstream). Update() follows ARGoS' CRangeAndBearingMediumSensor
 * (src/plugins/robots/generic/simulator/range_and_bearing_medium_sensor.cpp), with the IR cone check added.
 */

#include "thymio_range_and_bearing_sensor.h"
#include "thymio_measures.h"

#include <argos3/core/simulator/simulator.h>
#include <argos3/core/simulator/entity/composable_entity.h>
#include <argos3/core/simulator/entity/controllable_entity.h>
#include <argos3/plugins/simulator/entities/rab_equipped_entity.h>
#include <argos3/plugins/simulator/media/rab_medium.h>

namespace argos
{
    namespace
    {
        const CRange<CRadians> INCLINATION_RANGE(CRadians(0), CRadians(ARGOS_PI));
    }

    /****************************************/
    /****************************************/

    void CThymioRangeAndBearingSensor::SetRobot(CComposableEntity& c_entity)
    {
        m_pcRAB = &c_entity.GetComponent<CRABEquippedEntity>("rab");
        m_pcControllable = &c_entity.GetComponent<CControllableEntity>("controller");
    }

    /****************************************/
    /****************************************/

    void CThymioRangeAndBearingSensor::Init(TConfigurationNode& t_tree)
    {
        try
        {
            CCI_RangeAndBearingSensor::Init(t_tree);
            GetNodeAttributeOrDefault(t_tree, "show_rays", m_bShowRays, m_bShowRays);
            GetNodeAttributeOrDefault(t_tree, "noise_std_dev", m_fDistanceNoiseStdDev, m_fDistanceNoiseStdDev);
            GetNodeAttributeOrDefault(t_tree, "packet_drop_prob", m_fPacketDropProb, m_fPacketDropProb);
            Real fApertureDeg = ToDegrees(m_cAperture).GetValue();
            GetNodeAttributeOrDefault(t_tree, "aperture", fApertureDeg, fApertureDeg);
            m_cAperture = ToRadians(CDegrees(fApertureDeg));
            if (m_fPacketDropProb > 0.0 || m_fDistanceNoiseStdDev > 0.0)
            {
                m_pcRNG = CRandom::CreateRNG("argos");
            }
            std::string strMedium;
            GetNodeAttribute(t_tree, "medium", strMedium);
            m_pcMedium = &CSimulator::GetInstance().GetMedium<CRABMedium>(strMedium);
            m_pcRAB->SetMedium(*m_pcMedium);
        }
        catch (CARGoSException& ex)
        {
            THROW_ARGOSEXCEPTION_NESTED("Error initializing the Thymio range and bearing sensor", ex);
        }
        Enable();
    }

    /****************************************/
    /****************************************/

    bool CThymioRangeAndBearingSensor::IsInIRCone(const CRABEquippedEntity& c_source,
                                                  const CRABEquippedEntity& c_target) const
    {
        CVector3 cLocal = c_target.GetPosition() - c_source.GetPosition();
        cLocal.Rotate(c_source.GetOrientation().Inverse());
        const CRadians cDirection = cLocal.GetZAngle();
        for (const CRadians& cSensorAngle : PROXIMITY_SENSOR_ANGLES)
        {
            if (Abs((cDirection - cSensorAngle).SignedNormalize()) <= m_cAperture)
            {
                return true;
            }
        }
        return false;
    }

    /****************************************/
    /****************************************/

    void CThymioRangeAndBearingSensor::Update()
    {
        if (IsDisabled())
        {
            return;
        }
        m_tReadings.clear();
        SPacket sPacket;
        for (CRABEquippedEntity* pcOther : m_pcMedium->GetRABsCommunicatingWith(*m_pcRAB))
        {
            /* LOCAL CHANGE: the sender must emit towards us and we must see the sender */
            if (!IsInIRCone(*pcOther, *m_pcRAB) || !IsInIRCone(*m_pcRAB, *pcOther))
            {
                continue;
            }
            if (m_pcRNG != nullptr && m_fPacketDropProb > 0.0 && m_pcRNG->Bernoulli(m_fPacketDropProb))
            {
                continue;
            }
            if (m_bShowRays)
            {
                m_pcControllable->AddCheckedRay(false, CRay3(pcOther->GetPosition(), m_pcRAB->GetPosition()));
            }
            CVector3 cToSender = pcOther->GetPosition() - m_pcRAB->GetPosition();
            if (m_pcRNG != nullptr && m_fDistanceNoiseStdDev > 0.0)
            {
                cToSender += CVector3(m_pcRNG->Gaussian(m_fDistanceNoiseStdDev),
                                      m_pcRNG->Uniform(INCLINATION_RANGE),
                                      m_pcRNG->Uniform(CRadians::UNSIGNED_RANGE));
            }
            /* Express in the robot frame; range in cm, vertical bearing as elevation */
            cToSender.Rotate(m_pcRAB->GetOrientation().Inverse());
            cToSender.ToSphericalCoords(sPacket.Range, sPacket.VerticalBearing, sPacket.HorizontalBearing);
            sPacket.Range *= 100.0;
            sPacket.HorizontalBearing.SignedNormalize();
            sPacket.VerticalBearing.Negate();
            sPacket.VerticalBearing += CRadians::PI_OVER_TWO;
            sPacket.VerticalBearing.SignedNormalize();
            sPacket.Data = pcOther->GetData();
            m_tReadings.push_back(sPacket);
        }
    }

    /****************************************/
    /****************************************/

    void CThymioRangeAndBearingSensor::Reset()
    {
        m_tReadings.clear();
    }

    void CThymioRangeAndBearingSensor::Enable()
    {
        m_pcRAB->Enable();
        CCI_Sensor::Enable();
    }

    void CThymioRangeAndBearingSensor::Disable()
    {
        m_pcRAB->Disable();
        CCI_Sensor::Disable();
    }

    void CThymioRangeAndBearingSensor::Destroy()
    {
        m_pcMedium->RemoveEntity(*m_pcRAB);
    }

    /****************************************/
    /****************************************/

    REGISTER_SENSOR(CThymioRangeAndBearingSensor,
                    "Thymio_range_and_bearing", "medium",
                    "Paolo Baldini",
                    "1.0",
                    "Range-and-bearing sensor limited to the Thymio's front/rear IR coverage.",
                    "Same as <range_and_bearing implementation=\"medium\">, but a message is received\n"
                    "only if sender and receiver are each within 'aperture' (degrees, default 20)\n"
                    "of one of the other's proximity sensor directions. This mimics the real\n"
                    "Thymio, which communicates through its front and rear IR sensors.\n"
                    "Use it from controllers through ci_range_and_bearing_sensor.h.\n\n"
                    "REQUIRED XML CONFIGURATION\n\n"
                    "  <Thymio_range_and_bearing implementation=\"medium\" medium=\"rab\" />\n\n"
                    "OPTIONAL XML CONFIGURATION\n\n"
                    "  aperture          half-angle of each IR sensor cone, in degrees (default 20)\n"
                    "  show_rays         draw the received links in the OpenGL view (default false)\n"
                    "  noise_std_dev     as in the generic sensor (default 0)\n"
                    "  packet_drop_prob  as in the generic sensor (default 0)\n",
                    "Usable");
}
