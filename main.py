import pygame  
import sys  
from Menu.button import Button
from player import Player
from player import death
from spritesheet import Spritesheet
from camera import *
from tiles import *

# Initialization
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("RUN!")
BG = pygame.image.load("assets/Background.png")
FONT = pygame.font.SysFont("Times New Roman", 32)
BLACK = (0, 0, 0)

# Gets the Desired Font & Size
def get_font(size): 
    return pygame.font.Font("assets/font.ttf", size)

# Creates the Main Menu    
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("RUN!", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 300), text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500), text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Buttons Change Colors When Mouse Hovers
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        # For Interactions w/ the Main Menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game('level_files/level1.4.csv', "level_files/level1.4.png")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Starts the Game
def game(csv, png): #takes inputs of two file names in order to call back for different levels
    # Initializations
    pygame.init()  
    clock = pygame.time.Clock()  
    fps = 60  
    pygame.display.set_caption('Run')  
    new_bg = pygame.image.load(png).convert()
    display_w, display_h = 1000, 800
    canvas = pygame.Surface((display_w, display_w))
    screen = pygame.display.set_mode(((display_w, display_h)))
    running = True  

    # Loads Player, Camera,and Spritesheet
    player = Player()
    camera = Camera(player)
    follow = Follow(camera, player)
    auto = Auto(camera, player)
    camera.setmethod(follow)
    spritesheet = Spritesheet('spritesheet1.png')

    # Loads Each Sprite Map and sets the player's spawn to (0,0) 
    map = TileMap(csv, spritesheet)
    map1 = KillerMap(csv, spritesheet)
    map2 = ChainMap(csv, spritesheet)
    player.rect.x, player.rect.y = map.start_x, map.start_y

    # Game Loop
    while running:  
        dt = clock.tick(60) * .001 * fps # delta time for physics purposes
        
        # Player Inputs
        for event in pygame.event.get():  # Allows quitting with the red button
            if event.type == pygame.QUIT:  
                running = False 
                # Movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.LEFT_KEY = True
                elif event.key == pygame.K_RIGHT:
                    player.RIGHT_KEY = True
                # Jumping
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
                elif event.key == pygame.K_1:
                    camera.setmethod(follow)
                elif event.key == pygame.K_2:
                    camera.setmethod(auto)
            # Actions when the player releases the key
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.LEFT_KEY = False
                elif event.key == pygame.K_RIGHT:
                    player.RIGHT_KEY = False
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if player.is_jumping:
                        player.velocity.y *= .25 # quarters upwards velocity when space is let go
                        player.is_jumping = False
        # If the player falls off the stage, and screen, it dies, and the game over screen is displayed
        if player.position.y > 850:
            death()   
        
        # Update Sprites & Camera
        player.update(dt, map.tiles, map1.killers, map2.chains)
        camera.scroll()
        canvas.blit(new_bg, (0 - camera.offset.x, 0))
        canvas.blit(player.image, (player.rect.x - camera.offset.x, player.rect.y))
        screen.blit(canvas, (0,0))
        pygame.display.update()  
        clock.tick(fps)
        
        # Level 1 (levels are of different tile lengths)
        if csv == "level_files/level1.4.csv":
            # When Player Completes Level 1, Goes to Level 2
            if player.position.x > 3200:
                game('level_files/level2.3.csv',"level_files/level2.3.png")
        # Level 2
        elif csv == "level_files/level2.3.csv":
            # When Player Completes Level 2
            if player.position.x > 4650:
                pygame.quit()
                # Creates the Congraulations Screen
                pygame.init()
                SCREEN = pygame.display.set_mode((1280, 720))
                BG = pygame.image.load("assets/Background.png")
                while True:
                    SCREEN.blit(BG, (0, 0))
                    MENU_MOUSE_POS = pygame.mouse.get_pos()
                    MENU_TEXT = get_font(80).render("CONGRATULATIONS", True, "#b68f40")
                    MENU_RECT = MENU_TEXT.get_rect(center=(640, 360))
                    QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
                    SCREEN.blit(MENU_TEXT, MENU_RECT)
                    
                    # Buttons Change Colors When Mouse Hovers
                    for button in [QUIT_BUTTON]:
                        button.changeColor(MENU_MOUSE_POS)
                        button.update(SCREEN)
                    
                    # Interactions w/ Congratulations Screen
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                                pygame.quit()
                                sys.exit()

                    pygame.display.update()
         
main_menu()
