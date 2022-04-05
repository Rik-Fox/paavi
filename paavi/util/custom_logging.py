import os
import time
import numpy as np

from stable_baselines3.common.results_plotter import load_results, ts2xy
from stable_baselines3.common.callbacks import BaseCallback


class CustomTrackingCallback(BaseCallback):
    """
    Callback for saving a model (the check is done every ``check_freq`` steps)
    based on the training reward (in practice, we recommend using ``EvalCallback``).

    :param check_freq: (int)
    :param log_dir: (str) Path to the folder where the model will be saved.
    It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: (int)
    """

    def __init__(
        self, check_freq: int, log_dir: str, start_time: float, verbose=1
    ):
        super(CustomTrackingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.start_time = start_time

        self.save_path = log_dir
        self.checkpoint_save_path = os.path.join(log_dir, "checkpoint_model")
        self.periodic_save_path = os.path.join(log_dir, "periodic_model")

        self.best_mean_reward = -np.inf
        self.worst_mean_reward = np.inf

    def _init_callback(self) -> None:
        # Create folders if needed
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

        if self.checkpoint_save_path is not None:
            os.makedirs(self.checkpoint_save_path, exist_ok=True)

        if self.periodic_save_path is not None:
            os.makedirs(self.periodic_save_path, exist_ok=True)

    def _on_rollout_end(self) -> None:

        pass

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:

            # Retrieve training reward
            x, y = ts2xy(load_results(self.log_dir), "timesteps")
            # this if basically stops callback from executing on 0th call
            if len(x) > 0:
                # Mean training reward over the last 100 episodes
                mean_reward = np.mean(y[-100:])
                if self.verbose > 0:
                    print("Num timesteps: {}".format(self.num_timesteps))
                    print(
                        "Best mean reward: {:.5f} - Last 100 episodes mean reward: {:.5f}".format(
                            self.best_mean_reward, mean_reward
                        )
                    )

                # New best model, you could save the agent here
                if mean_reward > self.best_mean_reward:
                    self.best_mean_reward = mean_reward
                    # Example for saving best model
                    if self.verbose > 0:
                        print("Saving new best model to {}".format(self.save_path))
                    self.model.save(f"{self.save_path}/best")
                    open(f"{self.save_path}/best.zip").close()

                if mean_reward < self.worst_mean_reward:
                    self.worst_mean_reward = mean_reward
                    if self.verbose > 0:
                        print("Saving new worst model to {}".format(self.save_path))
                    self.model.save(f"{self.save_path}/worst")
                    open(f"{self.save_path}/worst.zip").close()

                if self.num_timesteps % 10000 == 0:
                    if self.verbose > 0:
                        print(
                            "Saving periodic model to {}".format(
                                self.periodic_save_path
                            )
                        )
                    self.model.save(
                        f"{self.periodic_save_path}/ep_{self.num_timesteps}"
                    )

                if ((self.start_time - time.time()) % 1200) <= 3:
                    self.model.save(f"{self.checkpoint_save_path}/continuation_point")

                self.logger.record("custom/mean_ep_rwd", mean_reward)
                # self.logger.record("custom/", )
                # self.logger.record("custom/", )
                # self.logger.record("custom/", )
                # self.logger.record("custom/", )
                # self.logger.record("custom/", )
                self.logger.dump(self.num_timesteps)

            print("--------------------------")

        return True
