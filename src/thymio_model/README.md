# Thymio plugin for ARGoS (vendored)

Simulator-only subset of the Thymio robot plugin by Sina Sarparast and Danesh Tarapore.

- Upstream: https://github.com/resilient-swarms/thymio
- Commit: `5fe22bbd8107554489e21f17c937fd991e096e4e` (2025-06-11)
- License: MIT (see `LICENSE`)

We kept only `control_interface/` and the `simulator/` sources that upstream compiles.
`real_robot/`, the Aseba interface and the test programs are left out. The layout under
`argos3/plugins/robots/thymio/` mirrors upstream, so that the upstream
`#include <argos3/plugins/robots/thymio/...>` lines resolve.

## What it provides

| XML | Kind | Notes |
|---|---|---|
| `<Thymio id rab_range rab_data_size>` | entity | `rab_range` defaults to 0.8 m, `rab_data_size` to 2 bytes |
| `<Thymio_proximity implementation="default">` | sensor | 7 readings in [0,1]: [0..4] front left to front right, [5] rear left, [6] rear right. `range` defaults to 0.11 m. Also accepts the generic `noise_level` and `show_rays` attributes |
| `<Thymio_ground implementation="rot_z_only">` | sensor | 2 grayscale readings: [0] left, [1] right. Needs a `<floor>` in the arena |
| `<thymio_led implementation="default">` | actuator | |

The generic `differential_steering` and `range_and_bearing` sensors and actuators also work with it.
The kinematic wheel distance is 0.08 m (`Thymio_WHEEL_DISTANCE`).

## Local changes

Each change is marked `LOCAL CHANGE` in the source.

1. `simulator/dynamics2d_thymio_model.cpp`: upstream's collision polygon was rotated by 90°, with its
   rounded front along +Y. The ARGoS forward axis is +X, and that is where the sensors, LEDs and
   OpenGL model are. The polygon now matches the OpenGL body outline. Also frees the vertex buffer.
2. `simulator/thymio_measures.cpp`: the ground sensor offsets were (-0.05, -0.01) and (0.05, -0.01),
   which put one sensor at the rear. They are now (0.05, ±0.0115), both at the front, taken from
   [enki](https://github.com/enki-community/enki/blob/master/enki/robots/thymio2/Thymio2.cpp)
   (7.2, ±1.15) cm with the same frame shift as the proximity sensors.
3. `control_interface/ci_thymio_proximity_sensor.cpp`: the `Angle` metadata of the proximity
   readings had the wrong sign compared to where the sensors actually are (reading 0 is front-left,
   +0.698 rad).
