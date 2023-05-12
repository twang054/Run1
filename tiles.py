import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image,x,y,spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x , self.rect.y = x,y

    def draw(self,surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Killer(pygame.sprite.Sprite):
    def __init__(self, image,x,y,spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x , self.rect.y = x,y
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Chain(pygame.sprite.Sprite):
    def __init__(self, image,x,y,spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x , self.rect.y = x,y
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self,filename, spritesheet):
        self.tile_size = 32 ## Size of the tiles
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()
    
    def draw_map(self, surface):
        surface.blit(self.map_surface, (0,0))
    
    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data,delimiter=',')
            for row in data:
                map.append(list(row))
            return map
    
    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0,0
        for row in map:
            x = 0
            for tile in row:
                if tile == '1':
                    tiles.append(Tile('assets/block.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
    

class KillerMap():
    def __init__(self,filename, spritesheet):
        self.killer_size = 32 ## Size of the tiles
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.killers = self.load_killers(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()
    
    def draw_map(self, surface):
        surface.blit(self.map_surface, (0,0))
    
    def load_map(self):
        for killer in self.killers:
            killer.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data,delimiter=',')
            for row in data:
                map.append(list(row))
            return map
    
    def load_killers(self, filename):
        killers = []
        map = self.read_csv(filename)
        x, y = 0,0
        for row in map:
            x = 0
            for tile in row:
                if tile == '3': ## Substitute filenames
                    killers.append(Killer('assets/hang_spike.png', x * self.killer_size, y * self.killer_size, self.spritesheet))
                elif tile == '4': ## Substitute filenames
                    killers.append(Killer('assets/spike.png', x * self.killer_size, y * self.killer_size, self.spritesheet))
                    
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.killer_size, y * self.killer_size
        return killers
    
class ChainMap():
    def __init__(self,filename, spritesheet):
        self.chain_size = 32 ## Size of the tiles
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.chains = self.load_chains(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()
    
    def draw_map(self, surface):
        surface.blit(self.map_surface, (0,0))
    
    def load_map(self):
        for chain in self.chains:
            chain.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data,delimiter=',')
            for row in data:
                map.append(list(row))
            return map
    
    def load_chains(self, filename):
        chains = []
        map = self.read_csv(filename)
        x, y = 0,0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y = x * self.chain_size, y * self.chain_size
                elif tile == '2':
                    chains.append(Chain('assets/chain.png', x * self.chain_size, y * self.chain_size, self.spritesheet))
                
                x += 1
            y += 1
        self.map_w, self.map_h = x * self.chain_size, y * self.chain_size
        return chains


    