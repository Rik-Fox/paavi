import logging

import gym

from Models import zoo_trainer_parser

from smarts.core.agent_interface import AgentType

from util.util import ALGOS

from Agents.agents import *

logging.basicConfig(level=logging.INFO)

AGENT_IDS = ["Agent-007"]  #    ["Agent-007", "Agent-009"]
AGENT_TYPES = [AgentType.Laner]
AGENT_BUILDERS = [simple_agent]


def main(config):

    agent_specs = config_agents(
        AGENT_IDS,
        AGENT_TYPES,
        AGENT_BUILDERS,
        max_episode_steps=config["max_episode_steps"],
    )

    env = gym.make(
        # "smarts.env:hiway-v0",
        "Envs:sb3hiway-v0",
        scenarios=config["scenarios"],
        agent_specs=agent_specs,
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

    if config["algo"] == "qrdqn":
        policy_kwargs = dict(n_quantiles=50)
    else:
        policy_kwargs = None

    model = ALGOS[config["algo"]](
        "MlpPolicy",
        env,
        learning_rate=0.01,  # 5e-5,
        buffer_size=config["buffer_size"],
        train_freq=(1, "episode"),
        tensorboard_log="logs/",
        seed=config["seed"],
        batch_size=config["batch_size"],
        learning_starts=20000,
        target_update_interval=1000,
        exploration_fraction=0.005,
        exploration_initial_eps=1.0,
        exploration_final_eps=0.01,
        policy_kwargs=policy_kwargs,
        verbose=0,
    )

    # model = ALGOS[config["algo"]].load(
    #     f'Models/{config["algo"]}{config["batch_size"]}_ped_single'
    # )

    model.learn(
        total_timesteps=1000000, tb_log_name=f'{config["algo"]}_{config["seed"]}'
    )

    model.save(f'Models/{config["algo"]}{config["batch_size"]}_ped_single')


if __name__ == "__main__":
    parser = zoo_trainer_parser("single-agent-experiment")

    parser.add_argument(
        "--max_episode_steps",
        default=None,
        help="If set, agents will become 'done' after this many steps. set to None to disable.",
    )

    parser.add_argument("--buffer_size", type=int, default=10000)

    parser.add_argument("--batch_size", type=int, default=1024)

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
    #     "batch_size": 256,
    # }

    main(config)
