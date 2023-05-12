# Import pygame, os, and random modules
import pygame
import random
import os

# Initialize pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Base Case for Run")

# Define some colors and fonts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.SysFont("Times New Roman", 32)

# Create the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Parent class constructor
        super().__init__()

        # Set the image and rect attributes
        self.image = pygame.image.load(os.path.join("test", "avatar.png"))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        # Set the initial position and velocity
        self.rect.x = 100
        self.rect.y = 300
        self.change_x = 0
        self.change_y = 0

        # Set the gravity and jump speed
        self.gravity = 1
        self.jump_speed = -15

    def update(self):
        # Move the player horizontally
        self.rect.x += self.change_x

        # Check if the player is out of bounds
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 750:
            self.rect.x = 750

        # Move the player vertically
        self.rect.y += self.change_y

        # Apply gravity
        self.change_y += self.gravity

        # Check if the player is on the ground or out of bounds
        if self.rect.y > 550:
            self.rect.y = 550
            self.change_y = 0

    def jump(self):
        # Make the player jump if on the ground or hits jumping block
        if self.rect.y == 550 or pygame.sprite.spritecollideany(self, obstacles):
            self.change_y = self.jump_speed
    
    def move_left(self):
        # Make the player move left
        self.change_x = -5

    def move_right(self):
        # Make the player move right
        self.change_x = 5

    def stop(self):
        # Make the player stop moving horizontally
        self.change_x = 0

# Create an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        # Parent class constructor
        super().__init__()

        # Set the image and rect attributes
        # Creates the obstacles
        self.image = pygame.Surface((50, random.randint(10, 20)))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        # Set the initial position and velocity
        self.rect.x = 800
        self.rect.y = 600 - self.rect.height
        self.change_x = -5

        # Randomly determines if an obstacle is a spike or jumping block
        self.type = random.choice(["spike", "block"])

        # If obstacle is block
        if self.type == "block":
            self.image.fill(GREEN)
            self.rect.y = 500 - self.rect.height

    def update(self):
        # Move the obstacle horizontally
        self.rect.x += self.change_x

# Create a sprite group for the player and obstacles
sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)
obstacles = pygame.sprite.Group()

# Create a score variable and a clock object
score = 0
clock = pygame.time.Clock()

# Create a game over flag and a message
game_over = False
message = ""

# Main loop
while True:
    # Process events
    for event in pygame.event.get():
        # Quit the game if the user closes the window or presses ESC
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        # Make the player jump if the user presses SPACE or UP arrow key
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            player.jump()
       
       # Make the player move left or right if the user presses LEFT or RIGHT arrow key
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()

        # Make the player stop moving horizontally if the user releases LEFT or RIGHT arrow key
        elif event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            player.stop()
        


    # Update the sprites if the game is not over
    if not game_over:
        sprites.update()
        obstacles.update()

    # Draw the background, sprites, score and message on the screen
    screen.fill(WHITE)
    sprites.draw(screen)
    obstacles.draw(screen)
    score_text = FONT.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    message_text = FONT.render(message, True, BLACK)
    screen.blit(message_text, (300, 300))

    # Update the display
    pygame.display.flip()

    # Check for collisions between the player and obstacles
    collisions = pygame.sprite.spritecollide(player, obstacles, False)

    # If there is a collision
    for collision in collisions:
        
        # If the type is a spike, game is over
        if collision.type == "spike":
            game_over = True
            message = "Game Over!"
        
        # If type is block, the player jumps
        elif collision.type == "block":
            player.jump()
   
   # Check if an obstacle has passed the left edge of the screen
    for obstacle in obstacles:
        if obstacle.rect.x < -50:
                # Remove the obstacle from the sprite groups and increase the score
            obstacle.kill()
            score += 1

    # Create a new obstacle every 0.05 seconds
    if pygame.time.get_ticks() % 50 == 0:
        obstacle = Obstacle()
        sprites.add(obstacle)
        obstacles.add(obstacle)

    # Limit the frame rate to 60 FPS
    clock.tick(60)
