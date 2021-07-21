import logging
from smarts.core.agent_interface import AgentType
from Agents import agents, build
from Envs import build_env

# import pdb

logging.basicConfig(level=logging.INFO)

AGENT_IDS = ["Agent-007"]  #    ["Agent-007", "Agent-009"]
AGENT_TYPES = [AgentType.Laner]
AGENT_BUILDERS = [agents.simple_agent]


def main(config):

    config["agent_specs"] = build.build_agents(
        AGENT_IDS,
        AGENT_TYPES,
        AGENT_BUILDERS,
        max_episode_steps=config["max_episode_steps"],
    )

    env = build_env(config)

    agent, save_path = build.build_algo(config, env=env)

    agent.learn(
        total_timesteps=config["n_timesteps"],
        tb_log_name=f'{config["algo"]}_{config["seed"]}',
    )
    agent.save(save_path)


if __name__ == "__main__":
    from param_parsers import trainer_parser

    parser = trainer_parser("single-agent-experiment")

    config = vars(parser.parse_args())

    ### expilict values for vscode debugger
    # from os import path
    # config = {
    #     "scenarios": ["Envs/ped_single"],
    #     "sim_name": None,
    #     "headless": True,
    #     "num_episodes": 3,
    #     "seed": 42,
    #     "algo": "qrdqn",
    #     "max_episode_steps": None,
    #     "buffer_size": 1024,
    #     "batch_size": 256,
    #     "load": None,  # "Models/qrdqn256_ped_single",
    #     "log_dir": path.expanduser("~/paavi_logs/tb_training_logs/"),
    #     "n_timesteps": 1e6,
    # }

    main(config)
