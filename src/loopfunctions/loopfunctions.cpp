#include "loopfunctions.hpp"

#include <algorithm>
#include <cmath>

using namespace argos;

void CExperimentLoopFunctions::Init(TConfigurationNode& t_node)
{
    GetNodeAttributeOrDefault(t_node, "arena_side", m_fArenaSide, m_fArenaSide);
    GetNodeAttributeOrDefault(t_node, "white_width", m_fWhiteWidth, m_fWhiteWidth);
    GetNodeAttributeOrDefault(t_node, "nest_radius", m_fNestRadius, m_fNestRadius);
    GetNodeAttributeOrDefault(t_node, "nest_x", m_fNestX, m_fNestX);

    /* The farthest left-side point from the nest is one of the corners of the left side */
    const Real fHalfSide = m_fArenaSide / 2.0;
    const Real fDx = std::max(m_fNestX + fHalfSide, -m_fWhiteWidth / 2.0 - m_fNestX);
    m_fGradientEnd = std::sqrt(fDx * fDx + fHalfSide * fHalfSide);
}

CColor CExperimentLoopFunctions::GetFloorColor(const CVector2& c_position_on_plane)
{
    const Real fX = c_position_on_plane.GetX();
    if (std::abs(fX) <= m_fWhiteWidth / 2.0)
    {
        return CColor::WHITE;
    }
    if (fX > 0.0)
    {
        return CColor(GRAY_LEVEL, GRAY_LEVEL, GRAY_LEVEL);
    }
    /* Left side: black at the nest border, gray at the farthest left-side point */
    const Real fDistance = (c_position_on_plane - CVector2(m_fNestX, 0.0)).Length();
    const Real fRatio = std::clamp((fDistance - m_fNestRadius) / (m_fGradientEnd - m_fNestRadius), 0.0, 1.0);
    const auto unLevel = static_cast<UInt8>(std::round(fRatio * GRAY_LEVEL));
    return CColor(unLevel, unLevel, unLevel);
}

REGISTER_LOOP_FUNCTIONS(CExperimentLoopFunctions, "loopfunctions")
