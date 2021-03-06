import os

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

# from Agents import build
from paavi.Agents.agents import HumanKeyboardAgent, random_agent, PedAgent
from paavi.Envs import build_env
from smarts.core.agent_interface import DoneCriteria
from paavi.util.custom_logging import CustomTrackingCallback
from paavi.util.browser import Browser


def main(config):

    # monitor_path = os.path.join(, "Monitor_logs")
    # run_name = f'{config["algo"]}_seed{config["seed"]}_batchsize{config["batch_size"]}_{config["scenarios"][-1].split("/")[-1]}'

    # run_dir = os.path.join(config["log_dir"], run_name)
    # os.makedirs(run_dir, exist_ok=True)

    # env = Monitor(
    #     build_env(config),
    #     filename=os.path.join(run_dir, "monitor.csv"),
    # )
    vehicle_type = "sedan"  # "pedestrian"
    done_criteria = DoneCriteria(
        collision=False,
        off_road=True,
        off_route=False,
        on_shoulder=False,
        wrong_way=False,
        not_moving=False,
    )

    env = build_env(config, vehicle_type=vehicle_type, done_criteria=done_criteria)

    agent = HumanKeyboardAgent() if vehicle_type == "pedestrian" else random_agent()

    chrome = Browser(config["envision_port"])

    for episode in episodes(n=config["episodes"]):
        agent_obs = env.reset()
        for i in range(int(config["max_episode_steps"])):
            agent_action = agent.act(agent_obs)
            agent_obs, rewards, dones, infos = env.step(agent_action)
            # episode.record_step(agent_obs, rewards, dones, infos)
            # print("episode => ", episode.index, " : step => ", i)
            while chrome.get_paused():
                chrome.get_paused()


if __name__ == "__main__":

    from paavi.util.param_parsers import trainer_parser

    parser = trainer_parser("single-agent-experiment")
    config = vars(parser.parse_args())

    main(config)
