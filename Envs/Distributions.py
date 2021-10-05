from smarts.sstudio import types as t
import random

# adapted from smarts.types distributions
class PoissonDistribution(t.Distribution):
    """A poisson distribution used for randomized parameters."""

    lam: float

    def sample(self):
        """The next sample from the distribution."""
        return random.poisson(self.lam)
