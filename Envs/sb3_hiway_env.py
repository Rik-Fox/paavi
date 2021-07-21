from smarts.core.sensors import Observation
from smarts.env.hiway_env import HiWayEnv
from gym import spaces
import numpy as np
import os
import shutil


class sb3HiWayEnv(HiWayEnv):
    """
    Wrapper for smarts HiWayEnv that creates action and observation spaces from agent specs information,
    required for stable baselines 3 training procedure.
    XXX: will add anything else nessary here in ad hoc fashion
    """

    def __init__(
        self,
        scenarios,
        agent_specs,
        sim_name=None,
        shuffle_scenarios=True,
        headless=False,
        visdom=False,
        timestep_sec=0.1,
        seed=42,
        num_external_sumo_clients=0,
        sumo_headless=True,
        sumo_port=None,
        sumo_auto_start=True,
        endless_traffic=True,
        envision_endpoint=None,
        envision_record_data_replay_path=None,
        zoo_addrs=None,
    ):

        super().__init__(
            scenarios,
            agent_specs,
            sim_name=sim_name,
            shuffle_scenarios=shuffle_scenarios,
            headless=headless,
            visdom=visdom,
            timestep_sec=timestep_sec,
            seed=seed,
            num_external_sumo_clients=num_external_sumo_clients,
            sumo_headless=sumo_headless,
            sumo_port=sumo_port,
            sumo_auto_start=sumo_auto_start,
            endless_traffic=endless_traffic,
            envision_endpoint=envision_endpoint,
            envision_record_data_replay_path=envision_record_data_replay_path,
            zoo_addrs=zoo_addrs,
        )

        self.agent_keys = [
            *agent_specs
        ]  # [*agent_specs] is same as list(dict.keys()), but faster

        #####################################################
        # raw observation is a dict of agents with observation
        # object that contains everything below,
        # spaces much match what is returned in steo
        #####################################################

        # events a NamedTuple with the following fields:

        #         collisions - collisions the vehicle has been involved with other vehicles (if any)

        #         off_road - True if the vehicle is off the road

        #         reached_goal - True if the vehicle has reached its goal

        #         reached_max_episode_steps - True if the vehicle has reached its max episode steps

        # ego_vehicle_state - a VehicleObservation NamedTuple for the ego vehicle with the following fields:

        #         id - a string identifier for this vehicle

        #         position - A 3D numpy array (x, y, z) of the center of the vehicle bounding box’s bottom plane

        #         bounding_box - BoundingBox data class for the length, width, height of the vehicle

        #         heading - vehicle heading in radians

        #         speed - agent speed in m/s

        #         steering - angle of front wheels in radians

        #         yaw_rate - rotational speed in radian per second

        #         lane_id - a globally unique identifier of the lane under this vehicle

        #         lane_index - index of the lane under this vehicle, right most lane has index 0 and the index increments to the left

        #         linear_velocity - A 3D numpy array of vehicle velocities in body coordinate frame

        #         angular_velocity - A 3D numpy array of angular velocity vector

        #         linear_acceleration - A 3D numpy array of linear acceleration vector (requires accelerometer sensor)

        #         angular_acceleration - A 3D numpy array of angular acceleration vector (requires accelerometer sensor)

        #         linear_jerk - A 3D numpy array of linear jerk vector (requires accelerometer sensor)

        #         angular_jerk - A 3D numpy array of angular jerk vector (requires accelerometer sensor)

        # neighborhood_vehicle_states - a list of VehicleObservation `NamedTuple`s, each with the following fields:

        #         position, bounding_box, heading, speed, lane_id, lane_index - the same as with ego_vehicle_state

        #####################################################

        # self.observation_space = spaces.Box(
        #     -np.inf, np.inf, shape=(27 * len(agent_specs), 1)
        # )
        # self.observation_space = spaces.Dict(
        #     {
        #         "position": spaces.Box(0, np.inf, shape=(3,)),
        #         "speed": spaces.Box(0.0, np.inf, shape=(1,)),
        #         "lane_index": spaces.Discrete(2),
        #     }
        # )

        self.observation_space = agent_specs[
            self.agent_keys[0]
        ].agent_builder.OBSERVATION_SPACE
        # self.observation_space = spaces.Box(0, np.inf, shape=(5,))

        self.action_space = agent_specs[self.agent_keys[0]].agent_builder.ACTION_SPACE
        # self.action_space = spaces.Discrete(4)

        # discrete actions that can be given to smarts
        if isinstance(self.action_space, spaces.Discrete):
            self.actions = [
                "keep_lane",
                "slow_down",
                "change_lane_left",
                "change_lane_right",
            ]

    # puts actions into dict to give to smarts,
    def step(self, agent_actions):

        # import pdb

        # pdb.set_trace()

        # ## memory error at ~10000 for with about 200GB of space if these logs not deleted
        # sumo_logs = os.path.expanduser("~/.smarts/_sumo_run_logs/")
        # if os.path.exists(sumo_logs):
        #     shutil.rmtree(sumo_logs)

        if isinstance(self.action_space, spaces.Discrete):
            if isinstance(agent_actions, np.int64):
                action_dict = {self.agent_keys[0]: self.actions[agent_actions]}
            else:
                # action_dict = {}
                # for i, agent_key in enumerate(self.agent_keys):
                #     action_dict[agent_key] = self.actions[agent_actions[i]]
                raise NotImplementedError
        else:
            raise NotImplementedError

        raw_observations, raw_rewards, raw_dones, raw_infos = super().step(action_dict)

        if isinstance(self.observation_space, spaces.Box):
            if len(self.agent_keys) == 1:
                observations = raw_observations[self.agent_keys[0]]
                rewards = raw_rewards[self.agent_keys[0]]
                dones = raw_dones[self.agent_keys[0]]
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

        # for agent in raw_observations.keys():
        #     obs = raw_observations[agent]
        #     observations = np.hstack(
        #         [
        #             np.array(obs.ego_vehicle_state.position),
        #             np.array(obs.ego_vehicle_state.speed),
        #             np.array(obs.ego_vehicle_state.lane_index),
        #         ]
        #     )

        return observations, rewards, dones, raw_infos

    # strips observations out of dict from smarts
    def reset(self):

        observations = super().reset()

        ## memory error at ~10000 for with about 200GB of space if these logs not deleted
        sumo_logs = os.path.expanduser("~/.smarts/_sumo_run_logs/")
        if os.path.exists(sumo_logs):
            shutil.rmtree(sumo_logs, ignore_errors=True)

        return np.hstack([observations[key] for key in self.agent_keys])
