from smarts.core.utils.episodes import episodes
import argparse
import os
from Agents import ALGOS



def eval(model, env, agent_specs, num_episodes):
    obs = env.reset()
    # while True:
    #     action, _states = model.predict(obs)
    #     obs, rewards, dones, info = env.step(action)
    # env.render()

    for episode in episodes(n=num_episodes):
        agents = {
            agent_id: agent_spec.build_agent()
            for agent_id, agent_spec in agent_specs.items()
        }
        observations = env.reset()
        episode.record_scenario(env.scenario_log)

        dones = {"__all__": False}
        while not dones["__all__"]:
            # actions = {
            #     agent_id: agents[agent_id].act(agent_obs)
            #     for agent_id, agent_obs in observations.items()
            # }
            # action, _states = model.predict(observations)
            actions = {
                agent_id: model.predict(agent_obs)
                for agent_id, agent_obs in observations.items()
            }
            observations, rewards, dones, infos = env.step(actions)
            episode.record_step(observations, rewards, dones, infos)

        del agents

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("load_path", type=str)
    parser.add_argument("--num_eps", type=int)
    parser.add_argument("--save_dir", type=str, default=os.path.expanduser("~/paavi_logs/eval_runs"))

    config = parser.parse_args()

    model = ALGOS[config["algo"]].load(config["load_path"], env=env)  # env=None

    # reset tensorboard_log incase model wasn't initally created from cwd
    model.tensorboard_log = config["log_dir"]
 
    eval()