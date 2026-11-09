#ifndef LOOPFUNCTIONS_HPP
#define LOOPFUNCTIONS_HPP

#include <argos3/core/simulator/loop_functions.h>
#include <argos3/core/utility/datatypes/color.h>
#include <argos3/core/utility/math/vector2.h>

/**
 * Loop functions of the experiment. Provide the floor color seen by the Thymio ground sensors (floor source="loop").
 *
 * The floor is a light gray disc (the arena) with a darker gray outside it.
 */
class CExperimentLoopFunctions : public argos::CLoopFunctions
{
    public:
        void Init(argos::TConfigurationNode& t_node) override;
        argos::CColor GetFloorColor(const argos::CVector2& c_position_on_plane) override;

    private:
        argos::Real m_fArenaRadius = 1.5;
};

#endif
