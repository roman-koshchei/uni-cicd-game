import pygame
from pygame.locals import *
from movement.vector import Vector2
from constants import *
from ghosts.entity import Entity

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.position = Vector2(200, 400)
        self.directions = {
            UP: Vector2(0, -1),
            DOWN: Vector2(0, 1),
            LEFT: Vector2(-1, 0),
            RIGHT: Vector2(1, 0),
            STOP: Vector2(),
        }
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.set_position()
        self.target = node
        self.collideRadius = 5

    def eat_pellets(self, pelletList):
        for pellet in pelletList:
            if self.collide_check(pellet):
                return pellet
        return None
    
    def collide_ghost(self, ghost):
        return self.collide_check(ghost)

    def collide_check(self, other):
        d = self.position - other.position
        dSquared = d.magnitude_squared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False

    def set_position(self):
        self.position = self.node.position.copy()

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.get_valid_key()

        if self.overshot_target():
            self.node = self.target
            self.target = self.get_new_target(direction)

            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            if self.target is self.node:
                self.direction = STOP

            self.set_position()
        else:
            if self.is_opposite_direction(direction):
                self.reverse_direction()

    def is_valid_direction(self, direction):
        return direction is not STOP and self.node.neighbors[direction] is not None

    def get_new_target(self, direction):
        return (
            self.node.neighbors[direction]
            if self.is_valid_direction(direction)
            else self.node
        )

    def get_valid_key(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP] or key_pressed[K_w]:
            return UP
        if key_pressed[K_DOWN] or key_pressed[K_s]:
            return DOWN
        if key_pressed[K_LEFT] or key_pressed[K_a]:
            return LEFT
        if key_pressed[K_RIGHT] or key_pressed[K_d]:
            return RIGHT
        return STOP

    def reverse_direction(self):
        self.direction *= -1
        self.node, self.target = self.target, self.node

    def is_opposite_direction(self, direction):
        return direction is not STOP and direction == -self.direction

    def overshot_target(self):
        if self.target:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            return vec2.magnitude_squared() >= vec1.magnitude_squared()
        return False

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.position.as_int(), self.radius)
