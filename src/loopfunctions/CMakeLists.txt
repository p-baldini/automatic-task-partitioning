# ARGoS loads this with library="loopfunctions/libloopfunctions.so" (resolved via ARGOS_PLUGIN_PATH=build)
add_library(loopfunctions MODULE
    loopfunctions.hpp
    loopfunctions.cpp
)

target_link_libraries(loopfunctions
    argos3core_simulator
)
