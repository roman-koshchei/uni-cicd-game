import pygame
from movement.vector import Vector2
from constants import *
import numpy as np

class Pellet(object):
    def __init__(self, row, column, sprite_manager=None):
        self.name = PELLET
        self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT)
        self.color = WHITE
        self.radius = int(4 * TILEWIDTH / 16)
        self.collideRadius = int(4 * TILEWIDTH / 16)
        self.points = 10
        self.visible = True
        self.sprite_manager = sprite_manager
        
    def render(self, screen):
        if self.visible:
            if self.sprite_manager:
                sprite = self.sprite_manager.get_sprite("pellet")
                if sprite:
                    position = (
                        int(self.position.x - sprite.get_width() // 2),
                        int(self.position.y - sprite.get_height() // 2)
                    )
                    screen.blit(sprite, position)
                else:
                    p = self.position.as_int()
                    pygame.draw.circle(screen, self.color, p, self.radius)
            else:
                p = self.position.as_int()
                pygame.draw.circle(screen, self.color, p, self.radius)


class PowerPellet(Pellet):
    def __init__(self, row, column, sprite_manager=None):
        Pellet.__init__(self, row, column, sprite_manager)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0
        
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0

    def render(self, screen):
        if self.visible:
            if self.sprite_manager:
                sprite = self.sprite_manager.get_sprite("powerpellet")
                if sprite:
                    position = (
                        int(self.position.x - sprite.get_width() // 2),
                        int(self.position.y - sprite.get_height() // 2)
                    )
                    screen.blit(sprite, position)
                else:
                    p = self.position.as_int()
                    pygame.draw.circle(screen, self.color, p, self.radius)
            else:
                p = self.position.as_int()
                pygame.draw.circle(screen, self.color, p, self.radius)

class PelletGroup(object):
    def __init__(self, pelletfile, sprite_manager=None):
        self.pelletList = []
        self.powerpellets = []
        self.sprite_manager = sprite_manager
        self.create_pellet_list(pelletfile)
        self.numEaten = 0

    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)
                
    def create_pellet_list(self, pelletfile):
        data = self.read_pellet_file(pelletfile)        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pelletList.append(Pellet(row, col, self.sprite_manager))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col, self.sprite_manager)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)
                    
    def read_pellet_file(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    def is_empty(self):
        if len(self.pelletList) == 0:
            return True
        return False
    
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)