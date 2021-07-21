from Agents import ALGOS
import os


def build_algo(config, env):

    if config["load"] is not None:
        # .load :param env: the new environment to run the loaded model on
        # (can be None if you only need prediction from a trained model) has priority over any saved environment
        # XXX: must overwrite env otherwise tries to connect to dead envision server instance
        model = ALGOS[config["algo"]].load(config["load"], env=env)  # env=None

        # reset tensorboard_log incase model wasn't initally created from cwd
        model.tensorboard_log = config["log_dir"]

        save_path = config["load"]

    else:
        if config["her"]:
            # model = ALGOS[
            pass

            save_path = os.path.join(
                os.path.expanduser("~/paavi_logs/"),
                f'Models/{config["algo"]}{config["batch_size"]}_{config["scenarios"][0].split("/")[1]}_ep0k',
            )

        else:

            if config["algo"] in ["dqn", "qrdqn"]:
                model = ALGOS[config["algo"]](
                    "MlpPolicy",
                    env,
                    learning_rate=0.01,  # 5e-5,
                    buffer_size=config["buffer_size"],
                    train_freq=(1, "episode"),
                    tensorboard_log=config["log_dir"],
                    seed=config["seed"],
                    batch_size=config["batch_size"],
                    learning_starts=20000,
                    target_update_interval=100,
                    exploration_fraction=0.005,
                    exploration_initial_eps=1.0,
                    exploration_final_eps=0.01,
                    policy_kwargs=dict(n_quantiles=50)
                    if config["algo"] == "qrdqn"
                    else None,
                    verbose=0,
                )
            elif config["algo"] in ["ppo", "a2c"]:
                policy_kwargs = dict(n_quantiles=50)

                model = ALGOS[config["algo"]](
                    "MlpPolicy",
                    env,
                    learning_rate=0.01,  # 5e-5,
                    n_steps=10 if config["algo"] == "a2c" else 1000,
                    batch_size=config["batch_size"],
                    tensorboard_log=config["log_dir"],
                    policy_kwargs=None,
                    verbose=0,
                    seed=config["seed"],
                )

            save_path = os.path.join(
                os.path.expanduser("~/paavi_logs/"),
                f'Models/{config["algo"]}{config["batch_size"]}_{config["scenarios"][0].split("/")[1]}_ep0k',
            )

    return model, save_path
