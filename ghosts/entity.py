import pygame
from pygame.locals import *
from movement.vector import Vector2
from constants import *
from random import randint

class Entity:
    def __init__(self, node):
        self.name = None
        self.directions = {UP:Vector2(0, -1),DOWN:Vector2(0, 1), 
                          LEFT:Vector2(-1, 0), RIGHT:Vector2(1, 0), STOP:Vector2()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.node = node
        self.setPosition()
        self.target = node
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.direction_method = self.random_direction

    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
         
        if self.overshot_target():
            self.node = self.target
            directions = self.valid_directions()
            direction = self.direction_method(directions)
            if not self.disablePortal:
                # todo: implement portal
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            self.set_position()

    def valid_directions(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def random_direction(self, directions):
        return directions[randint(0, len(directions)-1)]

    def set_position(self):
        self.position = self.node.position.copy()
          
    def valid_direction(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def get_new_target(self, direction):
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshot_target(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitude_squared()
            node2Self = vec2.magnitude_squared()
            return node2Self >= node2Target
        return False

    def reverse_direction(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
        
    def opposite_direction(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def set_speed(self, speed):
        self.speed = speed * TILEWIDTH / 16

    def goal_direction(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitude_squared())
        index = distances.index(min(distances))
        return directions[index]

    def render(self, screen):
        if self.visible:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)
