from typing import Sequence

from smarts.core.agent import Agent, AgentSpec
from smarts.core.agent_interface import AgentType, AgentInterface
from smarts.core.sensors import Observation

import numpy as np
from gym import spaces

#     * `ActionSpaceType.Continuous`: continuous action space with throttle, brake, absolute steering angle.
# It is a tuple of `throttle` [0, 1], `brake` [0, 1], and `steering` [-1, 1].

# * `ActionSpaceType.ActuatorDynamic`: continuous action space with throttle, brake, steering rate.
# Steering rate means the amount of steering angle change *per second*
# (either positive or negative) to be applied to the current steering angle.
# It is also a tuple of `throttle` [0, 1], `brake` [0, 1], and `steering_rate`,
# where steering rate is in number of radians per second.

# * `ActionSpaceType.Lane`: discrete lane action space of *strings* including
# "keep_lane",  "slow_down", "change_lane_left", "change_lane_right" as of version 0.3.2b,
# but a newer version will soon be released. In this newer version,
# the action space will no longer consist of strings, but will be a tuple of an integer for `lane_change`
# and a float for `target_speed`.

# Agent interface types

# Buddha = 0
# """Agent sees nothing and does nothing"""

# Full = 1
# """All observations and continuous action space"""

# Standard = 2
# """Minimal observations for dealing with waypoints and other vehicles and
# continuous action space.
# """

# Laner = 3
# """Agent sees waypoints and performs lane actions"""

# Loner = 4
# """Agent sees waypoints and performs continuous actions"""

# Tagger = 5
# """Agent sees waypoints, other vehicles, and performs continuous actions"""

# StandardWithAbsoluteSteering = 6
# """Agent sees waypoints, neighbor vehicles and performs continuous action"""
# action = [throttle(float), brake(float), steering_angle(float)]

# LanerWithSpeed = 7
# """Agent sees waypoints and performs speed and lane action"""
# action = [speed(float), laneChange([-1,0,1])]

# Tracker = 8
# """Agent sees waypoints and performs target position action"""

# Boid = 9
# """Controls multiple vehicles"""

# MPCTracker = 10
# """Agent performs trajectory tracking using model predictive control."""


class KeepLaneAgent(Agent):  # Laner
    def act(self, obs):
        return "keep_lane"


class ChaseViaPointsAgent(Agent):  # LanerWithSpeed
    def act(self, obs: Observation):
        if (
            len(obs.via_data.near_via_points) < 1
            or obs.ego_vehicle_state.edge_id != obs.via_data.near_via_points[0].edge_id
        ):
            return (obs.waypoint_paths[0][0].speed_limit, 0)

        nearest = obs.via_data.near_via_points[0]
        if nearest.lane_index == obs.ego_vehicle_state.lane_index:
            return (nearest.required_speed, 0)

        return (
            nearest.required_speed,
            1 if nearest.lane_index > obs.ego_vehicle_state.lane_index else -1,
        )


from pynput.keyboard import Key, Listener


class HumanKeyboardAgent(Agent):  # StandardWithAbsoluteSteering
    def __init__(self):
        # initialize the keyboard listener
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        # Parameters for the human-keyboard agent
        # you need to change them to suit the scenario
        # These values work the best with zoo_intersection

        self.INC_THROT = 0.01
        self.INC_STEER = 5.0

        self.MAX_THROTTLE = 0.6
        self.MIN_THROTTLE = 0.45

        self.MAX_BRAKE = 1.0
        self.MIN_BRAKE = 0.0

        self.MAX_STEERING = 1.0
        self.MIN_STEERING = -1.0

        self.THROTTLE_DISCOUNTING = 0.99
        self.BRAKE_DISCOUNTING = 0.95
        self.STEERING_DISCOUNTING = 0.9

        # initial values
        self.steering_angle = 0.0
        self.throttle = 0.48
        self.brake = 0.0

    def on_press(self, key):
        """To control, use the keys:
        Up: to increase the throttle
        Left Alt: to increase the brake
        Left: to decrease the steering angle
        Right: to increase the steering angle
        """

        if key == Key.up:
            self.throttle = min(self.throttle + self.INC_THROT, self.MAX_THROTTLE)
        elif key == Key.alt_l:
            self.brake = min(self.brake + 10.0 * self.INC_THROT, self.MAX_BRAKE)
        elif key == Key.right:
            self.steering_angle = min(
                self.steering_angle + self.INC_STEER, self.MAX_STEERING
            )
        elif key == Key.left:
            self.steering_angle = max(
                self.steering_angle - self.INC_STEER, self.MIN_STEERING
            )

    def act(self, obs):
        # discounting ..
        self.throttle = max(
            self.throttle * self.THROTTLE_DISCOUNTING, self.MIN_THROTTLE
        )
        self.steering_angle = self.steering_angle * self.STEERING_DISCOUNTING
        self.brake = self.brake * self.BRAKE_DISCOUNTING
        # send the action
        self.action = [self.throttle, self.brake, self.steering_angle]
        return self.action


class simple_agent(Agent):
    def __init__(self) -> None:
        super().__init__()

    OBSERVATION_SPACE = spaces.Box(0.0, np.inf, shape=(5,))

    def act(self, obs: Observation):
        pass

    def observation_adaptor(env_obs: Observation):
        return np.hstack(
            [
                np.array(env_obs.ego_vehicle_state.position),
                np.array(env_obs.ego_vehicle_state.speed),
                np.array(env_obs.ego_vehicle_state.lane_index),
            ]
        )


def config_agents(
    agent_ids: Sequence[str],
    agent_types: Sequence[AgentType],
    agent_builders: Sequence,
    **kwargs,
):

    if len(agent_types) == 1:
        agent_types = [agent_types[0] for i in range(len(agent_ids))]

    if len(agent_builders) == 1:
        agent_builders = [agent_builders[0] for i in range(len(agent_ids))]

    assert len(agent_types) == len(
        agent_ids
    ), "Number of AGENT_TYPES must either be 1 or match number of AGENT_IDS"
    assert len(agent_builders) == len(
        agent_ids
    ), "Number of AGENT_BUILDERS must either be 1 or match number of AGENT_IDS"

    agent_specs = {
        agent_id: AgentSpec(
            interface=AgentInterface.from_type(agent_type, **kwargs),
            agent_params={
                # "path_to_model": Path(__file__).resolve().parent / "model",
                "observation_space": agent_builder.OBSERVATION_SPACE,
            },
            agent_builder=agent_builder,
            observation_adapter=agent_builder.observation_adaptor,
            # reward_adapter=reward_adapter,
            # action_adapter=action_adapter,
        )
        for agent_id, agent_type, agent_builder in zip(
            agent_ids, agent_types, agent_builders
        )
    }
    # agent_spec.interface.vehicle_type = "motorcycle"

    return agent_specs


def config_open_agents(debug=False, aggressiveness=3):

    import importlib

    try:
        open_agent = importlib.import_module("open_agent")
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            f"Ensure that the open-agent has been installed with `pip install open-agent"
        )

    open_agent_spec = open_agent.entrypoint(debug, aggressiveness)

    return open_agent_spec
