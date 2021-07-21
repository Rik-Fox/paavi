import logging
from smarts.core.agent_interface import AgentType
from Agents import agents, build_algo
from Envs import build_env

# import pdb

logging.basicConfig(level=logging.INFO)

AGENT_IDS = ["Agent-007"]  #    ["Agent-007", "Agent-009"]
AGENT_TYPES = [AgentType.Laner]
AGENT_BUILDERS = [agents.simple_agent]


def main(config):

    config["agent_specs"] = agents.config_agents(
        AGENT_IDS,
        AGENT_TYPES,
        AGENT_BUILDERS,
        max_episode_steps=config["max_episode_steps"],
    )

    env = build_env(config)

    agent = build_algo(config, env=env)

    agent.learn(
        total_timesteps=config["n_timesteps"],
        tb_log_name=f'{config["algo"]}_{config["seed"]}',
    )
    agent.save(config["load"])


import os
from param_parsers import trainer_parser

if __name__ == "__main__":
    parser = trainer_parser("single-agent-experiment")

    parser.add_argument(
        "--max_episode_steps",
        default=None,
        help="If set, agents will become 'done' after this many steps. set to None to disable.",
    )
    parser.add_argument("--buffer_size", type=int, default=10000)
    parser.add_argument("--batch_size", type=int, default=1024)
    parser.add_argument("--load", type=str, default=None)
    parser.add_argument(
        "--log_dir",
        type=str,
        default=os.path.expanduser("~/paavi_logs/tb_training_logs/"),
    )

    args = parser.parse_args()

    config = vars(args)

    ### expilict values for vscode debugger

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
    #     "log_dir": os.path.expanduser("~/paavi_logs/tb_training_logs/"),
    #     "n_timesteps": 1e6,
    # }

    main(config)
