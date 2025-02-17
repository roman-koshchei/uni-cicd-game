import pygame
from movement.vector import Vector2
from constants import *
import numpy as np

class Pellet(object):
    def __init__(self, row, column, sprite_manager=None):
        self.name = PELLET
        self.position = Vector2(
            column * TILEWIDTH + TILEWIDTH // 2,
            row * TILEHEIGHT + TILEHEIGHT // 2
        )
        self.color = WHITE
        self.radius = int(2 * TILEWIDTH / 16)
        self.collideRadius = int(2 * TILEWIDTH / 16)
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
        self.radius = int(6 * TILEWIDTH / 16)
        self.collideRadius = int(6 * TILEWIDTH / 16)
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
    def __init__(self, level_data, sprite_manager=None):
        self.pelletList = []
        self.powerpellets = []
        self.sprite_manager = sprite_manager
        self.create_pellet_list(level_data)
        self.numEaten = 0

    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)
                
    def create_pellet_list(self, level_data):
        # Convert to numpy array if it's not already
        data = np.array(level_data) if not isinstance(level_data, np.ndarray) else level_data
        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] == 1:  # Regular pellet
                    self.pelletList.append(Pellet(row, col, self.sprite_manager))
                elif data[row][col] == 2:  # Power pellet
                    pp = PowerPellet(row, col, self.sprite_manager)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)
    
    def is_empty(self):
        if len(self.pelletList) == 0:
            return True
        return False
    
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)