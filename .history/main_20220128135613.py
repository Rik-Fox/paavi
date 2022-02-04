import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


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

from Agents import build
from Envs import build_env
from custom_logging import CustomTrackingCallback


options = webdriver.ChromeOptions()
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
options.add_argument("--log-level=0")
options.add_argument("--window-size=1400x1080")
# service = ChromeService(executable_path'/usr/local/bin/chromedriver')

envision_port = 8081


def checkPaused(driver, paused):
    for entry in driver.get_log("browser"):
        # if entry["source"] == "console-api":
        print(entry)

        if (
            entry["message"]
            == f"http://localhost:{envision_port}/main.js 384:88417 true"
        ):
            print()
            print("Paused")
            print()
            return True
        elif (
            entry["message"]
            == f"http://localhost:{envision_port}/main.js 384:88417 false"
        ):
            print()
            print("Playing")
            print()
            return False

    return paused


def main(config):

    # monitor_path = os.path.join(, "Monitor_logs")
    run_name = f'{config["algo"]}_seed{config["seed"]}_batchsize{config["batch_size"]}_{config["scenarios"][-1].split("/")[-1]}'

    run_dir = os.path.join(config["log_dir"], run_name)
    os.makedirs(run_dir, exist_ok=True)

    env = Monitor(
        build_env(config),
        filename=os.path.join(run_dir, "monitor.csv"),
    )

    agent = build.build_algo(config, env=env)

    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(options=options)
    driver.get(f"http://localhost:{envision_port}")

    paused = True

    for episode in episodes(n=config["episodes"]):
        agent_obs = env.reset()
        # episode.record_scenario(env.scenario_log)
        # import pdb

        # pdb.set_trace()
        # print(env.env._smarts._envision.endpoint)

        # dones = False
        # while not dones:
        for i in range(int(config["max_episode_steps"])):
            agent_action, _ = agent.predict(agent_obs, deterministic=False)
            agent_obs, rewards, dones, infos = env.step(agent_action)
            # episode.record_step(agent_obs, rewards, dones, infos)
            print("episode => ", episode.index, " : step => ", i)
            paused = checkPaused(driver, paused)

            while paused:

                paused = checkPaused(driver, paused)

    # agent.learn(
    #     total_timesteps=config["n_timesteps"],
    #     tb_log_name=f"{run_name}_logs",
    #     callback=CustomTrackingCallback(
    #         check_freq=1000,
    #         log_dir=run_dir,
    #         start_time=time.time(),
    #         verbose=1,
    #     ),
    # )

    # agent.save(run_dir, "final")


if __name__ == "__main__":
    from param_parsers import trainer_parser

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
