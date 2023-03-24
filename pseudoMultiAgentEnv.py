import gym
from gym import spaces
import pygame
from collections import deque
import numpy as np
import math

LEN_GOAL = 300
pygame.init()

class DriveEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self):
        super(DriveEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(10)
        # Example for using image as input (channel-first; channel-last also works):
        observation = self.reset()

        shape1 = (20 + LEN_GOAL,)
        dtype1 = np.int64
        self.observation_space = spaces.Box(low=-1000, high=1000,
                                            shape = shape1, dtype= dtype1)



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

        # Load car1 image
        self.car1_image = pygame.image.load('car1.png')
        self.Rcar1_image = pygame.transform.scale(self.car1_image, (45,45))
        self.Ucar1_image = pygame.transform.rotate(self.Rcar1_image, (90))
        self.Lcar1_image = pygame.transform.rotate(self.Rcar1_image, (180))
        self.Dcar1_image = pygame.transform.rotate(self.Rcar1_image, (270))

        self.car1_image = self.Ucar1_image

        # Load Car2 image
        self.car2_image = pygame.image.load('car2.png')
        self.Rcar2_image = pygame.transform.scale(self.car2_image, (45,45))
        self.Ucar2_image = pygame.transform.rotate(self.Rcar2_image, (90))
        self.Lcar2_image = pygame.transform.rotate(self.Rcar2_image, (180))
        self.Dcar2_image = pygame.transform.rotate(self.Rcar2_image, (270))

        self.car2_image = self.Ucar2_image

        #Define car1 properties
        self.car1_width = 45
        self.car1_height = 45
        self.car1_x = self.screen_width // 2 - self.car1_width // 2 
        self.car1_y = self.screen_height // 2 - self.car1_height // 2 + 200
        self.car1_speed = 5
        self.car1_Holding = False

        self.car1_gas_width = 20
        self.gas_height = 45
        self.car1_gas_length = self.gas_height

        #Define car2 properties
        self.car2_width = 45
        self.car2_height = 45
        self.car2_x = self.screen_width // 3 - self.car2_width // 2 
        self.car2_y = self.screen_height // 3 - self.car2_height // 2 + 200
        self.car2_speed = 5
        self.car2_Holding = False

        self.car2_gas_width = 20
        self.car2_gas_length = self.gas_height


        # Defining places
        self.station_x = self.screen_width // 2 - 60 // 2 - 200
        self.station_y = self.screen_height // 2 - 60 // 2

        self.goal_x = self.screen_width // 2 - 50 // 2 
        self.goal_y = self.screen_height // 2 - 50 // 2 - 200

        self.PickUp_x = self.screen_width // 2 - 50 // 2 
        self.PickUp_y = self.screen_height // 2 - 50 // 2 + 250

        #car1_x,car1_y,goal_x,goal_y, PickUp_x,PickUp_y, gas_level, previous moves

        # Observation for car1
        car1_x = self.car1_x
        car1_y = self.car1_y
        goal1_delta_x = car1_x - self.goal_x
        goal1_delta_y = car1_y - self.goal_y
        PU1_delta_x = car1_x - self.PickUp_x
        PU1_delta_y = car1_y - self.PickUp_y
        gas1_delta_x = car1_x - self.station_x
        gas1_delta_y = car1_y - self.station_y
        car1_gas_level = self.car1_gas_length
        car1_Holding = self.car1_Holding

        # Observation for car2
        car2_x = self.car2_x
        car2_y = self.car2_y
        goal2_delta_x = car2_x - self.goal_x
        goal2_delta_y = car2_y - self.goal_y
        PU2_delta_x = car2_x - self.PickUp_x
        PU2_delta_y = car2_y - self.PickUp_y
        gas2_delta_x = car2_x - self.station_x
        gas2_delta_y = car2_y - self.station_y
        car2_gas_level = self.car2_gas_length
        car2_Holding = self.car2_Holding


        self.prev_actions = deque(maxlen=LEN_GOAL)

        for i in range(LEN_GOAL):
            self.prev_actions.append(-1)


        car1_temp= [car1_x,car1_y,goal1_delta_x,goal1_delta_y,PU1_delta_x,PU1_delta_y,gas1_delta_x,gas1_delta_y,car1_gas_level,car1_Holding]
        car2_temp= [car2_x,car2_y,goal2_delta_x,goal2_delta_y,PU2_delta_x,PU2_delta_y,gas2_delta_x,gas2_delta_y,car2_gas_level,car2_Holding]
        
        obs_wrap = car1_temp + car2_temp + list(self.prev_actions)
        self.observation = np.array(obs_wrap)

        #print(self.observation)


        # storing parameters for reward
        self.prev_distances = deque()
        car1_gasDist = (gas1_delta_x**2 + gas1_delta_y**2) ** (1/2)
        car2_gasDist = (gas2_delta_x**2 + gas1_delta_y**2) ** (1/2)
        car1_goalDist = (goal1_delta_x**2 + goal1_delta_y**2) ** (1/2)
        car2_goalDist = (goal2_delta_x**2 + goal2_delta_y**2) ** (1/2)
        
        self.prev_distances.append(car1_goalDist)
        self.prev_distances.append(car2_goalDist)
        self.prev_distances.append(car1_gasDist)
        self.prev_distances.append(car2_gasDist)


        return self.observation  # reward, done, info can't be included
    


    def step(self, action):
        self.prev_actions.append(action)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        # Get the state of the arrow keys
        # Actions for Car 1
        if action == 0:
            self.car1_image = self.Ucar1_image
            self.car1_y -= self.car1_speed
            self.car1_gas_length -= 0.1
        if action == 1:
            self.car1_image = self.Dcar1_image
            self.car1_y += self.car1_speed
            self.car1_gas_length -= 0.1
        if action == 2:
            self.car1_image = self.Lcar1_image
            self.car1_x -= self.car1_speed
            self.car1_gas_length -= 0.1
        if action == 3:
            self.car_image = self.Rcar1_image
            self.car1_x += self.car1_speed
            self.car1_gas_length -= 0.1

        if self.car1_gas_length < 0:
            self.car1_gas_length = 0


        # Actions for Car 2
        if action == 5:
            self.car2_image = self.Ucar2_image
            self.car2_y -= self.car2_speed
            self.car2_gas_length -= 0.1
        if action == 6:
            self.car2_image = self.Dcar2_image
            self.car2_y += self.car2_speed
            self.car2_gas_length -= 0.1
        if action == 7:
            self.car2_image = self.Lcar2_image
            self.car2_x -= self.car2_speed
            self.car2_gas_length -= 0.1
        if action == 8:
            self.car2_image = self.Rcar2_image
            self.car2_x += self.car2_speed
            self.car2_gas_length -= 0.1

        if self.car2_gas_length < 0:
            self.car2_gas_length = 0


        # Adding gas for Car1

        if abs(self.car1_x -self.station_x) < 50 and abs(self.car1_y - self.station_y) < 50 and self.car1_gas_length < self.gas_height:
            self.car1_gas_length += 1

        if abs(self.car1_x - self.PickUp_x) < 50 and abs(self.car1_y - self.PickUp_y) < 50 and self.car1_Holding == False:
            self.car1_Holding = True

        if abs(self.car1_x - self.goal_x) < 50 and abs(self.car1_y - self.goal_y) < 50 and self.car1_Holding == True:
            self.score += 1
            self.car1_Holding = False

        # Adding gas for Car2
        if abs(self.car2_x -self.station_x) < 50 and abs(self.car2_y - self.station_y) < 50 and self.car2_gas_length < self.gas_height:
            self.car2_gas_length += 1

        if abs(self.car2_x - self.PickUp_x) < 50 and abs(self.car2_y - self.PickUp_y) < 50 and self.car2_Holding == False:
            self.car2_Holding = True

        if abs(self.car2_x - self.goal_x) < 50 and abs(self.car2_y - self.goal_y) < 50 and self.car2_Holding == True:
            self.score += 1
            self.car2_Holding = False


        if self.car1_gas_length == 0 or self.car2_gas_length == 0:
            # Reset car position and bar length
            self.done = True

        # Collaboration
        if  abs(self.car1_x - self.car2_x) < 50 and abs(self.car1_y - self.car2_y) < 50:
            if self.car1_Holding == False and self.car2_Holding == True and action == 9:
                self.car1_Holding = True
                self.car2_Holding = False

            elif self.car1_Holding == True and self.car2_Holding == False and action == 5:
                self.car1_Holding = False
                self.car2_Holding = True
        

        # Label for car 1
        self.car1_gas_x = self.car1_x + self.car1_width + 10
        self.car1_gas_y = self.car1_y
        self.car1_box_x = self.car1_x + (self.car1_width//2) - 5
        self.car1_box_y = self.car1_y - 15

        # Label for car2
        self.car2_gas_x = self.car2_x + self.car2_width + 10
        self.car2_gas_y = self.car2_y
        self.car2_box_x = self.car2_x + (self.car2_width//2) - 5
        self.car2_box_y = self.car2_y - 15


        # Fill the screen with white
        self.screen.fill((255, 255, 255))

        # Draw the car1 image
        self.screen.blit(self.car1_image, (self.car1_x, self.car1_y))
        pygame.draw.rect(self.screen,(0,255,0),(self.car1_gas_x, self.car1_gas_y,self.car1_gas_width,self.car1_gas_length))

        if self.car1_Holding == True:
            pygame.draw.rect(self.screen,(101,67,33),(self.car1_box_x, self.car1_box_y,10,10))
        
        # Draw the car2 image
        self.screen.blit(self.car2_image, (self.car2_x, self.car2_y))
        pygame.draw.rect(self.screen,(0,255,0),(self.car2_gas_x, self.car2_gas_y,self.car2_gas_width,self.car2_gas_length))

        if self.car2_Holding == True:
            pygame.draw.rect(self.screen,(101,67,33),(self.car2_box_x, self.car2_box_y,10,10))


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
        self.clock.tick(120)


        # reward part

        if self.done:
            self.reward = -10
        else:
            self.reward = self.score * 10


        # Observation for car1
        car1_x = self.car1_x
        car1_y = self.car1_y
        goal1_delta_x = car1_x - self.goal_x
        goal1_delta_y = car1_y - self.goal_y
        PU1_delta_x = car1_x - self.PickUp_x
        PU1_delta_y = car1_y - self.PickUp_y
        gas1_delta_x = car1_x - self.station_x
        gas1_delta_y = car1_y - self.station_y
        car1_gas_level = self.car1_gas_length
        car1_Holding = self.car1_Holding

        # Observation for car2
        car2_x = self.car2_x
        car2_y = self.car2_y
        goal2_delta_x = car2_x - self.goal_x
        goal2_delta_y = car2_y - self.goal_y
        PU2_delta_x = car2_x - self.PickUp_x
        PU2_delta_y = car2_y - self.PickUp_y
        gas2_delta_x = car2_x - self.station_x
        gas2_delta_y = car2_y - self.station_y
        car2_gas_level = self.car2_gas_length
        car2_Holding = self.car2_Holding

        car1_temp= [car1_x,car1_y,goal1_delta_x,goal1_delta_y,PU1_delta_x,PU1_delta_y,gas1_delta_x,gas1_delta_y,car1_gas_level,car1_Holding]
        car2_temp= [car2_x,car2_y,goal2_delta_x,goal2_delta_y,PU2_delta_x,PU2_delta_y,gas2_delta_x,gas2_delta_y,car2_gas_level,car2_Holding]
        
        obs_wrap = car1_temp + car2_temp + list(self.prev_actions)
        self.observation = np.array(obs_wrap)

        self.info = {}

        # reward part 2
        prev_car1_goalDist = self.prev_distances.popleft()
        prev_car2_goalDist = self.prev_distances.popleft()
        prev_car1_gasDist =  self.prev_distances.popleft()
        prev_car2_gasDist = self.prev_distances.popleft()

        car1_goalDist = (goal1_delta_x**2 + goal1_delta_y**2) ** (1/2)
        car2_goalDist = (goal2_delta_x**2 + goal2_delta_y**2) ** (1/2)
        car1_gasDist = (gas1_delta_x**2 + gas1_delta_y**2) ** (1/2)
        car2_gasDist = (gas2_delta_x**2 + gas2_delta_y**2) ** (1/2)

        if car1_goalDist <= prev_car1_goalDist or car2_goalDist <= prev_car2_goalDist:
            self.reward += 3
        
        if car1_gasDist <= prev_car1_gasDist or car2_gasDist <= prev_car2_gasDist:
            self.reward += 1
        
        self.prev_distances.append(car1_goalDist)
        self.prev_distances.append(car2_goalDist)
        self.prev_distances.append(car1_gasDist)
        self.prev_distances.append(car2_gasDist)

        return self.observation, self.reward, self.done, self.info


    