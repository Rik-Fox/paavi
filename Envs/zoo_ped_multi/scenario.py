import os
import random
from pathlib import Path

from smarts.sstudio import (
    gen_missions,
    gen_social_agent_missions,
    gen_traffic,
    gen_scenario,
)

# from smarts.sstudio.types import (
#     Distribution,
#     EndlessMission,
#     Flow,
#     LaneChangingModel,
#     Mission,
#     RandomRoute,
#     Route,
#     SocialAgentActor,
#     Traffic,
#     TrafficActor,
# )

from smarts.sstudio import types as t
from smarts.core.agent_interface import DoneCriteria
from dataclasses import dataclass

# class RandomEntryTatic(t.EntryTactic):
#     pass

# scenario = os.path.dirname(os.path.realpath(__file__))

# Traffic Vehicles
#
# car = t.TrafficActor(
#     name="car",
# )

# cooperative_car = t.TrafficActor(
#     name="cooperative_car",
#     speed=t.Distribution(sigma=0.2, mean=1.0),
#     lane_changing_model=t.LaneChangingModel(impatience=0.1, cooperative=1),
# )

# aggressive_car = t.TrafficActor(
#     name="aggressive_car",
#     speed=t.Distribution(sigma=0.2, mean=1.0),
#     lane_changing_model=t.LaneChangingModel(impatience=1, cooperative=0.1),
# )

# horizontal_routes = [("west-WE", "east-WE"), ("east-EW", "west-EW")]
# turn_left_routes = [("east-EW", "south-NS")]
# turn_right_routes = [("west-WE", "south-NS")]

ped = t.TrafficActor(
    "ped12",
    min_gap=t.Distribution(mean=0.1, sigma=0),
    speed=t.Distribution(mean=1.0, sigma=0.4),
    vehicle_type="pedestrian",
)
from pathlib import Path

# for name, routes in {
#     "horizontal": horizontal_routes,
#     "turns": turn_left_routes + turn_right_routes,
# }.items():
traffic = t.Traffic(
    flows=[
        t.Flow(
            route=t.Route(begin=("NC", 0, 5), end=("CS", 0, "max")),
            begin=20,
            rate=random.randint(50, 100),
            actors={ped: 1},
        )
    ]
)


# Social Agents
#
# N.B. You need to have the agent_locator in a location where the left side can be resolved
#   as a module in form:
#       "this.resolved.module:attribute"
#   In your own project you would place the prefabs script where python can reach it


num_peds = 4

# for p in range(num_peds)
social_agents = [
    t.SocialAgentActor(
        name=f"pedA{i}",
        # agent_locator="Envs.zoo_ped_single.agent_prefabs:zoo-agent2-v0",
        agent_locator="Envs.zoo_ped_single.agent_prefabs:zoo-pedAgent-v0",
        vehicle_type="pedestrian",
        policy_kwargs={
            "agent_params": {
                "vehicle_type": "pedestrian",
                "done_criteria": DoneCriteria(
                    collision=False,
                    off_road=True,
                    off_route=False,
                    on_shoulder=False,
                    wrong_way=False,
                    not_moving=False,
                ),
            }
        },
        initial_speed=20,
    )
    for i in range(num_peds)
]

ego_missions = [
    t.Mission(t.Route(begin=("WC", 1, 5), end=("CE", 1, "max")), start_time=5)
]

social_missions = [
    t.Mission(
        t.Route(begin=("NC", 0, 5), end=("CS", 0, "max")),
        start_time=0
        # vehicle_spec={"vehicle_type": "pedestrian"},
    ),
    t.Mission(
        t.Route(begin=("NC", 1, 5), end=("CS", 0, "max")),
        start_time=0
        # vehicle_spec={"vehicle_type": "pedestrian"},
    ),
    # t.Mission(
    #     t.Route(begin=("NC", 0, 5), end=("CS", 1, "max")),
    #     start_time=2
    #     # vehicle_spec={"vehicle_type": "pedestrian"},
    # ),
    # t.Mission(
    #     t.Route(begin=("NC", 1, 5), end=("CS", 1, "max")),
    #     start_time=2
    #     # vehicle_spec={"vehicle_type": "pedestrian"},
    # ),
    t.Mission(
        t.Route(begin=("SC", 0, 5), end=("CN", 0, "max")),
        start_time=5
        # vehicle_spec={"vehicle_type": "pedestrian"},
    ),
    # t.Mission(
    #     t.Route(begin=("SC", 0, 5), end=("CN", 1, "max")),
    #     start_time=2
    #     # vehicle_spec={"vehicle_type": "pedestrian"},
    # ),
    t.Mission(
        t.Route(begin=("SC", 1, 5), end=("CN", 0, "max")),
        start_time=5
        # vehicle_spec={"vehicle_type": "pedestrian"},
    ),
    # t.Mission(
    #     t.Route(begin=("SC", 1, 5), end=("CN", 1, "max")),
    #     start_time=2
    #     # vehicle_spec={"vehicle_type": "pedestrian"},
    # ),
    # t.Mission(
    #     t.Route(begin=("SC", 0, 5), end=("CN", 1, "max")),
    #     start_time=5
    #     # vehicle_spec={"vehicle_type": "pedestrian"},
    # ),
]

social_agent_missions = {}

for ped, mis in zip(social_agents, social_missions):
    social_agent_missions[ped.name[4]] = [[ped], [mis]]

scenario = t.Scenario(
    # traffic={"all": traffic},
    ego_missions=ego_missions,
    # social_agent_missions={
    #     "group1": [
    #         social_agents,
    #         social_missions,
    #     ]
    # },
    social_agent_missions=social_agent_missions,
)

gen_scenario(scenario, output_dir=str(Path(__file__).parent), seed=4312)
