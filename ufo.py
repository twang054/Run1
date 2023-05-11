import pygame

pos = (1000, 500) #position of the ufo

class Ufo(pygame.sprite.Sprite):
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([45, 45])  # Sets the size of the sprite
        self.image.fill((255, 0, 0))  # Sets the color of the sprite (red)
        self.rect = self.image.get_rect()  
        self.rect.center = pos  #position