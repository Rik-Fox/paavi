<<<<<<< HEAD:paavi/Agents/build.py
from genericpath import exists
import os
from torch import device, cuda
from typing import Sequence

from smarts.core.agent import AgentSpec
from smarts.core.agent_interface import AgentType, AgentInterface

from paavi.Agents import ALGOS


def build_agents(
    agent_ids: Sequence[str],
    agent_types: Sequence[AgentType],
    agent_builders: Sequence,
    **kwargs,
):

    if len(agent_types) == 1:
        agent_types = [agent_types[0] for i in range(len(agent_ids))]

    if len(agent_builders) == 1:
        agent_builders = [agent_builders[0] for i in range(len(agent_ids))]

    assert len(agent_types) == len(
        agent_ids
    ), "Number of AGENT_TYPES must either be 1 or match number of AGENT_IDS"
    assert len(agent_builders) == len(
        agent_ids
    ), "Number of AGENT_BUILDERS must either be 1 or match number of AGENT_IDS"

    agent_specs = {
        agent_id: AgentSpec(
            interface=AgentInterface.from_type(agent_type, **kwargs),
            # agent_params={
            #     # "path_to_model": Path(__file__).resolve().parent / "model",
            #     "observation_space": agent_builder.OBSERVATION_SPACE,
            #     "action_space": agent_builder.ACTION_SPACE,
            # },
            agent_builder=agent_builder,
            observation_adapter=agent_builder.observation_adaptor,
            # reward_adapter=reward_adapter,
            # action_adapter=action_adapter,
        )
        for agent_id, agent_type, agent_builder in zip(
            agent_ids, agent_types, agent_builders
        )
    }
    # need to create urdf for anything but "car" or "bus"
    # agent_specs[agent_ids[0]].interface.vehicle_type = "motorcycle"

    return agent_specs


# def config_open_agents(debug=False, aggressiveness=3):

#     import importlib

#     try:
#         open_agent = importlib.import_module("open_agent")
#     except ModuleNotFoundError as e:
#         raise ModuleNotFoundError(
#             f"Ensure that the open-agent has been installed with `pip install open-agent"
#         )

#     open_agent_spec = open_agent.entrypoint(debug, aggressiveness)

#     return open_agent_spec


def build_algo(config, env):

    tb_log_dir = os.path.join(config["log_dir"], "tb_run_logs")
    os.makedirs(tb_log_dir, exist_ok=True)
    # tb_log_dir = None  # replaced with custom logging using callback function

    device_to_use = device("cuda" if cuda.is_available() else "cpu")
    # device_to_use = "cpu"
    print("cuda available => ", cuda.is_available())
    print("device => ", device_to_use)

    if config["load_path"] is not None:
        # .load :param env: the new environment to run the loaded model on
        # (can be None if you only need prediction from a trained model) has priority over any saved environment
        # XXX: must overwrite env otherwise tries to connect to dead envision server instance
        model = ALGOS[config["algo"]].load(
            config["load"], env=env, device=device_to_use
        )  # env=None

        # reset tensorboard_log incase model wasn't initally created from cwd
        model.tensorboard_log = tb_log_dir

    elif config["her"]:
        implemented = ["sac", "td3", "ddpg", "dqn"]
        if config["algo"] not in implemented:
            raise NotImplementedError(f"only {implemented} are implemented to use HER")
        del implemented

        model = ALGOS["her"](
            "MlpPolicy", env, model_class=ALGOS[config["algo"]], max_episode_length=512
        )

    elif config["algo"] in ["dqn", "qrdqn"]:
        model = ALGOS[config["algo"]](
            "MlpPolicy",
            env,
            learning_rate=0.01,  # 5e-5,
            buffer_size=config["buffer_size"],
            train_freq=(10, "episode"),
            tensorboard_log=tb_log_dir,
            seed=config["seed"],
            batch_size=config["batch_size"],
            learning_starts=config["buffer_fill_period"],
            target_update_interval=1024,
            exploration_fraction=0.005,
            exploration_initial_eps=1.0,
            exploration_final_eps=0.1,
            policy_kwargs=dict(n_quantiles=50) if config["algo"] == "qrdqn" else None,
            device=device_to_use,
            verbose=0,
        )
    elif config["algo"] == "ppo":
        # doesnt take the epsilon behaviour arguments for exploration
        model = ALGOS[config["algo"]](
            "MlpPolicy",
            env,
            learning_rate=0.01,  # 5e-5,
            n_steps=64,
            batch_size=config["batch_size"],
            tensorboard_log=tb_log_dir,
            policy_kwargs=None,
            device=device_to_use,
            verbose=0,
            seed=config["seed"],
        )
    elif config["algo"] == "a2c":
        # same as ppo except no batch size as On Policy
        model = ALGOS[config["algo"]](
            "MlpPolicy",
            env,
            learning_rate=0.01,  # 5e-5,
            n_steps=1024,
            tensorboard_log=tb_log_dir,
            policy_kwargs=None,
            device=device_to_use,
            verbose=0,
            seed=config["seed"],
        )
    else:
        raise NotImplementedError

    save_path = os.path.join(
        config["log_dir"],
        f'Models/{config["algo"]}{config["batch_size"]}_{config["scenarios"][0].split("/")[1]}',
    )

    return model
