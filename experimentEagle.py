import logging

from paavi.Agents import ALGOS, build
from paavi.Envs import build_env

from env_helpers import env_data_grabber

logging.basicConfig(level=logging.INFO)


def eval(agent, env, config):
    import time

    # give TRACI server time to connect
    time.sleep(5)
    traj_data = env_data_grabber(env, auto_episode_recording=True)

    for episode in range(config["num_eps"]):
        print("Episode => ", episode)
        observations = env.reset()
        done = False
        while not done:
            action, _ = agent.predict(observations)
            observations, rewards, done, infos = env.step(action)
            traj_data.record_step(done, infos)

        # traj_data.record_episode()

        # input("Press Enter to end")
    traj_data.save(agent.tensorboard_log, config)

    # env.close()


if __name__ == "__main__":
    from paavi.util.param_parsers import eval_parser
    import os

    parser = eval_parser("eval_env")

    config = vars(parser.parse_args())

    env = build_env(config)

    if config["load_path"] == None:
        from paavi.Agents import build

        model = build.build_algo(config, env)
    else:
        model = ALGOS[config["algo"]].load(config["load_path"], env=env)  # env=None

    # manually set tensorboard_log incase model wasn't initally logging there
    model.tensorboard_log = config["log_dir"]

    if config["record_path"] is not None:
        os.makedirs(config["record_path"], exist_ok=True)

    eval(model, env, config)
