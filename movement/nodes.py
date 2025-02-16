import pygame
import numpy as np
from typing import Dict, Tuple
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
    def __init__(self, level: str):
        self.node_table: Dict[Tuple[int, int], Node] = {}
        self.level = level
        self.node_symbols = ["+"]
        self.path_symbols = ["."]

        data = self.read_maze_file(level)
        self.create_node_table(data)
        self.connect_horizontally(data)
        self.connect_vertically(data)
        
    def connect_home_nodes(self, homekey, otherkey, direction):     
        key = self.constructKey(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey]


    def render(self, screen):
        for node in self.node_table.values():
            node.render(screen)

    def read_maze_file(self, file: str):
        return np.loadtxt(file, dtype="<U1")

    def create_node_table(self, data: np.ndarray, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    x, y = self.create_key(col + xoffset, row + yoffset)
                    self.node_table[(x, y)] = Node(x, y)

    def create_key(self, x: int, y: int):
        return x * TILEWIDTH, y * TILEHEIGHT

    def connect_horizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    if key is None:
                        key = self.create_key(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.create_key(col + xoffset, row + yoffset)
                        self.node_table[key].neighbors[RIGHT] = self.node_table[otherkey]
                        self.node_table[otherkey].neighbors[LEFT] = self.node_table[key]
                        key = otherkey
                elif data[row][col] not in self.path_symbols:
                    key = None

    def connect_vertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.node_symbols:
                    if key is None:
                        key = self.create_key(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.create_key(col + xoffset, row + yoffset)
                        self.node_table[key].neighbors[DOWN] = self.node_table[otherkey]
                        self.node_table[otherkey].neighbors[UP] = self.node_table[key]
                        key = otherkey
                elif dataT[col][row] not in self.path_symbols:
                    key = None

    def node_from_pixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.node_table.keys():
            return self.node_table[(xpixel, ypixel)]
        return None

    def node_from_tiles(self, col: int, row: int):
        x, y = self.create_key(col, row)
        return self.node_table[(x, y)] if (x, y) in self.node_table.keys() else None

    def start_temp_node(self) -> Node:
        return next(iter(self.node_table.values()), None)