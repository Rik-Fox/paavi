import logging
import numpy as np

from smarts.core.utils.episodes import episodes

from paavi.Agents import ALGOS, build
from paavi.Envs import build_env

logging.basicConfig(level=logging.INFO)


def closeset_ped_dist(env):
    ped_obs, _, _, _ = env._smarts._agent_manager.observe(env._smarts)

    if env.agent_keys[0] not in ped_obs.keys():
        return None

    nearest_ped = 1e6
    for agent in ped_obs.keys():
        if agent == env.agent_keys[0]:
            continue

        ped_dist = np.linalg.norm(
            ped_obs[agent].ego_vehicle_state.position
            - ped_obs[env.agent_keys[0]].ego_vehicle_state.position
        )

        if ped_dist < nearest_ped:
            nearest_ped = ped_dist

    return nearest_ped


def eval(agent, env, num_episodes, stop_dist):
    import time

    time.sleep(5)
    ped_dist_data = []
    for episode in range(num_episodes):
        print("Episode => ", episode)
        observations = env.reset()
        dones = False
        while not dones:
            action, _ = agent.predict(observations)
            observations, rewards, done, infos = env.step(action)
            dones["__all__"] = done
            episode.record_step(observations, rewards, dones, infos)

            ped_dist_data.append(closeset_ped_dist(env))
            observations, rewards, dones, infos = env.step(action)

        # input("Press Enter to end")

    try:
        np.savetxt(
            f"{agent.tensorboard_log}/stop_dist_{stop_dist}_data.csv",
            np.array(ped_dist_data),
            delimiter=",",
            fmt="%s",
        )
    except FileNotFoundError:
        open(f"{agent.tensorboard_log}/stop_dist_{stop_dist}_data.csv", "a").close()
        np.savetxt(
            f"{agent.tensorboard_log}/stop_dist_{stop_dist}_data.csv",
            np.array(ped_dist_data),
            delimiter=",",
            fmt="%s",
        )
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

    eval(model, env, config["num_eps"], config["stop_dist_rwd"])
