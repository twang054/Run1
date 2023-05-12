import pygame

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename)

    # takes the spritesheet png and divides it into 5 sections, one for each sprite.
    # The x and y values represent the top left corner of each png to be cut, and the w
    # and height are the size of the png. 
    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0)) # For transparency purposes
        sprite.blit(self.sprite_sheet,(0,0),(x,y,w,h))
        return sprite
    