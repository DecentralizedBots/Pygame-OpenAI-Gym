import gym
from stable_baselines3 import A2C
#import os

'''
models_dir = "models/A2C"
logdir = "logs"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)
'''

env = gym.make("LunarLander-v2")
env.reset()

models_dir = "models/A2C"
model_path = f"{models_dir}/50000.zip"

model = A2C.load(model_path, env=env)

'''
model = A2C("MlpPolicy",env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 10000
for i in range(30):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="A2C")
    model.save(f"{models_dir}/{TIMESTEPS * i}")
'''


episodes = 10

for ep in range(episodes):
    obs = env.reset()
    done = False
    while not done:
        env.render()
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)


"""
print("sample action:", env.action_space.sample())

print("observation space shape", env.observation_space.shape)
print("sample observation", env.observation_space.sample())
"""
env.close()