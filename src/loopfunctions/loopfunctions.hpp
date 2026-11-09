#ifndef LOOPFUNCTIONS_HPP
#define LOOPFUNCTIONS_HPP

#include <argos3/core/simulator/loop_functions.h>
#include <argos3/core/utility/datatypes/color.h>
#include <argos3/core/utility/math/vector2.h>

/**
 * Loop functions of the experiment. Provide the floor color seen by the Thymio ground sensors (floor source="loop").
 *
 * The arena is a square of side `arena_side` centered in the origin, X pointing right and Y pointing up. The floor is:
 * - a white vertical band of `white_width` meters around X = 0, spanning the whole arena from top to bottom;
 * - a black circle (the nest) of radius `nest_radius` centered in (`nest_x`, 0), on the left side;
 * - on the left of the white band, a radial gradient centered in the nest that goes from black (at the nest border)
 *   to gray (at the left-side point farthest from the nest), so that every left-side point leads to the nest;
 * - uniform gray on the right of the white band.
 */
class CExperimentLoopFunctions : public argos::CLoopFunctions
{
    public:
        void Init(argos::TConfigurationNode& t_node) override;
        argos::CColor GetFloorColor(const argos::CVector2& c_position_on_plane) override;

    private:
        static constexpr argos::UInt8 GRAY_LEVEL = 128;

        argos::Real m_fArenaSide = 5.0;
        argos::Real m_fWhiteWidth = 0.5;
        argos::Real m_fNestRadius = 0.35;
        argos::Real m_fNestX = -1.8;
        /* Distance from the nest center of the left-side point farthest from it (computed in Init) */
        argos::Real m_fGradientEnd = 0.0;
};

#endif
