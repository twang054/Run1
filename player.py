# Import Necessary Modules
import pygame
import sys
from spritesheet import Spritesheet
from Menu.button import Button

# Intialization of Variables
spritesheet = Spritesheet('spritesheet1.png')
horizontal_acceleration = 5
ground_y = 1440
velocity_cap = 15

# Returns the Desired Font & Size
def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

# When a Player Dies
def death():
    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 720))
    BG = pygame.image.load("assets/Background.png")
    while True:

        #Creates the Death Screen
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("GAME OVER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500), text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Button Changes Color When Mouse Hovers
        for button in [QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        # For Interactions w/ the Death Screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Creates the Main Player Class
class Player(pygame.sprite.Sprite):  
    # Initialization 
    def __init__(self):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = spritesheet.get_sprite(0,0,64,64) # Creates sprite image
        self.image = pygame.transform.scale(self.image, (25,25)) # Scales to appropriate size
        self.rect = self.image.get_rect() # Gives player rect. properties
        
        # Physics parameters
        self.LEFT_KEY, self.RIGHT_KEY= False, False
        self.is_jumping, self.on_ground, self.friction = False, True, False
        self.gravity, self.friction = 1, -.5
        self.position, self.velocity = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,self.gravity)
        self.ground_y = 350
        self.left_border, self.right_border = 250, 4700

    # Draws the Player
    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
    
    # Updates the Player's Position and updates collision information
    def update(self, dt, tiles, killers, chains):
        self.horizontal_movement(dt)
        self.checkCollisionsx(tiles, killers)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles, killers)

    # Defines Horizontal Movement
    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= horizontal_acceleration
        elif self.RIGHT_KEY:
            self.acceleration.x += horizontal_acceleration
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x
        
        # Prevents the Player from Going Off Screen
        if self.rect.x < 0:
            self.rect.x = 0

    # Defines Vertical Movement 
    def vertical_movement(self,dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > velocity_cap: self.velocity.y = velocity_cap
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        if self.position.y > ground_y:
            self.on_ground = True
            self.velocity.y = 0
            self.position.y = ground_y
        self.rect.bottom = self.position.y

    # Defines Jumping Motion
    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 20
            self.on_ground = False

    # Collects the collisions of the player and blocks that kill.
    # Notably there is no get_ interaction for chains because we want there to
    # be no collision.
    def get_kills(self, killers):
        killed = []
        for killer in killers:
            if self.rect.colliderect(killer):
                killed.append(killer)
        return killed
    
    # Collects the collisions of the player and tiles
    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits
    
    # Determines the nature of the collisions in the x-direction
    def checkCollisionsx(self, tiles, killers):
        collisions = self.get_hits(tiles)
        kills = self.get_kills(killers)
        for tile in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tile.rect.right
                self.rect.x = self.position.x
        # When the Player collides with a killing object, it kills the player
        for killer in kills:
            if self.velocity.x > 0:
                death()
            elif self.velocity.x < 0:
                death()
    
    # Determines the nature of the collisions in the y-direction         
    def checkCollisionsy(self, tiles, killers):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        kills = self.get_kills(killers)
        for tile in collisions:
            if self.velocity.y > 0:  # Hit tile from the top
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:  # Hit tile from the bottom
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y
        # Player collides with killing object, player dies
        for killer in kills:
            if self.velocity.y > 0:
                death()
            elif self.velocity.y < 0:
                death()
