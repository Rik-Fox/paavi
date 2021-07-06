from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t

# generate SUMO controlled traffic

traffic = t.Traffic(
    flows=[
        # t.Flow(
        #     # begin/end = ("edge", lane, offset in metres)
        #     route=t.Route(begin=("EC", 0, 10), end=("CW", 0, "max"),),
        #     rate=1,
        #     actors={t.TrafficActor("car", max_speed=8, vehicle_type="truck"): 1},
        #     # this begin is time to start popluating in seconds, can define end also
        #     begin=2,
        # ),
        # t.Flow(
        #     route=t.Route(begin=("WC", 0, 10), end=("CE", 0, "max",),),
        #     rate=1,
        #     actors={t.TrafficActor("car", max_speed=8): 1},
        #     begin=2,
        # ),
        t.Flow(
            route=t.Route(begin=("NC", 0, 100), end=("CS", 0, "max"),),
            rate=60 * 30,
            actors={t.TrafficActor("ped", max_speed=8, vehicle_type="pedestrian"): 1},
            # begin=0.5,
        ),
    ]
)

# generate pre trained RL controlled agents

social_agent_missions = {
    "all": (
        [
            t.SocialAgentActor(
                name="open-agent",
                agent_locator="open_agent:open_agent-v0",
                initial_speed=20,
            ),
            # t.SocialAgentActor(
            #     name="keep-lane-agent",
            #     agent_locator="zoo.policies:keep-lane-agent-v0",
            #     initial_speed=20,
            # ),
        ],
        [
            t.Mission(t.Route(begin=("EC", 1, 10), end=("CW", 0, "max")),),
            # t.Mission(t.Route(begin=("NC", 0, 10), end=("CS", 0, "max")),),
        ],
    ),
}

# generate desired route for learning agent

ego_missions = [t.Mission(t.Route(begin=("WC", 1, 5), end=("CE", 1, "max")),)]

scenario = t.Scenario(
    traffic={"all": traffic},
    ego_missions=ego_missions,
    # social_agent_missions=social_agent_missions,
)

gen_scenario(scenario, output_dir=str(Path(__file__).parent))
