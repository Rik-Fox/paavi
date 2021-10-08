# def main(config):

# class Pedestrian():

from Agents.agents import simple_agent

agent = simple_agent()

# import pdb

# pdb.set_trace()

#######################################################

import cloudpickle

# with open("cloudpickle_test.pkl", "w") as f:
#     cloudpickle.dump([agent], f)

cloudpickle.dumps(agent)

loaded_obj = cloudpickle.loads("cloudpickle_test.pkl")

print(loaded_obj)


###########################################################
# if __name__ == "__main__":
#     from param_parsers import trainer_parser

#     parser = trainer_parser("single-agent-experiment")

#     config = vars(parser.parse_args())

#     ### expilict values for vscode debugger
#     # from os import path

#     # config = {
#     #     "scenarios": ["Envs/ped_single"],
#     #     "sim_name": None,
#     #     "headless": True,
#     #     "num_episodes": 3,
#     #     "seed": 42,
#     #     "algo": "qrdqn",
#     #     "max_episode_steps": None,
#     #     "buffer_size": 1024,
#     #     "batch_size": 256,
#     #     "load_path": None,  # "Models/qrdqn256_ped_single",
#     #     "log_dir": path.expanduser("~/paavi_logs/"),
#     #     "n_timesteps": 1e6,
#     #     "record_path": None,
#     #     "her": False,
#     # }

#     main(config)
###########################################################
