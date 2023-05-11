import pygame
from spritesheet import Spritesheet

pygame.init()
display_w, display_h = 480, 270
canvas = pygame.Surface((display_w, display_w))
window = pygame.display.set_mode(((display_w, display_h)))
running = True

spritesheet = Spritesheet('spritesheet1.png')

blobby = spritesheet.get_sprite(0,0,64,64)
block = spritesheet.get_sprite(64,0,64,64)
chain = spritesheet.get_sprite(128,0,64,64)
hang_spike = spritesheet.get_sprite(192,0,64,64)
spike = spritesheet.get_sprite(256,0,64,64)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
    
    canvas.fill((255,255,255))
    canvas.blit(blobby, (64, 200))
    canvas.blit(block, (128, 200))
    canvas.blit(chain, (192, 200))
    canvas.blit(hang_spike, (256, 200))
    canvas.blit(spike, (320, 200))

    window.blit(canvas, (0,0))
    pygame.display.update()