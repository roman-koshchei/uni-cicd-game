import pytest
from ghosts.entity import Entity
from movement.vector import Vector2
from movement.nodes import Node
from constants import *
import pygame

class TestEntity:
    def test_entity_initialization(self, node):
        """Test entity initialization with a node"""
        entity = Entity(node)
        assert entity.name is None
        assert entity.direction == STOP
        assert entity.node == node
        assert entity.target == node
        assert entity.visible is True
        assert entity.disablePortal is False
        assert entity.collideRadius == 5

    def test_entity_set_start_node(self, node):
        """Test setting the start node for an entity"""
        # Create a mock node to use as initial
        initial_node = Node(50, 50)
        entity = Entity(initial_node)
        
        # Change to a new node
        entity.setStartNode(node)
        assert entity.node == node
        assert entity.startNode == node
        assert entity.target == node
        
        # Position should match node position
        assert hasattr(entity, 'position')
        assert entity.position == node.position

    def test_entity_reset(self, node):
        """Test resetting an entity to initial state"""
        entity = Entity(node)
        
        # Change some properties
        entity.direction = LEFT
        entity.speed = 200
        entity.visible = False
        
        # Reset entity
        entity.reset()
        
        # Verify reset values
        assert entity.direction == STOP
        assert entity.speed == 100
        assert entity.visible is True

    def test_entity_set_position(self, node):
        """Test setting entity position to match node position"""
        entity = Entity(node)
        # Initially position is not defined
        if hasattr(entity, 'position'):
            initial_pos = entity.position.copy()
            
        # Change node position
        node.position = Vector2(300, 400)
        
        # Set entity position
        entity.setPosition()
        
        # Verify position matches node position
        assert entity.position.x == 300
        assert entity.position.y == 400

    def test_entity_set_between_nodes(self, connected_nodes):
        """Test positioning an entity between two nodes"""
        entity = Entity(connected_nodes['center'])
        
        # Set entity between center and right nodes
        entity.setBetweenNodes(RIGHT)
        
        # Position should be midpoint between center and right
        expected_x = (connected_nodes['center'].position.x + connected_nodes['right'].position.x) / 2
        expected_y = (connected_nodes['center'].position.y + connected_nodes['right'].position.y) / 2
        
        assert entity.position.x == expected_x
        assert entity.position.y == expected_y
        assert entity.target == connected_nodes['right']

    def test_entity_set_speed(self):
        """Test setting entity speed"""
        # Create a node to avoid None issues
        node = Node(100, 100)
        entity = Entity(node)
        
        # Set speed to 200
        entity.setSpeed(200)
        assert entity.speed == 200
        
        # Set speed to 0
        entity.setSpeed(0)
        assert entity.speed == 0

    @pytest.mark.parametrize("direction,expected", [
        (UP, Vector2(0, -1)),
        (DOWN, Vector2(0, 1)),
        (LEFT, Vector2(-1, 0)),
        (RIGHT, Vector2(1, 0)),
        (STOP, Vector2(0, 0))
    ])
    def test_entity_directions(self, direction, expected, node):
        """Test entity direction vectors"""
        entity = Entity(node)
        assert entity.directions[direction] == expected 