=======
from genericpath import exists
import os
from torch import device, cuda
from typing import Sequence

from smarts.core.agent import AgentSpec
from smarts.core.agent_interface import AgentType, AgentInterface

from Agents import ALGOS


def build_agents(
    agent_ids: Sequence[str],
    agent_types: Sequence[AgentType],
    agent_builders: Sequence,
    **kwargs,
):

    if len(agent_types) == 1:
        agent_types = [agent_types[0] for i in range(len(agent_ids))]

    if len(agent_builders) == 1:
        agent_builders = [agent_builders[0] for i in range(len(agent_ids))]

    assert len(agent_types) == len(
        agent_ids
    ), "Number of AGENT_TYPES must either be 1 or match number of AGENT_IDS"
    assert len(agent_builders) == len(
        agent_ids
    ), "Number of AGENT_BUILDERS must either be 1 or match number of AGENT_IDS"

    agent_specs = {
        agent_id: AgentSpec(
            interface=AgentInterface.from_type(agent_type, **kwargs),
            # agent_params={
            #     # "path_to_model": Path(__file__).resolve().parent / "model",
            #     "observation_space": agent_builder.OBSERVATION_SPACE,
            #     "action_space": agent_builder.ACTION_SPACE,
            # },
            agent_builder=agent_builder,
            observation_adapter=agent_builder.observation_adaptor,
            # reward_adapter=reward_adapter,
            # action_adapter=action_adapter,
        )
        for agent_id, agent_type, agent_builder in zip(
            agent_ids, agent_types, agent_builders
        )
    }
    # need to create urdf for anything but "car" or "bus"
    # agent_specs[agent_ids[0]].interface.vehicle_type = "motorcycle"

    return agent_specs


# def config_open_agents(debug=False, aggressiveness=3):

#     import importlib

#     try:
#         open_agent = importlib.import_module("open_agent")
#     except ModuleNotFoundError as e:
#         raise ModuleNotFoundError(
#             f"Ensure that the open-agent has been installed with `pip install open-agent"
#         )

#     open_agent_spec = open_agent.entrypoint(debug, aggressiveness)

#     return open_agent_spec


def build_algo(config, env):

    tb_log_dir = os.path.join(config["log_dir"], "tb_run_logs")
    os.makedirs(tb_log_dir, exist_ok=True)
    # tb_log_dir = None  # replaced with custom logging using callback function

    device_to_use = device("cuda" if cuda.is_available() else "cpu")
    # device_to_use = "cpu"
    print("cuda available => ", cuda.is_available())
    print("device => ", device_to_use)

    if config["load_path"] is not None:
        # .load :param env: the new environment to run the loaded model on
        # (can be None if you only need prediction from a trained model) has priority over any saved environment
        # XXX: must overwrite env otherwise tries to connect to dead envision server instance
        model = ALGOS[config["algo"]].load(
            config["load"], env=env, device=device_to_use
        )  # env=None

        # reset tensorboard_log incase model wasn't initally created from cwd
        model.tensorboard_log = tb_log_dir

    elif config["her"]:
        implemented = ["sac", "td3", "ddpg", "dqn"]
        if config["algo"] not in implemented:
            raise NotImplementedError(f"only {implemented} are implemented to use HER")
        del implemented

        model = ALGOS["her"](
            "MlpPolicy", env, model_class=ALGOS[config["algo"]], max_episode_length=512
        )

    elif config["algo"] in ["dqn", "qrdqn"]:
        model = ALGOS[config["algo"]](
            "MlpPolicy",
            env,
            learning_rate=0.01,  # 5e-5,
            buffer_size=config["buffer_size"],
            train_freq=(10, "episode"),
            tensorboard_log=tb_log_dir,
            seed=config["seed"],
            batch_size=config["batch_size"],
            learning_starts=config["buffer_fill_period"],
            target_update_interval=1024,
            exploration_fraction=0.005,
            exploration_initial_eps=1.0,
            exploration_final_eps=0.1,
            policy_kwargs=dict(n_quantiles=50) if config["algo"] == "qrdqn" else None,
            device=device_to_use,
            verbose=0,
        )
    elif config["algo"] == "ppo":
        # doesnt take the epsilon behaviour arguments for exploration
        model = ALGOS[config["algo"]](
            "MlpPolicy",
            env,
            learning_rate=0.01,  # 5e-5,
            n_steps=64,
            batch_size=config["batch_size"],
            tensorboard_log=tb_log_dir,
            policy_kwargs=None,
            device=device_to_use,
            verbose=0,
            seed=config["seed"],
        )
    elif config["algo"] == "a2c":
        # same as ppo except no batch size as On Policy
        model = ALGOS[config["algo"]](
            "MlpPolicy",
            env,
            learning_rate=0.01,  # 5e-5,
            n_steps=1024,
            tensorboard_log=tb_log_dir,
            policy_kwargs=None,
            device=device_to_use,
            verbose=0,
            seed=config["seed"],
        )
    else:
        raise NotImplementedError

    save_path = os.path.join(
        config["log_dir"],
        f'Models/{config["algo"]}{config["batch_size"]}_{config["scenarios"][0].split("/")[1]}',
    )

    return model
>>>>>>> branch:Agents/build.py
