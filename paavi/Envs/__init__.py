from gym.envs.registration import register
from gym import make

from smarts.core.agent_interface import AgentType
from smarts.core.agent_interface import AgentInterface, AgentType

from paavi.Agents import agents, build

register(
    id="sb3hiway-v0",
    entry_point="paavi.Envs.sb3_hiway_env:sb3HiWayEnv",
)


def build_env(config, **kwargs):

    AGENT_IDS = ["Agent-007"]  #    ["Agent-007", "Agent-009"]
    if "vehicle_type" in kwargs:
        AGENT_TYPES = (
            [AgentType.Imitation]
            if kwargs["vehicle_type"] == "pedestrian"
            else [AgentType.Laner]
        )
        AGENT_BUILDERS = (
            [agents.HumanKeyboardAgent]
            if kwargs["vehicle_type"] == "pedestrian"
            else [agents.random_agent]
        )
    else:
        AGENT_TYPES = [AgentType.Laner]
        AGENT_BUILDERS = [agents.simple_agent]

    config["agent_specs"] = build.build_agents(
        AGENT_IDS, AGENT_TYPES, AGENT_BUILDERS, **kwargs
    )

    # config["agent_specs"][AGENT_IDS[0]].agent_builder.STOP_DIST=config["stop_dist_rwd"]

    # if config["load_path"] is None:

    env = make(
        # "smarts.env:hiway-v0",
        "paavi.Envs:sb3hiway-v0",
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
        # envision_endpoint="ws://localhost:8080/simulations",  # dev server
        envision_endpoint=None,
        envision_record_data_replay_path=config["record_path"],
        zoo_addrs=None,
        stop_dist_rwd=config["stop_dist_rwd"],
    )  # else:
    #     env = None

    return env
