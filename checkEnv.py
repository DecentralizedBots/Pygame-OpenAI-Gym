from stable_baselines3.common.env_checker import check_env
from DriveEnv import DriveEnv

env = DriveEnv()

check_env(env)