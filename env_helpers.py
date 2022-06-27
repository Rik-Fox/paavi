import json
import numpy as np


class env_data_grabber(object):
    def __init__(self, env, auto_episode_recording=False):
        self.data = {
            "vehicle_position": [],
            "pedestrian_position": [],
            "veh2ped_distance": [],
        }
        self.auto = auto_episode_recording
        self.env = env
        self.vpos_ts = []
        self.ppos_ts = []
        self.d_ts = []

    def _sim_obs(self):
        sim_obs, _, _, _ = self.env._smarts._agent_manager.observe(self.env._smarts)
        return sim_obs

    def sim_obs(self):
        return self._sim_obs()

    def record_step(self, done, info):

        if done:
            if info[[*self.env.agent_specs][0]]["env_obs"].events.collisions:
                self.d_ts.append(-1)
            if self.auto:
                self.record_episode()
            return

        obs = self.sim_obs()

        veh = self.env.agent_keys[0]
        if veh not in obs.keys():
            self.vpos_ts.append(None)
            return
        else:
            veh_pos = obs[veh].ego_vehicle_state.position
            self.vpos_ts.append(list(veh_pos))

            ped = [*obs.keys()].pop([*obs.keys()] != veh)
            ped_pos = obs[ped].ego_vehicle_state.position
            self.ppos_ts.append(list(ped_pos))

            self.d_ts.append(np.linalg.norm(ped_pos - veh_pos))

    def record_episode(self):

        self.data["vehicle_position"].append(self.vpos_ts)
        self.data["pedestrian_position"].append(self.ppos_ts)
        self.data["veh2ped_distance"].append(self.d_ts)
        self.vpos_ts = []
        self.ppos_ts = []
        self.d_ts = []

    # for multiple pedestrians
    # def closeset_ped_dist(env):
    #     sim_obs, _, _, _ = env._smarts._agent_manager.observe(env._smarts)

    #     if env.agent_keys[0] not in sim_obs.keys():
    #         return None

    #     nearest_ped = 1e6
    #     vehicle_position = sim_obs[env.agent_keys[0]].ego_vehicle_state.position
    #     for agent in sim_obs.keys():
    #         if agent == env.agent_keys[0]:
    #             continue

    #         ped_pos = sim_obs[agent].ego_vehicle_state.position
    #         ped_dist = np.linalg.norm(ped_pos - vehicle_position)

    #         if ped_dist < nearest_ped:
    #             nearest_ped = ped_dist

    #     return nearest_ped

    # nearest_ped.append(closeset_ped_dist(env))
    # if done:
    #     if infos[[*env.agent_specs][0]]["env_obs"].events.collisions:
    #         # print(infos[[*env.agent_specs][0]]["env_obs"].events.collisions)
    #         nearest_ped[-1] = -1
    #     else:
    #         nearest_ped.pop()

    def save(self, log_dir, config, save_type="json"):
        if save_type == "json":
            self._save_to_json(log_dir, config)
        else:
            raise (ValueError("Only json output currently supported"))

    def _save_to_json(self, log_dir, config):
        for data_name, data_set in self.data.items():
            try:
                with open(
                    f"{log_dir}/{data_name}/SD{config['stop_dist_rwd']}_seed{config['seed']}.json",
                    "w",
                ) as myfile:
                    json.dump(data_set, myfile)

            except FileNotFoundError:
                import os

                os.makedirs(f"{log_dir}/{data_name}", exist_ok=True)

                open(
                    f"{log_dir}/{data_name}/SD{config['stop_dist_rwd']}_seed{config['seed']}.json",
                    "a",
                ).close()

                with open(
                    f"{log_dir}/{data_name}/SD{config['stop_dist_rwd']}_seed{config['seed']}.json",
                    "w",
                ) as myfile:
                    json.dump(data_set, myfile)