from DriveEnv import DriveEnv

env = DriveEnv()
episodes = 2

for i in range(episodes):
    done = False
    obs = env.reset()
    while True:
        random_action = env.action_space.sample()
        print("Action", random_action)
        obs, reward, done, info = env.step(random_action)
        print('reward', reward)
        if (done):
            break
    env.render
