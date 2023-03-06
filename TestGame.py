import pygame

# Initialize Pygame
pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# Define screen dimensions
screen_width = 960
screen_height = 720

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
score = 0
highscore = 0
# Set up the clock
clock = pygame.time.Clock()

# Load car image
car_image = pygame.image.load('car.png')
Rcar_image = pygame.transform.scale(car_image, (45,45))
Ucar_image = pygame.transform.rotate(Rcar_image, (90))
Lcar_image = pygame.transform.rotate(Rcar_image, (180))
Dcar_image = pygame.transform.rotate(Rcar_image, (270))

car_image = Ucar_image
# Define car properties
car_width = 45
car_height = 45
car_x = screen_width // 2 - car_width // 2 
car_y = screen_height // 2 - car_height // 2 + 200
car_speed = 5
Holding = False

gas_width = 20
gas_height = 45
gas_length = gas_height

station_x = screen_width // 2 - 60 // 2 - 200
station_y = screen_height // 2 - 60 // 2

goal_x = screen_width // 2 - 50 // 2 
goal_y = screen_height // 2 - 50 // 2 - 200

PickUp_x = screen_width // 2 - 50 // 2 
PickUp_y = screen_height // 2 - 50 // 2 + 250
# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    # Get the state of the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car_image = Ucar_image
        car_y -= car_speed
        gas_length -= 0.1
    if keys[pygame.K_DOWN]:
        car_image = Dcar_image
        car_y += car_speed
        gas_length -= 0.1
    if keys[pygame.K_LEFT]:
        car_image = Lcar_image
        car_x -= car_speed
        gas_length -= 0.1
    if keys[pygame.K_RIGHT]:
        car_image = Rcar_image
        car_x += car_speed
        gas_length -= 0.1
    if gas_length < 0:
        gas_length = 0

    if abs(car_x - station_x) < 50 and abs(car_y - station_y) < 50 and gas_length < gas_height and not any(keys):
        gas_length += 1

    if abs(car_x - PickUp_x) < 50 and abs(car_y - PickUp_y) < 50 and Holding == False:
        Holding = True

    if abs(car_x - goal_x) < 50 and abs(car_y - goal_y) < 50 and Holding == True:
        score += 1
        Holding = False

    if gas_length == 0:
        # Reset car position and bar length
        car_x = screen_width // 2 - car_width // 2 
        car_y = screen_height // 2 - car_height // 2 + 200
        gas_length = gas_height
        highscore = max(highscore,score)
        score = 0
        
    gas_x = car_x + car_width + 10
    gas_y = car_y
    box_x = car_x + (car_width//2) - 5
    box_y = car_y - 15
    # Fill the screen with white
    screen.fill((255, 255, 255))
    # Draw the car image
    screen.blit(car_image, (car_x, car_y))
    pygame.draw.rect(screen,(0,255,0),(gas_x, gas_y,gas_width,gas_length))

    if Holding == True:
        pygame.draw.rect(screen,(101,67,33),(box_x, box_y,10,10))

    pygame.draw.rect(screen,(255,0,0),(station_x, station_y,60,60))
    pygame.draw.rect(screen,(0,0,255),(goal_x, goal_y,50,50))
    pygame.draw.rect(screen,(0,255,255),(PickUp_x, PickUp_y,50,50))
    text = font.render("Score: " + str(score), True, (0,0,0))
    text1 = font.render("HighScore: " + str(highscore), True, (0,0,0))
    screen.blit(text, [50, 5])
    screen.blit(text1, [200,5])
    # Update the display
    pygame.display.update()
    
    # Tick the clock
    clock.tick(60)
