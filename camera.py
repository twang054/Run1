# Imports
import pygame
vec = pygame.math.Vector2
from abc import ABC, abstractmethod

# Creates Viewing Frame of Player
class Camera:
    # Initialization
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.DISPLAY_W, self.DISPLAY_H = 480, 270
        self.CONST = vec(-self.DISPLAY_W / 2 + player.rect.w / 2, -self.player.ground_y + 20)
    
    # Sets the Camera Scrolling Method
    def setmethod(self, method):
        self.method = method

    # Defines Scrolling
    def scroll(self):
        self.method.scroll()

# General Camera Scrolling
class CamScroll(ABC):
    def __init__(self, camera,player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass

# Defines Follow Method of Camera Scrolling
class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = min(self.camera.offset.x, self.player.right_border - self.camera.DISPLAY_W)

# Defines Auto Method of Camera Scrolling
class Auto(CamScroll):
    def __init__(self,camera,player):
        CamScroll.__init__(self,camera,player)

    def scroll(self):
        self.camera.offset.x += 1









