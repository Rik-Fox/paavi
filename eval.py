import os
import logging

from gym import make

from examples import default_argument_parser
from smarts.core.utils.episodes import episodes

from Agents import ALGOS, build
from Envs import build_env

logging.basicConfig(level=logging.INFO)

def eval(agent, env, num_episodes):
    # obs = env.reset()
    # while True:
    #     action, _states = model.predict(obs)
    #     obs, rewards, dones, info = env.step(action)
    # env.render()
    import time
    time.sleep(5)
    for episode in episodes(n=num_episodes):
        # agents = {
        #     agent_id: agent_spec.build_agent()
        #     for agent_id, agent_spec in agent_specs.items()
        # }
        observations = env.reset()
        episode.record_scenario(env.scenario_log)

        dones = {"__all__": False}
        while not dones["__all__"]:
            # actions = {
            #     agent_id: agents[agent_id].act(agent_obs)
            #     for agent_id, agent_obs in observations.items()
            # }
            # action, _states = model.predict(observations)
            # actions = {
            #     agent_id: agent.predict(agent_obs)
            #     for agent_id, agent_obs in observations.items()
            # }
            action, _ = agent.predict(observations)
            observations, rewards, dones, infos = env.step(action)
            episode.record_step(observations, rewards, dones, infos)

    # env.close()


if __name__ == "__main__":
    parser = default_argument_parser("eval_env")
    parser.add_argument("algo", type=str)
    parser.add_argument("--load_path", type=str, default=None)
    parser.add_argument("--num_eps", type=int, default=5)
    parser.add_argument("--log_dir", type=str, default=os.path.expanduser("~/paavi_logs/eval_run_logs"))

    config = vars(parser.parse_args())

    env = build_env(config)
    
    if config["load_path"] == None:
        from Agents import build
        model = build.build_algo(config, env)
    else:
        model = ALGOS[config["algo"]].load(config["load_path"], env=env)  # env=None

    # reset tensorboard_log incase model wasn't initally created from cwd
    model.tensorboard_log = config["log_dir"]
 
    eval(model, env, config["num_eps"])