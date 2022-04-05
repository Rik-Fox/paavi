<<<<<<< HEAD:paavi/Agents/agents.py
from smarts.core.agent import Agent
from smarts.core.sensors import Observation

import numpy as np
from gym import spaces


#     * `ActionSpaceType.Continuous`: continuous action space with throttle, brake, absolute steering angle.
# It is a tuple of `throttle` [0, 1], `brake` [0, 1], and `steering` [-1, 1].

# * `ActionSpaceType.ActuatorDynamic`: continuous action space with throttle, brake, steering rate.
# Steering rate means the amount of steering anconfiggle change *per second*
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
        return 0  # "keep_lane" is this index in discrete actionspace of new env


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

try:
    from pynput.keyboard import Key, Listener
except ImportError:
    # print("no keyboard agent as running headless")
    pass


class HumanKeyboardAgent(Agent):  # StandardWithAbsoluteSteering

    OBSERVATION_SPACE = spaces.Box(0.0, np.inf, shape=(5,))
    ACTION_SPACE = spaces.Discrete(4)  # this is a lie, needs correcting

    def __init__(self, vehicle_type="pedestrian") -> None:
        super().__init__()
        self.vehicle_type = vehicle_type

        # initialize the keyboard listener
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        # Parameters for the human-keyboard agent
        # you need to change them to suit the scenario

        self.INC_ACCEL = 1.0
        self.INC_STEER = np.pi / 4

        self.MAX_ACCEL = 5.0
        self.MIN_ACCEL = -5.0

        # self.MAX_BRAKE = 1.0
        # self.MIN_BRAKE = 0.0

        self.MAX_STEERING = np.pi
        self.MIN_STEERING = -np.pi

        # self.THROTTLE_DISCOUNTING = 0.99
        # self.BRAKE_DISCOUNTING = 0.95
        # self.STEERING_DISCOUNTING = 0.9

        # initial values
        self.steering_angle = 0.0
        self.accel = 0.0
        # self.brake = 0.0

    def on_press(self, key):
        """To control, use the keys:
        Up: to increase the throttle
        Down: to increase the brake
        Left: to decrease the steering angle
        Right: to increase the steering angle
        """

        if key == Key.up:
            self.accel = min(self.accel + self.INC_ACCEL, self.MAX_ACCEL)
        elif key == Key.down:
            self.accel = max(self.accel - self.INC_ACCEL, self.MIN_ACCEL)
        elif key == Key.right:
            self.steering_angle = max(
                self.steering_angle + self.INC_STEER, self.MAX_STEERING
            )
        elif key == Key.left:
            self.steering_angle = min(
                self.steering_angle - self.INC_STEER, self.MIN_STEERING
            )

    def act(self, obs):
        # discounting ..
        self.accel = max(self.accel, self.MIN_ACCEL)  # * self.THROTTLE_DISCOUNTING
        self.steering_angle = self.steering_angle  # * self.STEERING_DISCOUNTING
        # self.brake = self.brake * self.BRAKE_DISCOUNTING
        # send the action
        # print(self.accel)
        self.action = [self.accel, self.steering_angle]
        # reset steering angle, otherise will constantly turn in circles
        self.steering_angle = 0

        return self.action

    def observation_adaptor(env_obs: Observation):
        return np.hstack(
            [
                np.array(env_obs.ego_vehicle_state.position),
                np.array(env_obs.ego_vehicle_state.speed),
                np.array(env_obs.ego_vehicle_state.lane_index),
            ]
        )


class PedAgent(Agent):

    OBSERVATION_SPACE = spaces.Box(0.0, np.inf, shape=(5,))
    ACTION_SPACE = spaces.Discrete(4)

    def __init__(self, vehicle_type="pedestrian") -> None:
        super().__init__()
        self.vehicle_type = vehicle_type

    def act(self, obs: Observation):
        # acceleration is scalar in m/s^2, angular_velocity is scalar in rad/s
        # acceleration is in the direction of the heading only.
        a = np.random.rand() * 2
        theta = ((np.random.rand() * 2 * np.pi) - np.pi) / 8
        # theta = 0
        return [a, theta]

    def observation_adaptor(env_obs: Observation):
        return np.hstack(
            [
                np.array(env_obs.ego_vehicle_state.position),
                np.array(env_obs.ego_vehicle_state.speed),
                np.array(env_obs.ego_vehicle_state.lane_index),
            ]
        )


class simple_agent(Agent):

    OBSERVATION_SPACE = spaces.Box(0.0, np.inf, shape=(5,))
    ACTION_SPACE = spaces.Discrete(4)
    # STOP_DIST = None

    def __init__(self, vehicle_type="passenger") -> None:
        super().__init__()
        self.vehicle_type = vehicle_type

    def act(self, obs: Observation):
        print("should have a learning model that wraps this act -> no action taken")

    def observation_adaptor(env_obs: Observation):
        return np.hstack(
            [
                np.array(env_obs.ego_vehicle_state.position),
                np.array(env_obs.ego_vehicle_state.speed),
                np.array(env_obs.ego_vehicle_state.lane_index),
            ]
        )

    # def reward_adaptor(self, env_obs: Observation, reward):
    #     if self.STOP_DIST is None:
    #         return reward
    #     else:
    #         import pdb
    #         pdb.set_trace()



