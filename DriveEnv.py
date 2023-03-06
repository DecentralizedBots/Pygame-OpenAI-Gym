import gym
from gym import spaces
import pygame
from collections import deque
import numpy as np

LEN_GOAL = 300
pygame.init()

class DriveEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self):
        super(DriveEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(4)
        # Example for using image as input (channel-first; channel-last also works):
        observation = self.reset()

        shape1 = (9 + LEN_GOAL,)
        dtype1 = np.int64
        self.observation_space = spaces.Box(low=-1000, high=1000,
                                            shape = shape1, dtype= dtype1)

    def step(self, action):
        self.prev_actions.append(action)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        

    
        # Get the state of the arrow keys
        if action == 0:
            self.car_image = self.Ucar_image
            self.car_y -= self.car_speed
            self.gas_length -= 0.1
        if action == 1:
            self.car_image = self.Dcar_image
            self.car_y += self.car_speed
            self.gas_length -= 0.1
        if action == 2:
            self.car_image = self.Lcar_image
            self.car_x -= self.car_speed
            self.gas_length -= 0.1
        if action == 3:
            self.car_image = self.Rcar_image
            self.car_x += self.car_speed
            self.gas_length -= 0.1
        if self.gas_length < 0:
            self.gas_length = 0

        if abs(self.car_x -self.station_x) < 50 and abs(self.car_y - self.station_y) < 50 and self.gas_length < self.gas_height:
            self.gas_length += 1

        if abs(self.car_x - self.PickUp_x) < 50 and abs(self.car_y - self.PickUp_y) < 50 and self.Holding == False:
            self.Holding = True

        if abs(self.car_x - self.goal_x) < 50 and abs(self.car_y - self.goal_y) < 50 and self.Holding == True:
            self.score += 1
            self.Holding = False

        if self.gas_length == 0:
            # Reset car position and bar length
            self.done = True
            
        self.gas_x = self.car_x + self.car_width + 10
        self.gas_y = self.car_y
        self.box_x = self.car_x + (self.car_width//2) - 5
        self.box_y = self.car_y - 15
        # Fill the screen with white
        self.screen.fill((255, 255, 255))
        # Draw the car image
        self.screen.blit(self.car_image, (self.car_x, self.car_y))
        pygame.draw.rect(self.screen,(0,255,0),(self.gas_x, self.gas_y,self.gas_width,self.gas_length))

        if self.Holding == True:
            pygame.draw.rect(self.screen,(101,67,33),(self.box_x, self.box_y,10,10))

        pygame.draw.rect(self.screen,(255,0,0),(self.station_x, self.station_y,60,60))
        pygame.draw.rect(self.screen,(0,0,255),(self.goal_x, self.goal_y,50,50))
        pygame.draw.rect(self.screen,(0,255,255),(self.PickUp_x, self.PickUp_y,50,50))
        text = self.font.render("Score: " + str(self.score), True, (0,0,0))
        text1 = self.font.render("HighScore: " + str(self.highscore), True, (0,0,0))
        self.screen.blit(text, [50, 5])
        self.screen.blit(text1, [200,5])
        # Update the display
        pygame.display.update()
        
        # Tick the clock
        self.clock.tick(60)

        if self.done:
            self.reward = -10
        else:
            self.reward = self.score * 10

        car_x = self.car_x
        car_y = self.car_y
        goal_delta_x = car_x - self.goal_x
        goal_delta_y = car_y - self.goal_y
        PU_delta_x = car_x - self.PickUp_x
        PU_delta_y = car_y - self.PickUp_y
        gas_delta_x = car_x - self.station_x
        gas_delta_y = car_y - self.station_y
        gas_level = self.gas_length

        self.observation = [car_x,car_y,goal_delta_x,goal_delta_y,PU_delta_x,PU_delta_y,gas_delta_x,gas_delta_y,gas_level] + list(self.prev_actions)
        self.observation = np.array(self.observation)

        self.info = {}
        return self.observation, self.reward, self.done, self.info


    def reset(self):
        self.done=False
        self.font = pygame.font.Font('arial.ttf', 25)

        # Define screen dimensions
        self.screen_width = 960
        self.screen_height = 720

        # Set up the display
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.score = 0
        self.highscore = 0
        # Set up the clock
        self.clock = pygame.time.Clock()

        # Load car image
        self.car_image = pygame.image.load('car.png')
        self.Rcar_image = pygame.transform.scale(self.car_image, (45,45))
        self.Ucar_image = pygame.transform.rotate(self.Rcar_image, (90))
        self.Lcar_image = pygame.transform.rotate(self.Rcar_image, (180))
        self.Dcar_image = pygame.transform.rotate(self.Rcar_image, (270))

        self.car_image = self.Ucar_image
        #Define car properties
        self.car_width = 45
        self.car_height = 45
        self.car_x = self.screen_width // 2 - self.car_width // 2 
        self.car_y = self.screen_height // 2 - self.car_height // 2 + 200
        self.car_speed = 5
        self.Holding = False

        self.gas_width = 20
        self.gas_height = 45
        self.gas_length = self.gas_height

        self.station_x = self.screen_width // 2 - 60 // 2 - 200
        self.station_y = self.screen_height // 2 - 60 // 2

        self.goal_x = self.screen_width // 2 - 50 // 2 
        self.goal_y = self.screen_height // 2 - 50 // 2 - 200

        self.PickUp_x = self.screen_width // 2 - 50 // 2 
        self.PickUp_y = self.screen_height // 2 - 50 // 2 + 250

        #car_x,car_y,goal_x,goal_y, PickUp_x,PickUp_y, gas_level, previous moves

        car_x = self.car_x
        car_y = self.car_y
        goal_delta_x = car_x - self.goal_x
        goal_delta_y = car_y - self.goal_y
        PU_delta_x = car_x - self.PickUp_x
        PU_delta_y = car_y - self.PickUp_y
        gas_delta_x = car_x - self.station_x
        gas_delta_y = car_y - self.station_y
        gas_level = self.gas_length

        self.prev_actions = deque(maxlen=LEN_GOAL)
        for i in range(LEN_GOAL):
            self.prev_actions.append(-1)

        temp= [car_x,car_y,goal_delta_x,goal_delta_y,PU_delta_x,PU_delta_y,gas_delta_x,gas_delta_y,gas_level] + list(self.prev_actions)
        self.observation = np.array(temp)

        print(self.observation)

        return self.observation  # reward, done, info can't be included
