from smarts.core.utils.episodes import episodes


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
            action, _states = model.predict(observations)
            actions = {
                agent_id: model.predict(agent_obs)
                for agent_id, agent_obs in observations.items()
            }
            observations, rewards, dones, infos = env.step(actions)
            episode.record_step(observations, rewards, dones, infos)

        del agents
