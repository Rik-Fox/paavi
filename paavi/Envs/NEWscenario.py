from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t

# from Distributions import PoissonDistribution

from smarts.sstudio import types as t
import random

# adapted from smarts.types distributions
class PoissonDistribution(t.Distribution):
    """A poisson distribution used for randomized parameters."""

    lam: float

    def sample(self):
        """The next sample from the distribution."""
        return random.poisson(self.lam)


from random import randrange


# generate pedestrian

slow_ped = t.TrafficActor(
    "ped8",
    speed=t.Distribution(mean=0.2, sigma=0.1),
    vehicle_type="pedestrian",
)
ped = t.TrafficActor(
    "ped12",
    speed=t.Distribution(mean=0.6, sigma=0.2),
    vehicle_type="pedestrian",
)
fast_ped = t.TrafficActor(
    "ped16",
    speed=t.Distribution(mean=1.2, sigma=0.2),
    vehicle_type="pedestrian",
)
super_fast_ped = t.TrafficActor(
    "ped20",
    speed=t.Distribution(mean=1.6, sigma=0.1),
    vehicle_type="pedestrian",
)

traffic = t.Traffic(
    flows=[
        t.Flow(
            route=t.Route(
                begin=("NC", 0, 5),
                end=("CS", 0, "max"),
            ),
            rate=60 * 60,
            actors={slow_ped: 0.2, ped: 0.4, fast_ped: 0.3, super_fast_ped: 0.1},
            # begin=0.5,
        ),
    ]
)

# generate desired route for learning agent

ego_missions = [
    t.Mission(t.Route(begin=("WC", 1, 5), end=("CE", 1, "max")), start_time=15)
]

scenario = t.Scenario(
    traffic={"all": traffic},
    ego_missions=ego_missions,
)

gen_scenario(scenario, output_dir=str(Path(__file__).parent))
