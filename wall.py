import pygame

class Wall(pygame.sprite.Sprite):  
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([20, 20])  
        self.image.fill((255, 0, 255))  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  