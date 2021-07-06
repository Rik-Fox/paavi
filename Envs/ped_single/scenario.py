from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t

from random import randrange

# generate pedestrian

traffic = t.Traffic(
    flows=[
        t.Flow(
            route=t.Route(begin=("NC", 0, 5), end=("CS", 0, "max"),),
            rate=60 * 30,
            actors={t.TrafficActor("ped", max_speed=8, vehicle_type="pedestrian"): 0.5},
            # begin=0.5,
        ),
    ]
)

# generate desired route for learning agent

ego_missions = [
    t.Mission(t.Route(begin=("WC", 1, 5), end=("CE", 1, "max")), start_time=1)
]

scenario = t.Scenario(traffic={"all": traffic}, ego_missions=ego_missions,)

gen_scenario(scenario, output_dir=str(Path(__file__).parent))
