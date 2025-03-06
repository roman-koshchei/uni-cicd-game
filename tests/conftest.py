import pytest
import pygame
import numpy as np
import os
import sys

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from movement.vector import Vector2
from movement.nodes import Node, NodeGroup
from pacman.pacman import Pacman
from ghosts.entity import Entity
from ghosts.ghost import Ghost, GhostGroup
from food.pellets import Pellet, PowerPellet, PelletGroup
from constants import *

@pytest.fixture
def vector():
    return Vector2(5, 10)

@pytest.fixture
def node():
    return Node(100, 200)

@pytest.fixture
def connected_nodes():
    """Create a small grid of connected nodes for testing"""
    center = Node(100, 100)
    up = Node(100, 68)
    down = Node(100, 132)
    left = Node(68, 100)
    right = Node(132, 100)
    
    # Connect nodes
    center.neighbors[UP] = up
    center.neighbors[DOWN] = down
    center.neighbors[LEFT] = left
    center.neighbors[RIGHT] = right
    
    up.neighbors[DOWN] = center
    down.neighbors[UP] = center
    left.neighbors[RIGHT] = center
    right.neighbors[LEFT] = center
    
    return {
        'center': center,
        'up': up,
        'down': down,
        'left': left,
        'right': right
    }

@pytest.fixture
def entity(node):
    return Entity(node)

@pytest.fixture
def pacman(node):
    return Pacman(node)

@pytest.fixture
def mock_pellet_data():
    """Create a mock pellet data array for testing"""
    return np.array([
        ['.', '.', 'P'],
        ['.', ' ', ' '],
        ['P', ' ', '.']
    ])

@pytest.fixture
def mock_screen():
    """Create a mock pygame screen for testing rendering"""
    pygame.init()
    return pygame.Surface((800, 600)) 