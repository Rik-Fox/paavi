import logging
import os
import time
from stable_baselines3.common.monitor import Monitor
from smarts.core.agent_interface import AgentType
from Agents import agents, build
from Envs import build_env
from custom_logging import CustomTrackingCallback

# import pdb

logging.basicConfig(level=logging.INFO)

AGENT_IDS = ["Agent-007"]  #    ["Agent-007", "Agent-009"]
AGENT_TYPES = [AgentType.Laner]
AGENT_BUILDERS = [agents.simple_agent]


def main(config):    

    monitor_path = os.path.join(config["log_dir"], "Monitor_logs")
    run_name = f'{config["algo"]}_seed{config["seed"]}_batchsize{config["batch_size"]}_env_{config["scenarios"][0].split("/")[1]}'

    config["agent_specs"] = build.build_agents(
        AGENT_IDS,
        AGENT_TYPES,
        AGENT_BUILDERS,
        max_episode_steps=config["max_episode_steps"],
    )
    
    env = Monitor(build_env(config), filename=os.path.join(monitor_path, f"{run_name}_monitor.csv"))

    agent = build.build_algo(config, env=env)

    agent.learn(
        total_timesteps=config["n_timesteps"],
        tb_log_name=f'{config["algo"]}_{config["seed"]}',
        callback=CustomTrackingCallback(check_freq=100, log_dir=monitor_path, run_name=run_name, start_time =time.time(), verbose=1),
    )

    agent.save(os.path.join(monitor_path, f'{run_name}_final'))


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
    #     "log_dir": path.expanduser("~/paavi_logs/"),
    #     "n_timesteps": 1e6,
    # }

    main(config)
