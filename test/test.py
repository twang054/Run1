# This was used as an inital model to get an idea of how to attack this project

# Import modules
import pygame
import random
import os

# Creates a Window
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Base Case for Run")

# Defines Colors & Fonts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.SysFont("Times New Roman", 32)

# Create the Player 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Sets the image and rect attributes
        self.image = pygame.image.load(os.path.join("test", "avatar.png"))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

        # Sets the initial position and velocity
        self.rect.x = 100
        self.rect.y = 300
        self.change_x = 0
        self.change_y = 0

        # Sets the gravity and jump speed
        self.gravity = 1
        self.jump_speed = -15

    # Updates Player's Position w/ Current Movement
    def update(self):
        # Moves the Player Horizontally
        self.rect.x += self.change_x

        # Checks if the Player is Out of Bounds
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 750:
            self.rect.x = 750

        # Moves the Player Vertically
        self.rect.y += self.change_y

        # Applies Gravity
        self.change_y += self.gravity

        # Checks if Player is on the Ground or Out of Bounds
        if self.rect.y > 550:
            self.rect.y = 550
            self.change_y = 0

    # Defines Jumping
    def jump(self):
        # Jumps if on the ground or hits jumping block
        if self.rect.y == 550 or pygame.sprite.spritecollideany(self, obstacles):
            self.change_y = self.jump_speed
    
    # Defines Movement to the Left
    def move_left(self):
        self.change_x = -5

    # Defines Movement to the Right
    def move_right(self):
        self.change_x = 5

    # Stops Horizontal Movement
    def stop(self):
        self.change_x = 0

# Creates an Obstacle
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Sets the image and rect attributes and creates obstacles
        self.image = pygame.Surface((50, random.randint(10, 20)))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        # Sets the initial position and velocity
        self.rect.x = 800
        self.rect.y = 600 - self.rect.height
        self.change_x = -5

        # Randomly Determines if Obstacle is a Spike or Jumping Block
        self.type = random.choice(["spike", "block"])

        # Obstacle is Green Block
        if self.type == "block":
            self.image.fill(GREEN)
            self.rect.y = 500 - self.rect.height

    # Updates Position of Obstacle
    def update(self):
        self.rect.x += self.change_x

# Creates a Sprite Group for Player and Obstacles
sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)
obstacles = pygame.sprite.Group()

# Creates Score and Clock
score = 0
clock = pygame.time.Clock()

# Creates Game Over & Message
game_over = False
message = ""

# Starts the Test
while True:
    for event in pygame.event.get():
        # Quits the game if user closes the window or presses ESC
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        # Jumps if the user presses SPACE or UP arrow key
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            player.jump()
       
       # Moves left or right if the user presses LEFT or RIGHT arrow key
        elif event.type == pygame.KEYDOWN and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            if event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()

        # Stops moving horizontally if the user releases LEFT or RIGHT arrow key
        elif event.type == pygame.KEYUP and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
            player.stop()
        
    # Updates the sprites if the game is not over
    if not game_over:
        sprites.update()
        obstacles.update()

    # Draws the background, sprites, score, and message on the screen
    screen.fill(WHITE)
    sprites.draw(screen)
    obstacles.draw(screen)
    score_text = FONT.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    message_text = FONT.render(message, True, BLACK)
    screen.blit(message_text, (300, 300))
    pygame.display.flip()

    # Checks for collisions between the player and obstacles
    collisions = pygame.sprite.spritecollide(player, obstacles, False)
    for collision in collisions:
        # If the type is a spike, game is over
        if collision.type == "spike":
            game_over = True
            message = "Game Over!"
        # If type is block, the player jumps
        elif collision.type == "block":
            player.jump()
   
   # Checks if an obstacle has passed the left edge of the screen
    for obstacle in obstacles:
        # Removes the obstacle from the sprite groups and increasesthe score
        if obstacle.rect.x < -50:
            obstacle.kill()
            score += 1

    # Creates a new obstacle every 0.05 seconds
    if pygame.time.get_ticks() % 50 == 0:
        obstacle = Obstacle()
        sprites.add(obstacle)
        obstacles.add(obstacle)

    # Limits the frame rate to 60 FPS
    clock.tick(60)