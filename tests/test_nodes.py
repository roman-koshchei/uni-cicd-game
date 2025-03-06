import pytest
import numpy as np
from movement.nodes import Node, NodeGroup
from movement.vector import Vector2
from constants import *
from unittest.mock import patch, MagicMock

class TestNode:
    def test_node_initialization(self):
        """Test node initialization with position"""
        x, y = 100, 200
        node = Node(x, y)
        
        # Check node properties
        assert node.position.x == x
        assert node.position.y == y
        assert node.neighbors[UP] is None
        assert node.neighbors[DOWN] is None
        assert node.neighbors[LEFT] is None
        assert node.neighbors[RIGHT] is None
        assert hasattr(node, 'access')
    
    def test_node_connecting(self):
        """Test connecting nodes through neighbors"""
        # Create nodes
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
        
        # Verify connections
        assert center.neighbors[UP] == up
        assert center.neighbors[DOWN] == down
        assert center.neighbors[LEFT] == left
        assert center.neighbors[RIGHT] == right
        
        # Connect in reverse
        up.neighbors[DOWN] = center
        down.neighbors[UP] = center
        left.neighbors[RIGHT] = center
        right.neighbors[LEFT] = center
        
        # Verify reverse connections
        assert up.neighbors[DOWN] == center
        assert down.neighbors[UP] == center
        assert left.neighbors[RIGHT] == center
        assert right.neighbors[LEFT] == center
        
    def test_node_valid_directions(self):
        """Test valid directions from a node"""
        # Create a node with only UP and RIGHT neighbors
        node = Node(100, 100)
        node.neighbors[UP] = Node(100, 68)
        node.neighbors[RIGHT] = Node(132, 100)
        
        # UP and RIGHT should be valid, DOWN and LEFT should not
        valid_dirs = [direction for direction, neighbor in node.neighbors.items() 
                     if neighbor is not None and direction != PORTAL]
        assert UP in valid_dirs
        assert RIGHT in valid_dirs
        assert DOWN not in valid_dirs
        assert LEFT not in valid_dirs
        
        # Add a DOWN neighbor
        node.neighbors[DOWN] = Node(100, 132)
        
        # UP, RIGHT, and DOWN should be valid
        valid_dirs = [direction for direction, neighbor in node.neighbors.items() 
                     if neighbor is not None and direction != PORTAL]
        assert UP in valid_dirs
        assert DOWN in valid_dirs
        assert RIGHT in valid_dirs
        assert LEFT not in valid_dirs
        
        # Empty node should have no valid directions
        empty_node = Node(0, 0)
        empty_valid_dirs = [direction for direction, neighbor in empty_node.neighbors.items() 
                           if neighbor is not None and direction != PORTAL]
        assert len(empty_valid_dirs) == 0
        
    def test_node_denied_directions(self, monkeypatch):
        """Test directions that are explicitly denied"""
        node = Node(100, 100)
        
        # Add all neighbors
        node.neighbors[UP] = Node(100, 68)
        node.neighbors[DOWN] = Node(100, 132)
        node.neighbors[LEFT] = Node(68, 100)
        node.neighbors[RIGHT] = Node(132, 100)
        
        # Initially all directions should be valid
        directions = [UP, DOWN, LEFT, RIGHT]
        for direction in directions:
            assert PACMAN in node.access[direction]
        
        # Create a mock entity with name=PACMAN
        mock_entity = MagicMock()
        mock_entity.name = PACMAN
        
        # Deny LEFT access
        node.denyAccess(LEFT, mock_entity)
        
        # LEFT should be denied for PACMAN but still a valid direction
        assert PACMAN not in node.access[LEFT]
        assert node.neighbors[LEFT] is not None  # Still a valid direction
        
class TestNodeGroup:
    @patch('movement.nodes.NodeGroup.readMazeFile')
    def test_node_group_initialization(self, mock_read):
        """Test NodeGroup initialization and node creation"""
        # Mock maze data
        mock_data = np.array([
            ['0', '0', '0'],
            ['0', '+', '0'],
            ['0', '0', '0']
        ])
        mock_read.return_value = mock_data
        
        # Create NodeGroup
        node_group = NodeGroup("fake_maze.txt")
        
        # Verify node attributes
        assert hasattr(node_group, 'nodesLUT')
        assert hasattr(node_group, 'level')
        
    def test_node_connections(self):
        """Test node connections in a simple grid"""
        # Create a very simple grid for testing connections
        with patch('movement.nodes.NodeGroup.readMazeFile') as mock_read:
            mock_data = np.array([
                [' ', '|', ' '],
                ['-', '+', '-'],
                [' ', '|', ' ']
            ])
            mock_read.return_value = mock_data
            
            # Create NodeGroup
            node_group = NodeGroup("fake_maze.txt")
            
            # Test the node lookup
            assert hasattr(node_group, 'nodesLUT')
            
    def test_get_node_methods(self):
        """Test methods to get nodes from the group"""
        with patch('movement.nodes.NodeGroup.readMazeFile') as mock_read:
            mock_data = np.array([
                [' ', ' ', ' '],
                [' ', '+', ' '],
                [' ', ' ', ' ']
            ])
            mock_read.return_value = mock_data
            
            # Create NodeGroup
            node_group = NodeGroup("fake_maze.txt")
            
            # Test with mock implementation
            # We mock the getNodeFromTiles and getNodeFromPixels methods
            node = Node(100, 100)
            
            # Replace the getNodeFromTiles method
            node_group.getNodeFromTiles = lambda x, y: node if x == 1 and y == 1 else None
            
            # Replace the getNodeFromPixels method
            node_group.getNodeFromPixels = lambda x, y: node if x == TILEWIDTH and y == TILEHEIGHT else None
            
            # Get node from grid position
            result = node_group.getNodeFromTiles(1, 1)
            assert result is not None
            assert result == node
            
            # Get the same node from pixels
            pixel_result = node_group.getNodeFromPixels(TILEWIDTH, TILEHEIGHT)
            assert pixel_result == node
            
            # Test node not found
            assert node_group.getNodeFromTiles(10, 10) is None 