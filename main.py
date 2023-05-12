import pygame  
import sys  
from tiles import *
from Menu.button import Button
from player import Player
from player import death
from spritesheet import Spritesheet
from camera import *

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("RUN!")
BG = pygame.image.load("assets/Background.png")
FONT = pygame.font.SysFont("Times New Roman", 32)
BLACK = (0, 0, 0)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)
    
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("RUN!", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 300), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game('level1.4.csv', "level1.4.png")
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def game(csv, png):
    pygame.init()  

    # Initializations
    clock = pygame.time.Clock()  
    fps = 60  
    
    pygame.display.set_caption('Run')  
<<<<<<< HEAD
    new_bg = pygame.image.load("level_files/level1.4.png").convert()
=======
    image = pygame.image.load("run_background.webp")
    new_bg = pygame.image.load(png).convert()
>>>>>>> 4bd0b5d632fa339ccf6f39c83ab24db6430483eb

    display_w, display_h = 1000, 800
    canvas = pygame.Surface((display_w, display_w))
    screen = pygame.display.set_mode(((display_w, display_h)))
    running = True  

    # Load Player and Spritesheet
    player = Player()
    camera = Camera(player)
    follow = Follow(camera, player)
    border = Border(camera, player)
    auto = Auto(camera, player)
    camera.setmethod(follow)

    spritesheet = Spritesheet('spritesheet1.png')

    # Load Map 
    map = TileMap(csv, spritesheet)
    map1 = KillerMap(csv, spritesheet)
    map2 = ChainMap(csv, spritesheet)
    player.rect.x, player.rect.y = map.start_x, map.start_y


    while running:  
        dt = clock.tick(60) * .001 * fps
        
        # Player Inputs
        for event in pygame.event.get():  # Allows quitting with the red button
            if event.type == pygame.QUIT:  
                running = False 
                # Horizontal Movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.LEFT_KEY = True
                elif event.key == pygame.K_RIGHT:
                    player.RIGHT_KEY = True
                elif event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_1:
                    camera.setmethod(follow)
                elif event.key == pygame.K_2:
                    camera.setmethod(auto)
                elif event.key == pygame.K_3:
                    camera.setmethod(border)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.LEFT_KEY = False
                elif event.key == pygame.K_RIGHT:
                    player.RIGHT_KEY = False
                elif event.key == pygame.K_SPACE:
                    if player.is_jumping:
                        player.velocity.y *= .25 # quarters upwards velocity when space is let go
                        player.is_jumping = False
        if player.position.y > 850:
            death()   
        # Update Sprite
        player.update(dt, map.tiles, map1.killers, map2.chains)
        camera.scroll()

        canvas.blit(new_bg, (0 - camera.offset.x, 0))
        canvas.blit(player.image, (player.rect.x - camera.offset.x, player.rect.y))
        screen.blit(canvas, (0,0))
        pygame.display.update()  
        clock.tick(fps)
        
        if csv == "level1.4.csv":
            if player.position.x > 3200:
                game('level2.3.csv',"level2.3.png")
        elif csv == "level2.3.csv":
            if player.position.x > 4650:
                pygame.quit()
                pygame.init()
                SCREEN = pygame.display.set_mode((1280, 720))
                BG = pygame.image.load("assets/Background.png")
                while True:
                    SCREEN.blit(BG, (0, 0))

                    MENU_MOUSE_POS = pygame.mouse.get_pos()

                    MENU_TEXT = get_font(80).render("CONGRATULATIONS", True, "#b68f40")
                    MENU_RECT = MENU_TEXT.get_rect(center=(640, 360))
                    
                    QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                                        text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

                    SCREEN.blit(MENU_TEXT, MENU_RECT)

                    for button in [QUIT_BUTTON]:
                        button.changeColor(MENU_MOUSE_POS)
                        button.update(SCREEN)
                    
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
