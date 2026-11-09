# Individual Online Learning in Robot Swarms with Task Specialization

*Author: Paolo Baldini*
*Possible venues: Autonomous Robots, Robotics and Autonomous Systems, Swarm and Evolutionary Computation, IROS (upcoming)*

This experiment builds on previous work concerning the individual, communication-free, online adaptation of robots in a swarm subject to a dynamic environment.
That work demonstrated that collective behaviour can be achieved through individual adaptation; however, it also highlighted how such process can only succeed if the performance in the task can be inferred from the individual performance of the robot.
With this experiment, we demonstrate that introducing communication permits to address a class of problems for which the collective performance cannot be deduced from the individual one.
An example is that of *foraging*, in which some robots may not receive rewards for their actions but remain essentials for task completition.

## Run the experiment

Use the following command(s) to run the experiment:

```bash
pixi run experiment
```

## Packages

In the following, you can find a description of each package and/or module of the experiment:

- `src/loopfunctions`: ARGoS loop functions of the experiment, which set the floor color seen by the Thymio ground sensors (a light gray arena disc on a darker gray floor).
- `src/ros_evaluation`: ROS 2 node (one per robot) that will evaluate the robot's performance during the experiment (placeholder, not yet implemented).
- `src/ros_experiment`: ROS 2 launch package; starts ARGoS, one gossip, policy and evaluation node per robot (namespace `thymio_<i>`).
- `src/ros_gossip`: ROS 2 node that will handle communication between robots (placeholder, not yet implemented).
- `src/ros_policy`: ROS 2 node that will host the robot's control policy (placeholder, not yet implemented).
- `src/ros_thymio`: ARGoS controller that exposes each simulated Thymio to ROS 2, publishing its sensor readings and subscribing to velocity commands.
- `src/thymio_model`: ARGoS plugin (vendored from [resilient-swarms/thymio](https://github.com/resilient-swarms/thymio)) that models the Thymio robot in simulation, with its sensors, actuators and physics. The plugin has been customized to simulate the only directional (front/rear) communication of the Thymio.
