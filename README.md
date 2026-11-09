# Individual Online Learning in Robot Swarms with Task Specialization

*Author: Paolo Baldini*

This experiment builds on previous work concerning the individual, communication-free, online adaptation of robots in a swarm subject to a dynamic environment.
That work demonstrated that collective behaviour can be achieved through individual adaptation; however, it also highlighted how such process can only succeed if the performance in the task can be inferred from the individual performance of the robot.
With this experiment, we demonstrate that introducing communication permits to address a class of problems for which the collective performance cannot be deduced from the individual one.
An example is that of *foraging*, in which some robots may not receive rewards for their actions but remain essentials for task completition.

## Packages

In the following, you can find a description of each package and/or module of the experiment:

- `src/loopfunctions`: ARGoS loop functions of the experiment, which set the floor color seen by the Thymio ground sensors (a light gray arena disc on a darker gray floor).
- `src/ros_thymio`: ARGoS controller that exposes each simulated Thymio to ROS 2, publishing its sensor readings and subscribing to velocity commands.
- `src/thymio_model`: ARGoS plugin (vendored from [resilient-swarms/thymio](https://github.com/resilient-swarms/thymio)) that models the Thymio robot in simulation, with its sensors, actuators and physics.
