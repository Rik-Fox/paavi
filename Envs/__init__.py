from gym.envs.registration import register

register(
    id="sb3hiway-v0", entry_point="Envs.sb3_hiway_env:sb3HiWayEnv",
)
