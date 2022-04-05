import os
import time

from stable_baselines3.common.monitor import Monitor
from smarts.core.utils.episodes import episodes

import sys

sys.settrace

# Try to import numpy first or set the threading layer accordingly. Set MKL_SERVICE_FORCE_INTEL to force it.
os.environ["MKL_THREADING_LAYER"] = "GNU"
os.environ["MKL_SERVICE_FORCE_INTEL"] = "1"
# fixes below error
# XXX: Error: mkl-service + Intel(R) MKL: MKL_THREADING_LAYER=INTEL is incompatible with libgomp-a34b3233.so.1 library.

# to give access to scenarios for subprocesses, maybe fixed now
# export PYTHONPATH="${PYTHONPATH}:/home/rfox/PhD/paavi"

from paavi.Agents.build import build_algo
from paavi.Envs import build_env
from paavi.util.custom_logging import CustomTrackingCallback


def main(config):

    # monitor_path = os.path.join(, "Monitor_logs")
    run_name = f'{config["algo"]}_seed{config["seed"]}_batchsize{config["batch_size"]}_{config["scenarios"][-1].split("/")[-1]}'

    if config["stop_dist_rwd"]:
        run_name = f'{run_name}_SD{config["stop_dist_rwd"]}'

    run_dir = os.path.join(config["log_dir"], run_name)
    os.makedirs(run_dir, exist_ok=True)

    env = Monitor(
        build_env(config),
        filename=os.path.join(run_dir, "monitor.csv"),
    )
    
    agent = build_algo(config, env=env)

    agent.learn(
        total_timesteps=config["n_timesteps"],
        tb_log_name=f"{run_name}_logs",
        callback=CustomTrackingCallback(
            check_freq=1000,
            log_dir=run_dir,
            start_time=time.time(),
            verbose=1,
        ),
    )

    agent.save(run_dir, "final")


if __name__ == "__main__":
    from paavi.util.param_parsers import trainer_parser

    parser = trainer_parser("single-agent-experiment")

    config = vars(parser.parse_args())

    ### expilict values for vscode debugger

    # config = {
    #     "scenarios": ["Envs/zoo_ped_single"],
    #     "sim_name": None,
    #     "headless": False,
    #     "num_episodes": 3,
    #     "seed": 42,
    #     "algo": "qrdqn",
    #     "max_episode_steps": None,
    #     "buffer_size": 1024,
    #     "batch_size": 256,
    #     "load_path": None,  # "Models/qrdqn256_ped_single",
    #     "log_dir": os.path.expanduser("~/paavi_logs/"),
    #     "n_timesteps": 1e6,
    #     "record_path": None,
    #     "her": False,
    #     "buffer_fill_period": 1e4,
    # }

    main(config)
