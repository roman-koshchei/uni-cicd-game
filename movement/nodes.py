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
                # Calculate the wall thickness and path width
                wall_thickness = max(2, int(TILEWIDTH / 8))  # Thicker walls
                path_width = int(TILEWIDTH / 2)  # Wide path
                wall_offset = int(TILEWIDTH / 2.5)  # Offset for walls
                
                # Get start and end positions
                start_pos = self.position.as_tuple()
                end_pos = neighbor.position.as_tuple()
                
                # Draw the path (black)
                pygame.draw.line(screen, MAZE_BLACK, start_pos, end_pos, path_width)
                
                # Draw the walls (blue)
                if direction in [LEFT, RIGHT]:
                    # Horizontal walls
                    pygame.draw.line(screen, MAZE_BLUE, 
                                   (start_pos[0], start_pos[1] - wall_offset),
                                   (end_pos[0], end_pos[1] - wall_offset), wall_thickness)
                    pygame.draw.line(screen, MAZE_BLUE,
                                   (start_pos[0], start_pos[1] + wall_offset),
                                   (end_pos[0], end_pos[1] + wall_offset), wall_thickness)
                else:
                    # Vertical walls
                    pygame.draw.line(screen, MAZE_BLUE,
                                   (start_pos[0] - wall_offset, start_pos[1]),
                                   (end_pos[0] - wall_offset, end_pos[1]), wall_thickness)
                    pygame.draw.line(screen, MAZE_BLUE,
                                   (start_pos[0] + wall_offset, start_pos[1]),
                                   (end_pos[0] + wall_offset, end_pos[1]), wall_thickness)


class NodeGroup(object):
    def __init__(self, level: str):
        self.node_table: Dict[Tuple[int, int], Node] = {}
        self.level = level
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        data = self.read_maze_file(level)
        self.create_node_table(data)
        self.connect_horizontally(data)
        self.connect_vertically(data)
        self.homekey = None

    def create_home_nodes(self, xoffset, yoffset):
        homedata = np.array([['X','X','+','X','X'],
                             ['X','X','.','X','X'],
                             ['+','X','.','X','+'],
                             ['+','.','+','.','+'],
                             ['+','X','X','X','+']])

        self.create_node_table(homedata, xoffset, yoffset)
        self.connect_horizontally(homedata, xoffset, yoffset)
        self.connect_vertically(homedata, xoffset, yoffset)
        self.homekey = self.construct_key(xoffset+2, yoffset)
        return self.homekey
    
    def construct_key(self, x, y):
        return x * TILEWIDTH, y * TILEHEIGHT

    def connect_home_nodes(self, homekey, otherkey, direction):     
        key = self.construct_key(*otherkey)
        self.node_table[homekey].neighbors[direction] = self.node_table[key]
        self.node_table[key].neighbors[direction*-1] = self.node_table[homekey]

    def render(self, screen):
        # First draw all paths
        for node in self.node_table.values():
            node.render(screen)

    def read_maze_file(self, file: str):
        return np.loadtxt(file, dtype="<U1")

    def create_node_table(self, data: np.ndarray, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.create_key(col + xoffset, row + yoffset)
                    self.node_table[(x, y)] = Node(x, y)

    def create_key(self, x: int, y: int):
        return x * TILEWIDTH, y * TILEHEIGHT

    def connect_horizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.create_key(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.create_key(col + xoffset, row + yoffset)
                        self.node_table[key].neighbors[RIGHT] = self.node_table[otherkey]
                        self.node_table[otherkey].neighbors[LEFT] = self.node_table[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connect_vertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.create_key(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.create_key(col + xoffset, row + yoffset)
                        self.node_table[key].neighbors[DOWN] = self.node_table[otherkey]
                        self.node_table[otherkey].neighbors[UP] = self.node_table[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
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