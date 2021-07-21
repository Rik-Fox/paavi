from gym.envs.registration import register
from gym import make

register(
    id="sb3hiway-v0",
    entry_point="Envs.sb3_hiway_env:sb3HiWayEnv",
)


def build_env(config):

    if config["load"] is None:
        env = make(
            # "smarts.env:hiway-v0",
            "Envs:sb3hiway-v0",
            scenarios=config["scenarios"],
            agent_specs=config["agent_specs"],
            sim_name=config["sim_name"],
            headless=config["headless"],
            timestep_sec=0.1,
            seed=config["seed"],
            shuffle_scenarios=True,
            visdom=False,
            num_external_sumo_clients=0,
            sumo_headless=True,
            sumo_port=None,
            sumo_auto_start=True,
            endless_traffic=True,
            envision_endpoint=None,
            envision_record_data_replay_path=None,
            zoo_addrs=None,
        )
    else:
        env = None

    return env
