## take parser args from SMARTS examples then add args from both zoo's train.py and custom defined
import argparse
from os import path
from util.util import StoreDict
from Agents import ALGOS


def default_argument_parser(program: str):
    """This factory method returns a vanilla `argparse.ArgumentParser` with the
    minimum subset of arguments that should be supported.
    You can extend it with more `parser.add_argument(...)` calls or obtain the
    arguments via `parser.parse_args()`.
    """
    parser = argparse.ArgumentParser(program)
    parser.add_argument(
        "scenarios",
        help="A list of scenarios. Each element can be either the scenario to run "
        "(see scenarios/ for some samples you can use) OR a directory of scenarios "
        "to sample from.",
        type=str,
        nargs="+",
    )
    parser.add_argument(
        "--sim-name",
        help="a string that gives this simulation a name.",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--headless", help="Run the simulation in headless mode.", action="store_true"
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--sumo-port", help="Run SUMO with a specified port.", type=int, default=None
    )
    parser.add_argument(
        "--episodes",
        help="The number of episodes to run the simulation for.",
        type=int,
        default=10,
    )
    return parser


def trainer_parser(program: str):
    parser = default_argument_parser(program)

    ## zoo's arguments
    parser.add_argument(
        "--algo",
        help="RL Algorithm",
        default="dqn",
        type=str,
        required=False,
        choices=list(ALGOS.keys()),
    )
    parser.add_argument("--env", type=str, default="CartPole-v1", help="environment ID")
    parser.add_argument(
        "-tb", "--tensorboard-log", help="Tensorboard log dir", default="", type=str
    )
    parser.add_argument(
        "-i",
        "--trained-agent",
        help="Path to a pretrained agent to continue training",
        default="",
        type=str,
    )
    parser.add_argument(
        "--truncate-last-trajectory",
        help="When using HER with online sampling the last trajectory "
        "in the replay buffer will be truncated after reloading the replay buffer.",
        default=True,
        type=bool,
    )
    parser.add_argument(
        "-n",
        "--n-timesteps",
        help="Overwrite the number of timesteps to learn for in each epoch",
        default=1e6,
        type=int,
    )
    parser.add_argument(
        "--num-threads",
        help="Number of threads for PyTorch (-1 to use default)",
        default=-1,
        type=int,
    )
    parser.add_argument(
        "--log-interval",
        help="Override log interval (default: -1, no change)",
        default=-1,
        type=int,
    )
    parser.add_argument(
        "--eval-freq",
        help="Evaluate the agent every n steps (if negative, no evaluation)",
        default=10000,
        type=int,
    )
    parser.add_argument(
        "--eval-episodes",
        help="Number of episodes to use for evaluation",
        default=5,
        type=int,
    )
    parser.add_argument(
        "--save-freq",
        help="Save the model every n steps (if negative, no checkpoint)",
        default=-1,
        type=int,
    )
    parser.add_argument(
        "--save-replay-buffer",
        help="Save the replay buffer too (when applicable)",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-f", "--log-folder", help="Log folder", type=str, default="logs"
    )
    parser.add_argument(
        "--vec-env",
        help="VecEnv type",
        type=str,
        default="dummy",
        choices=["dummy", "subproc"],
    )
    parser.add_argument(
        "--n-trials",
        help="Number of trials for optimizing hyperparameters",
        type=int,
        default=10,
    )
    parser.add_argument(
        "-optimize",
        "--optimize-hyperparameters",
        action="store_true",
        default=False,
        help="Run hyperparameters search",
    )
    parser.add_argument(
        "--n-jobs",
        help="Number of parallel jobs when optimizing hyperparameters",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--sampler",
        help="Sampler to use when optimizing hyperparameters",
        type=str,
        default="tpe",
        choices=["random", "tpe", "skopt"],
    )
    parser.add_argument(
        "--pruner",
        help="Pruner to use when optimizing hyperparameters",
        type=str,
        default="median",
        choices=["halving", "median", "none"],
    )
    parser.add_argument(
        "--n-startup-trials",
        help="Number of trials before using optuna sampler",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--n-evaluations",
        help="Number of evaluations for hyperparameter optimization",
        type=int,
        default=20,
    )
    parser.add_argument(
        "--storage",
        help="Database storage path if distributed optimization should be used",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--study-name",
        help="Study name for distributed optimization",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--verbose", help="Verbose mode (0: no output, 1: INFO)", default=1, type=int
    )
    parser.add_argument(
        "--gym-packages",
        type=str,
        nargs="+",
        default=[],
        help="Additional external Gym environment package modules to import (e.g. gym_minigrid)",
    )
    parser.add_argument(
        "--env-kwargs",
        type=str,
        nargs="+",
        action=StoreDict,
        help="Optional keyword argument to pass to the env constructor",
    )
    parser.add_argument(
        "-params",
        "--hyperparams",
        type=str,
        nargs="+",
        action=StoreDict,
        help="Overwrite hyperparameter (e.g. learning_rate:0.01 train_freq:10)",
    )
    parser.add_argument(
        "-uuid",
        "--uuid",
        action="store_true",
        default=False,
        help="Ensure that the run has a unique ID",
    )

    # own arguments
    parser.add_argument(
        "--max_episode_steps",
        default=None,
        help="If set, agents will become 'done' after this many steps. set to None to disable.",
    )
    parser.add_argument("--buffer_size", type=int, default=10000)
    parser.add_argument("--batch_size", type=int, default=1024)
    parser.add_argument("--load_path", type=str, default=None)
    parser.add_argument(
        "--log_dir",
        type=str,
        default=path.expanduser("~/paavi_logs/"),
    )
    parser.add_argument(
        "--her",
        help="use hindsight experience replay, implemented for (SAC, TD3, DDPG, DQN).",
        action="store_true",
    )

    return parser


def eval_parser(program: str):
    parser = default_argument_parser(program)

    parser.add_argument("algo", type=str)
    parser.add_argument("--load_path", type=str, default=None)
    parser.add_argument("--record_path", type=str, default=None)
    parser.add_argument("--num_eps", type=int, default=5)
    parser.add_argument(
        "--log_dir", type=str, default=path.expanduser("~/paavi_logs/eval_run_logs")
    )
    parser.add_argument(
        "--her",
        help="use hindsight experience replay, implemented for (SAC, TD3, DDPG, DQN).",
        action="store_true",
    )

    return parser
