from pathlib import Path

from smarts.sstudio import gen_scenario
from smarts.sstudio import types as t

from random import randrange

# adapted from smarts.types distributions
class PoissonDistribution(t.Distribution):
    """A poisson distribution used for randomized parameters."""

    lam: float

    def sample(self):
        """The next sample from the distribution."""
        return random.poisson(self.lam)


# generate pedestrian

slow_ped = t.TrafficActor(
    "ped8",
    min_gap=t.Distribution(mean=0.1, sigma=0),
    speed=t.Distribution(mean=0.2, sigma=0.1),
    vehicle_type="pedestrian",
)
ped = t.TrafficActor(
    "ped12",
    min_gap=t.Distribution(mean=0.1, sigma=0),
    speed=t.Distribution(mean=1.0, sigma=0.4),
    vehicle_type="pedestrian",
)
fast_ped = t.TrafficActor(
    "ped16",
    min_gap=t.Distribution(mean=0.1, sigma=0),
    speed=t.Distribution(mean=1.2, sigma=0.2),
    vehicle_type="pedestrian",
)
super_fast_ped = t.TrafficActor(
    "ped20",
    min_gap=t.Distribution(mean=0.1, sigma=0),
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
            rate=60 * 15,
            actors={ped: 1},
            # begin=0.5,
        ),
    ]
)

# generate desired route for learning agent

ego_missions = [
    t.Mission(t.Route(begin=("WC", 1, 5), end=("CE", 1, "max")), start_time=20)
]

scenario = t.Scenario(
    traffic={"all": traffic},
    ego_missions=ego_missions,
)

gen_scenario(scenario, output_dir=str(Path(__file__).parent), seed=4312)
