import pygame  
import sys  
from tiles import TileMap

from button import Button
from player import Player
from wall import Wall
from spritesheet import Spritesheet

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("RUN!")

BG = pygame.image.load("assets/Background.png")

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
                    game()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def game():
    pygame.init()  

    # Initializations
    clock = pygame.time.Clock()  
    running = True
    fps = 60  
    background = [255, 255, 255]
    pygame.display.set_caption('Run')  
    image = pygame.image.load("run_background.webp")  
    size =[800, 600]  
    screen = pygame.display.set_mode(size)  

    # Load Player
    player = Player()
    player.position.x, player.position.y = 640, 500

    # Map Setup
    map = TileMap('level1..csv', Spritesheet
                )
    player.rect.x, player.rect.y = map.start_x, map.start_y

    # Define keys for player movement  
    player.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE]  
    player

    wall = Wall([100,100])  # The other sprites

    wall_group = pygame.sprite.Group()  # This is how we do collision detections. We'll have to group a bunch of walls
    wall_group.add(wall)  # We'll also have to make another class for walls

    player_group = pygame.sprite.Group()  
    player_group.add(player)  

    while running:  
        dt = clock.tick(60) * .001 * fps
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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.LEFT_KEY = False
                elif event.key == pygame.K_RIGHT:
                    player.RIGHT_KEY = False
                elif event.key == pygame.K_SPACE:
                    if player.is_jumping:
                        player.velocity.y *= .25 # quarters upwards velocity when space is let go
                        player.is_jumping = False

        # Update Sprite
        player.update(dt)

        # Update Screen
        screen.fill(background)
        screen.blit(image,(0, 0))  
        player.draw(screen)

        map.draw_map(screen)

        hit = pygame.sprite.spritecollide(player, wall_group, True)  
        if hit:  
        # if collision is detected call a function to destroy  
            # rect  
            player.image.fill((255, 255, 255))  
        player_group.draw(screen)  
        wall_group.draw(screen)  
        pygame.display.update()  
        clock.tick(fps)  
    pygame.quit()  
    sys.exit  

main_menu()