class random_agent(Agent):

    OBSERVATION_SPACE = spaces.Box(0.0, np.inf, shape=(5,))
    ACTION_SPACE = spaces.Discrete(4)

    def __init__(self, vehicle_type="passenger") -> None:
        super().__init__()
        self.vehicle_type = vehicle_type

    def act(self, obs: Observation):
        return np.random.choice([0, 1, 2, 3])

    def observation_adaptor(env_obs: Observation):
        return np.hstack(
            [
                np.array(env_obs.ego_vehicle_state.position),
                np.array(env_obs.ego_vehicle_state.speed),
                np.array(env_obs.ego_vehicle_state.lane_index),
            ]
=======
from smarts.core.agent import Agent
from smarts.core.sensors import Observation

import numpy as np
from gym import spaces


#     * `ActionSpaceType.Continuous`: continuous action space with throttle, brake, absolute steering angle.
# It is a tuple of `throttle` [0, 1], `brake` [0, 1], and `steering` [-1, 1].

# * `ActionSpaceType.ActuatorDynamic`: continuous action space with throttle, brake, steering rate.
# Steering rate means the amount of steering anconfiggle change *per second*
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
        return 0  # "keep_lane" is this index in discrete actionspace of new env


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

    OBSERVATION_SPACE = spaces.Box(0.0, np.inf, shape=(5,))
    ACTION_SPACE = spaces.Discrete(4)  # this is a lie, needs correcting

    def __init__(self, vehicle_type="pedestrian") -> None:
        super().__init__()
        self.vehicle_type = vehicle_type

        # initialize the keyboard listener
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        # Parameters for the human-keyboard agent
        # you need to change them to suit the scenario

        self.INC_ACCEL = 1.0
        self.INC_STEER = np.pi / 4

        self.MAX_ACCEL = 5.0
        self.MIN_ACCEL = -5.0

        # self.MAX_BRAKE = 1.0
        # self.MIN_BRAKE = 0.0

        self.MAX_STEERING = np.pi
        self.MIN_STEERING = -np.pi

        # self.THROTTLE_DISCOUNTING = 0.99
        # self.BRAKE_DISCOUNTING = 0.95
        # self.STEERING_DISCOUNTING = 0.9

        # initial values
        self.steering_angle = 0.0
        self.accel = 0.0
        # self.brake = 0.0

    def on_press(self, key):
        """To control, use the keys:
        Up: to increase the throttle
        Down: to increase the brake
        Left: to decrease the steering angle
        Right: to increase the steering angle
        """

        if key == Key.up:
            self.accel = min(self.accel + self.INC_ACCEL, self.MAX_ACCEL)
        elif key == Key.down:
            self.accel = max(self.accel - self.INC_ACCEL, self.MIN_ACCEL)
        elif key == Key.right:
            self.steering_angle = max(
                self.steering_angle + self.INC_STEER, self.MAX_STEERING
            )
        elif key == Key.left:
            self.steering_angle = min(
                self.steering_angle - self.INC_STEER, self.MIN_STEERING
            )

    def act(self, obs):
        # discounting ..
        self.accel = max(self.accel, self.MIN_ACCEL)  # * self.THROTTLE_DISCOUNTING
        self.steering_angle = self.steering_angle  # * self.STEERING_DISCOUNTING
        # self.brake = self.brake * self.BRAKE_DISCOUNTING
        # send the action
        # print(self.accel)
        self.action = [self.accel, self.steering_angle]
        # reset steering angle, otherise will constantly turn in circles
        self.steering_angle = 0

        return self.action

    def observation_adaptor(env_obs: Observation):
        return np.hstack(
            [
                np.array(env_obs.ego_vehicle_state.position),
                np.array(env_obs.ego_vehicle_state.speed),
                np.array(env_obs.ego_vehicle_state.lane_index),
            ]
        )


class PedAgent(Agent):

    OBSERVATION_SPACE = spaces.Box(0.0, np.inf, shape=(5,))
    ACTION_SPACE = spaces.Discrete(4)

    def __init__(self, vehicle_type="pedestrian") -> None:
        super().__init__()
        self.vehicle_type = vehicle_type

    def act(self, obs: Observation):
        # acceleration is scalar in m/s^2, angular_velocity is scalar in rad/s
        # acceleration is in the direction of the heading only.
        a = np.random.rand() * 2
        theta = ((np.random.rand() * 2 * np.pi) - np.pi) / 8
        # theta = 0
        return [a, theta]

    def observation_adaptor(env_obs: Observation):
        return np.hstack(
            [
                np.array(env_obs.ego_vehicle_state.position),
                np.array(env_obs.ego_vehicle_state.speed),
                np.array(env_obs.ego_vehicle_state.lane_index),
            ]
        )


class simple_agent(Agent):

    OBSERVATION_SPACE = spaces.Box(0.0, np.inf, shape=(5,))
    ACTION_SPACE = spaces.Discrete(4)

    def __init__(self, vehicle_type="passenger") -> None:
        super().__init__()
        self.vehicle_type = vehicle_type

    def act(self, obs: Observation):
        print("should have a learning model that wraps this act -> no action taken")

    def observation_adaptor(env_obs: Observation):
        return np.hstack(
            [
                np.array(env_obs.ego_vehicle_state.position),
                np.array(env_obs.ego_vehicle_state.speed),
                np.array(env_obs.ego_vehicle_state.lane_index),
            ]
        )


class random_agent(Agent):

    OBSERVATION_SPACE = spaces.Box(0.0, np.inf, shape=(5,))
    ACTION_SPACE = spaces.Discrete(4)

    def __init__(self, vehicle_type="passenger") -> None:
        super().__init__()
        self.vehicle_type = vehicle_type

    def act(self, obs: Observation):
        return np.random.choice([0, 1, 2, 3])

    def observation_adaptor(env_obs: Observation):
        return np.hstack(
            [
                np.array(env_obs.ego_vehicle_state.position),
                np.array(env_obs.ego_vehicle_state.speed),
                np.array(env_obs.ego_vehicle_state.lane_index),
            ]
>>>>>>> branch:Agents/agents.py
        )