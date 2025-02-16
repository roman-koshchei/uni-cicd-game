import pygame
from pygame.locals import *
from movement.vector import Vector2
from constants import *
from entity import Entity
from modes.modes import ModeController

class Ghost:
    def __init__(self, node, pacman=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goal_direction
        self.pacman = pacman
        self.mode = ModeController(self)
    
    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

    def start_freight(self):
        self.mode.set_freight_mode()
        if self.mode.current == FREIGHT:
            self.set_speed(50)
            self.directionMethod = self.random_direction         

    def normal_mode(self):
        self.set_speed(100)
        self.directionMethod = self.goal_direction

    def spawn(self):
        self.goal = self.spawnNode.position

    def set_spawn_node(self, node):
        self.spawnNode = node

    def start_spawn(self):
        self.mode.set_spawn_node()
        if self.mode.current == SPAWN:
            self.set_speed(150)
            self.directionMethod = self.goal_direction
            self.spawn()
