# Thymio robot plugin for ARGoS (simulator only), vendored from
# https://github.com/resilient-swarms/thymio -- see README.md in this folder.
#
# The library is placed directly in the build root so that ARGoS loads it at
# startup through ARGOS_PLUGIN_PATH (needed for the <Thymio> arena entity).

set(THYMIO_DIR argos3/plugins/robots/thymio)

set(THYMIO_SOURCES
  ${THYMIO_DIR}/control_interface/ci_thymio_ground_sensor.cpp
  ${THYMIO_DIR}/control_interface/ci_thymio_proximity_sensor.cpp
  ${THYMIO_DIR}/control_interface/ci_thymio_leds_actuator.cpp
  ${THYMIO_DIR}/control_interface/ci_thymio_acc_sensor.cpp
  ${THYMIO_DIR}/simulator/dynamics2d_thymio_model.cpp
  ${THYMIO_DIR}/simulator/thymio_entity.cpp
  ${THYMIO_DIR}/simulator/thymio_measures.cpp
  ${THYMIO_DIR}/simulator/thymio_ground_rotzonly_sensor.cpp
  ${THYMIO_DIR}/simulator/thymio_proximity_default_sensor.cpp
  ${THYMIO_DIR}/simulator/thymio_led_actuator.cpp
  ${THYMIO_DIR}/simulator/thymio_range_and_bearing_sensor.cpp
)

set(THYMIO_LIBRARIES
  argos3core_simulator
  argos3plugin_simulator_entities
  argos3plugin_simulator_media
  argos3plugin_simulator_genericrobot
  argos3plugin_simulator_dynamics2d
)

if(ARGOS_QTOPENGL_FOUND)
  list(APPEND THYMIO_SOURCES ${THYMIO_DIR}/simulator/qtopengl_thymio.cpp)
  list(APPEND THYMIO_LIBRARIES argos3plugin_simulator_qtopengl ${ARGOS_QTOPENGL_LIBRARIES})
endif()

add_library(argos3plugin_simulator_thymio SHARED ${THYMIO_SOURCES})

target_include_directories(argos3plugin_simulator_thymio PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(argos3plugin_simulator_thymio ${THYMIO_LIBRARIES} ${ARGOS_LDFLAGS})
# Third-party code: keep its warnings out of our build output
target_compile_options(argos3plugin_simulator_thymio PRIVATE -w)

set_target_properties(argos3plugin_simulator_thymio PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)
