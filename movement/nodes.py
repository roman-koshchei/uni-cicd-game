import pygame
from movement.vector import Vector2
from constants import *
import numpy as np

class Node:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}

    def render(self, screen):
        for direction, neighbor in self.neighbors.items():
            if neighbor is not None:
                line_start = self.position.as_tuple()
                line_end = neighbor.position.as_tuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.as_int(), 12)


class NodeGroup:
    def __init__(self, level):
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        self.node_list = []
        self.home_key = None

    def create_home_nodes(self, xoffset, yoffset):
        homedata = np.array([['X','X','+','X','X'],
                             ['X','X','.','X','X'],
                             ['+','X','.','X','+'],
                             ['+','.','+','.','+'],
                             ['+','X','X','X','+']])

        self.createNodeTable(homedata, xoffset, yoffset)
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset+2, yoffset)
        return self.homekey
    
    def connect_home_nodes(self, homekey, otherkey, direction):     
        key = self.constructKey(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey]

    def setup_test_nodes(self):
        node_a = Node(80, 80)
        node_b = Node(160, 80)
        node_c = Node(80, 160)
        node_d = Node(160, 160)
        node_e = Node(208, 160)
        node_f = Node(80, 320)
        node_g = Node(208, 320)

        node_a.neighbors[RIGHT] = node_b
        node_a.neighbors[DOWN] = node_c

        node_b.neighbors[LEFT] = node_a
        node_b.neighbors[DOWN] = node_d

        node_c.neighbors[UP] = node_a
        node_c.neighbors[RIGHT] = node_d
        node_c.neighbors[DOWN] = node_f

        node_d.neighbors[UP] = node_b
        node_d.neighbors[LEFT] = node_c
        node_d.neighbors[RIGHT] = node_e

        node_e.neighbors[LEFT] = node_d
        node_e.neighbors[DOWN] = node_g

        node_f.neighbors[UP] = node_c
        node_f.neighbors[RIGHT] = node_g

        node_g.neighbors[UP] = node_e
        node_g.neighbors[LEFT] = node_f

        self.node_list = [node_a, node_b, node_c, node_d, node_e, node_f, node_g]

    def render(self, screen):
        for node in self.node_list:
            node.render(screen)