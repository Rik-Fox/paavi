from smarts.core.agent import Agent, AgentSpec
from smarts.core.agent_interface import AgentInterface, AgentType
from smarts.zoo.registry import register

from Agents.agents import PedAgent, HumanKeyboardAgent


class SimpleAgent(Agent):
    def act(self, obs):
        return "keep_lane"


# You can register a callable that will build your AgentSpec
def ped_agent_callable(target_prefix=None, interface=None, agent_params=None):
    if interface is None:
        interface = AgentInterface.from_type(
            AgentType.Imitation,
            vehicle_type=agent_params["vehicle_type"],
            done_criteria=agent_params["done_criteria"],
        )
    agent_spec = AgentSpec(interface=interface, agent_builder=PedAgent)
    agent_spec.interface.vehicle_type = "pedestrian"
    return agent_spec


def human_agent_callable(target_prefix=None, interface=None, agent_params=None):
    if interface is None:
        interface = AgentInterface.from_type(
            AgentType.Imitation,
            vehicle_type=agent_params["vehicle_type"],
            done_criteria=agent_params["done_criteria"],
        )
    agent_spec = AgentSpec(interface=interface, agent_builder=HumanKeyboardAgent)
    agent_spec.interface.vehicle_type = "pedestrian"
    return agent_spec


# def demo_agent_callable(target_prefix=None, interface=None):
#     if interface is None:
#         interface = AgentInterface.from_type(AgentType.Laner)
#     agent_spec = AgentSpec(interface=interface, agent_builder=SimpleAgent)
#     return agent_spec


# register(
#     locator="zoo-agent1-v0",
#     entry_point="smarts.core.agent:AgentSpec",
#     # Also works:
#     # entry_point=smarts.core.agent.AgentSpec
#     interface=AgentInterface.from_type(AgentType.Laner, max_episode_steps=20000),
# )

# register(
#     locator="zoo-agent2-v0",
#     entry_point=demo_agent_callable,
#     # Also works:
#     # entry_point="scenarios.zoo_intersection:demo_agent_callable",
# )

register(
    locator="HumanAgent-v0",
    entry_point=human_agent_callable,
    # Also works:
    # entry_point="scenarios.zoo_intersection:demo_agent_callable",
)

register(
    locator="zoo-pedAgent-v0",
    entry_point=ped_agent_callable,
    # Also works:
    # entry_point="scenarios.zoo_intersection:demo_agent_callable",
)
