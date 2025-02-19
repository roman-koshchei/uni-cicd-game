import numpy as np
from typing import Dict, Tuple
from movement.vector import Vector2
from constants import *
import numpy as np


class Node:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}


class NodeGroup(object):
    def __init__(self, level_data):
        self.node_table: Dict[Tuple[int, int], Node] = {}
        # Numbers that represent walkable paths (dots, power pellets, and empty spaces)
        self.nodeSymbols = [0, 1, 2]
        # Numbers that represent walls and gates
        self.wallSymbols = [3, 4, 5, 6, 7, 8, 9]

        data = np.array(level_data)
        self.create_node_table(data)
        self.connect_horizontally(data)
        self.connect_vertically(data)

    def create_key(self, x: int, y: int):
        # Center the node in the middle of the tile
        return (x * TILEWIDTH + TILEWIDTH // 2), (y * TILEHEIGHT + TILEHEIGHT // 2)

    def create_node_table(self, data: np.ndarray, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.create_key(col + xoffset, row + yoffset)
                    self.node_table[(x, y)] = Node(x, y)

    def connect_horizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:  # If it's a walkable space
                    if key is None:
                        key = self.create_key(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.create_key(col + xoffset, row + yoffset)
                        self.node_table[key].neighbors[RIGHT] = self.node_table[
                            otherkey
                        ]
                        self.node_table[otherkey].neighbors[LEFT] = self.node_table[key]
                        key = otherkey
                elif data[row][col] in self.wallSymbols:  # If it's a wall
                    key = None

    def connect_vertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:  # If it's a walkable space
                    if key is None:
                        key = self.create_key(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.create_key(col + xoffset, row + yoffset)
                        self.node_table[key].neighbors[DOWN] = self.node_table[otherkey]
                        self.node_table[otherkey].neighbors[UP] = self.node_table[key]
                        key = otherkey
                elif dataT[col][row] in self.wallSymbols:  # If it's a wall
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
