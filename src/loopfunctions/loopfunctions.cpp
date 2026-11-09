#include "loopfunctions.hpp"

using namespace argos;

void CExperimentLoopFunctions::Init(TConfigurationNode& t_node)
{
    GetNodeAttributeOrDefault(t_node, "arena_radius", m_fArenaRadius, m_fArenaRadius);
}

CColor CExperimentLoopFunctions::GetFloorColor(const CVector2& c_position_on_plane)
{
    if (c_position_on_plane.Length() <= m_fArenaRadius)
    {
        return CColor::GRAY80;
    }
    return CColor::GRAY40;
}

REGISTER_LOOP_FUNCTIONS(CExperimentLoopFunctions, "loopfunctions")
