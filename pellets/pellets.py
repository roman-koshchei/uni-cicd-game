import pygame
from movement.vector import Vector2
from constants import *
import numpy as np

from sprites.sprite_manager import SpriteManager


class Pellet(object):
    def __init__(
        self, row: int, column: int, sprite_manager: SpriteManager | None = None
    ):
        self.name = PELLET
        self.position = Vector2(
            column * TILEWIDTH + TILEWIDTH // 2, row * TILEHEIGHT + TILEHEIGHT // 2
        )
        self.color = WHITE
        self.radius = int(TILEWIDTH * 0.125)
        self.collideRadius = int(TILEWIDTH * 0.125)
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
                        int(self.position.y - sprite.get_height() // 2),
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
        self.radius = int(TILEWIDTH * 0.35)
        self.collideRadius = int(TILEWIDTH * 0.35)
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
                        int(self.position.y - sprite.get_height() // 2),
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
        self.pellet_list: list[Pellet] = []
        self.power_pellet_list: list[PowerPellet] = []
        self.sprite_manager: SpriteManager = sprite_manager
        self.eaten_count = 0

        self.create_pellet_list(level_data)

    def update(self, dt):
        for powerpellet in self.power_pellet_list:
            powerpellet.update(dt)

    def create_pellet_list(self, level_data):
        # Convert to numpy array if it's not already
        data = (
            np.array(level_data)
            if not isinstance(level_data, np.ndarray)
            else level_data
        )

        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                cell = data[row][col]

                if cell == PELLET:
                    self.pellet_list.append(Pellet(row, col, self.sprite_manager))
                elif cell == POWERPELLET:
                    pp = PowerPellet(row, col, self.sprite_manager)
                    self.pellet_list.append(pp)
                    self.power_pellet_list.append(pp)

    def is_empty(self):
        return len(self.pellet_list) == 0

    def render(self, screen):
        for pellet in self.pellet_list:
            pellet.render(screen)
