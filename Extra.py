import pygame

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width = 640
screen_height = 480

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the clock
clock = pygame.time.Clock()

# Load car image
car_image = pygame.image.load('car.png').convert()
car_image = pygame.transform.scale(car_image, (45,45))
# Define car properties
car_width = 45
car_height = 45
car_x = screen_width // 2 - car_width // 2
car_y = screen_height // 2 - car_height // 2
car_speed = 5

# Define bar properties
bar_width = 20
bar_height = 45
bar_x = car_x + car_width + 10
bar_y = car_y
bar_length = bar_height

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
        car_y -= car_speed
    if keys[pygame.K_DOWN]:
        car_y += car_speed
    if keys[pygame.K_LEFT]:
        car_x -= car_speed
    if keys[pygame.K_RIGHT]:
        car_x += car_speed
    bar_y = car_y
    
    # Update the length of the green bar
    bar_length -= abs(car_speed)
    if bar_length < 0:
        bar_length = 0
    
    # Fill the screen with white
    
    # Draw the car image
    screen.blit(car_image, (car_x, car_y))
    
    # Draw the green bar
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width, bar_length))
    
    # Update the display
    pygame.display.update()
    
    # Tick the clock
    clock.tick(60)
