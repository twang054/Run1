import pygame
from spritesheet import Spritesheet

spritesheet = Spritesheet('spritesheet1.png')
sprite_size = (100,100)
horizontal_acceleration = 5
ground_y = 600
velocity_cap = 15
class Player(pygame.sprite.Sprite):  
    def __init__(self):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = spritesheet.get_sprite(0,0,64,64)
        self.image = pygame.transform.scale(self.image, (100,100))
        self.rect = self.image.get_rect()
        self.LEFT_KEY, self.RIGHT_KEY= False, False
        self.is_jumping, self.on_ground, self.friction = False, True, False
        self.gravity, self.friction = .5, -.12
        self.position, self.velocity = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,self.gravity)
        
    
    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self, dt):
        self.horizontal_movement(dt)
        self.vertical_movement(dt)
    
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
    
    def vertical_movement(self,dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > velocity_cap: self.velocity.y = velocity_cap
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        if self.position.y > ground_y:
            self.on_ground = True
            self.velocity.y = 0
            self.position.y = ground_y
        self.rect.bottom = self.position.y
    
    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 12
            self.on_ground = False
