import logging

from smarts.core.utils.episodes import episodes

from paavi.Agents import ALGOS, build
from paavi.Envs import build_env

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
            observations, rewards, done, infos = env.step(action)
            dones["__all__"] = done
            episode.record_step(observations, rewards, dones, infos)

        input("Press Enter to end")

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

    eval(model, env, config["num_eps"])
