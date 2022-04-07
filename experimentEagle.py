import logging
import json
import numpy as np
import pdb

from smarts.core.utils.episodes import episodes

from paavi.Agents import ALGOS, build
from paavi.Envs import build_env

logging.basicConfig(level=logging.INFO)


class env_data_grabber(object):
    def __init__(self, env):
        self.data = {
            "vehicle_position": [],
            "pedestrian_position": [],
            "veh2ped_distance": [],
        }
        self.env = env
        self.vpos_ts = []
        self.ppos_ts = []
        self.d_ts = []

    def _sim_obs(self):
        sim_obs, _, _, _ = self.env._smarts._agent_manager.observe(env._smarts)
        return sim_obs

    def sim_obs(self):
        return self._sim_obs

    def record_step(self):

        obs = self.sim_obs

        veh = self.env.agent_keys[0]
        if veh not in obs.keys():
            self.vpos_ts.append(None)
        else:
            veh_pos = obs[veh].ego_vehicle_state.position
            self.vpos_ts.append(veh_pos)

        ped = [*obs.keys()].remove(veh)

        veh_pos = obs[veh].ego_vehicle_state.position
        ped_pos = obs[ped].ego_vehicle_state.position

        return veh_pos, ped_pos, np.linalg.norm(ped_pos - veh_pos)

    # for multiple pedestrians
    def closeset_ped_dist(env):
        sim_obs, _, _, _ = env._smarts._agent_manager.observe(env._smarts)

        if env.agent_keys[0] not in sim_obs.keys():
            return None

        nearest_ped = 1e6
        vehicle_position = sim_obs[env.agent_keys[0]].ego_vehicle_state.position
        for agent in sim_obs.keys():
            if agent == env.agent_keys[0]:
                continue

            ped_pos = sim_obs[agent].ego_vehicle_state.position
            ped_dist = np.linalg.norm(ped_pos - vehicle_position)

            if ped_dist < nearest_ped:
                nearest_ped = ped_dist

        return nearest_ped

        # nearest_ped.append(closeset_ped_dist(env))
        # if done:
        #     if infos[[*env.agent_specs][0]]["env_obs"].events.collisions:
        #         # print(infos[[*env.agent_specs][0]]["env_obs"].events.collisions)
        #         nearest_ped[-1] = -1
        #     else:
        #         nearest_ped.pop()

    def _save_to_json(data, agent, config):
        for data_name, data_set in data.items():
            try:
                with open(
                    f"{agent.tensorboard_log}/{data_name}/SD{config['stop_dist_rwd']}_seed{config['seed']}.json",
                    "w",
                ) as myfile:
                    json.dump(data_set, myfile)

            except FileNotFoundError:
                open(
                    f"{agent.tensorboard_log}/{data_name}/SD{config['stop_dist_rwd']}_seed{config['seed']}.json",
                    "a",
                ).close()

                with open(
                    f"{agent.tensorboard_log}/{data_name}/SD{config['stop_dist_rwd']}_seed{config['seed']}.json",
                    "w",
                ) as myfile:
                    json.dump(data_set, myfile)


def eval(agent, env, config):
    import time

    time.sleep(5)
    data = {"vehicle_position": [], "pedestrian_position": [], "veh2ped_distance": []}
    for episode in range(config["num_eps"]):
        print("Episode => ", episode)
        observations = env.reset()
        done = False
        v_ts, p_ts, d_ts = [], [], []
        while not done:
            action, _ = agent.predict(observations)
            observations, rewards, done, infos = env.step(action)
            v, p, d = env_data_grabber(env)
            v_ts.append(v)
            p_ts.append(p)
            d_ts.append(d)
            if done:
                if infos[[*env.agent_specs][0]]["env_obs"].events.collisions:
                    # print(infos[[*env.agent_specs][0]]["env_obs"].events.collisions)
                    v_ts.pop()
                    p_ts.pop()
                    d_ts[-1] = -1
                else:
                    v_ts.pop()
                    p_ts.pop()
                    d_ts.pop()

        data["ped_distance_data"].append(d_ts)

        # input("Press Enter to end")

    save_to_json(data, agent, config)

    # env.close()


if __name__ == "__main__":
    from paavi.util.param_parsers import eval_parser
    import os

    parser = eval_parser("eval_env")

    config = vars(parser.parse_args())

    env = build_env(config)

    if config["load_path"] == None:
        from paavi.Agents import build

        model = build.build_algo(config, env)
    else:
        model = ALGOS[config["algo"]].load(config["load_path"], env=env)  # env=None

    # manually set tensorboard_log incase model wasn't initally logging there
    model.tensorboard_log = config["log_dir"]

    if config["record_path"] is not None:
        os.makedirs(config["record_path"], exist_ok=True)

    eval(model, env, config)
