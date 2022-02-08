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

from dataclasses import dataclass

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
# social_agent1 = SocialAgentActor(
#     name="zoo-car1",
#     agent_locator="scenarios.zoo_intersection.agent_prefabs:zoo-agent2-v0",
#     initial_speed=20,
# )
# social_agent2 = SocialAgentActor(
#     name="zoo-car2",
#     agent_locator="scenarios.zoo_intersection.agent_prefabs:zoo-agent2-v0",
#     initial_speed=20,
# )


# @dataclass(frozen=True)
# class PedSocialAgentActor(t.SocialAgentActor):
#     # pasted straight from TrafficActor class
#     vehicle_type: str = "passenger"
#     """The type of vehicle this actor uses. ("passenger", "bus", "coach", "truck", "trailer")"""


social_agent1 = t.SocialAgentActor(
    name="pedA",
    # agent_locator="Envs.zoo_ped_single.agent_prefabs:zoo-agent2-v0",
    agent_locator="Envs.zoo_ped_single.agent_prefabs:zoo-pedAgent-v0",
    vehicle_type="pedestrian",
    policy_kwargs={"agent_params": {"vehicle_type": "pedestrian"}},
    initial_speed=20,
)
# social_agent2 = t.SocialAgentActor(
#     name="zoo-car2",
#     agent_locator="Envs.zoo_ped_single.agent_prefabs:zoo-agent2-v0",
#     vehicle_type="pedestrian",
#     initial_speed=20,
# )

# gen_social_agent_missions(
#     scenario,
#     social_agent_actor=social_agent2,
#     name=f"s-agent-{social_agent2.name}",# to give access to scenarios for subprocesses
#     missions=[Mission(RandomRoute())],
# )

# gen_social_agent_missions(
#     scenario,
#     social_agent_actor=social_agent1,
#     name=f"s-agent-{social_agent1.name}",
#     missions=[
#         EndlessMission(begin=("edge-south-SN", 0, 30)),
#         Mission(Route(begin=("edge-west-WE", 0, 10), end=("edge-east-WE", 0, 10))),
#     ],
# )

# # Agent Missions
# gen_missions(
#     scenario=scenario,
#     missions=[
#         Mission(Route(begin=("edge-east-EW", 0, 10), end=("edge-south-NS", 0, 10))),
#         Mission(Route(begin=("edge-south-SN", 0, 10), end=("edge-east-WE", 0, 10))),
#     ],
# )

ego_missions = [
    t.Mission(t.Route(begin=("WC", 1, 5), end=("CE", 1, "max")), start_time=0)
]

social_missions = [
    t.Mission(
        t.Route(begin=("NC", 0, 5), end=("CS", 0, "max")),
        # vehicle_spec={"vehicle_type": "pedestrian"},
    )
]

scenario = t.Scenario(
    # traffic={"all": traffic},
    ego_missions=ego_missions,
    social_agent_missions={
        f"1": [
            [social_agent1],
            social_missions,
        ]
    },
)

gen_scenario(scenario, output_dir=str(Path(__file__).parent), seed=4312)
