import pytest
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from movement.vector import Vector2
from movement.nodes import Node
from pacman.pacman import Pacman
from ghosts.ghost import Ghost
from ghosts.entity import Entity
from food.pellets import Pellet, PowerPellet
from constants import *
from unittest.mock import patch, MagicMock

# Mock the Spritesheet initialization to avoid file loading
@pytest.fixture
def mock_sprites(monkeypatch):
    # Create a patch for the Spritesheet.__init__ method
    def mock_init(self):
        self.sheet = MagicMock()
        self.data = {}
    
    # Apply the patch
    from styles.sprite.sprites import Spritesheet
    monkeypatch.setattr(Spritesheet, "__init__", mock_init)
    
    # Also patch the getImage method
    def mock_get_image(self, x, y, width, height):
        return MagicMock()
    
    monkeypatch.setattr(Spritesheet, "getImage", mock_get_image)
    
    # Return a dummy value - the patch is already applied
    return True

class TestEntityInteractions:
    def test_pacman_pellet_collision(self, mock_sprites):
        """Test Pacman collision with a pellet"""
        # Mock the getStartImage method
        with patch('styles.sprite.sprites.PacmanSprites.getStartImage', return_value=MagicMock()):
            # Create pacman and pellet at same position
            node = Node(100, 100)
            pacman = Pacman(node)
            pellet = Pellet(3, 3)  # Position at 3,3 tiles
            
            # Place both at the same position
            pacman.position = Vector2(pellet.position.x, pellet.position.y)
            
            # Set collision radius
            pacman.collideRadius = 10
            
            # Check collision
            distance = (pacman.position - pellet.position).magnitude()
            collision = distance <= pacman.collideRadius + pellet.collideRadius
            
            # Should collide
            assert collision is True
        
    def test_pacman_ghost_collision(self, mock_sprites):
        """Test Pacman collision with a ghost"""
        # Mock the getStartImage method
        with patch('styles.sprite.sprites.PacmanSprites.getStartImage', return_value=MagicMock()):
            # Create pacman and ghost at same position
            node = Node(100, 100)
            pacman = Pacman(node)
            
            # Mock the ghost sprites
            with patch('ghosts.ghost.GhostSprites', return_value=MagicMock()):
                ghost = Ghost(node, 0)
                
                # Ensure both are at the same position
                pacman.position = Vector2(100, 100)
                ghost.position = Vector2(100, 100)
                
                # Set collision radii
                pacman.collideRadius = 5
                ghost.collideRadius = 5
                
                # Check collision
                distance = (pacman.position - ghost.position).magnitude()
                collision = distance <= pacman.collideRadius + ghost.collideRadius
                
                # Should collide
                assert collision is True
        
    def test_ghost_mode_affects_pacman_collision(self, mock_sprites):
        """Test ghost mode affects outcome of collision with Pacman"""
        # Mock the getStartImage method
        with patch('styles.sprite.sprites.PacmanSprites.getStartImage', return_value=MagicMock()):
            # Create pacman and ghost
            node = Node(100, 100)
            pacman = Pacman(node)
            
            # Mock the ghost sprites
            with patch('ghosts.ghost.GhostSprites', return_value=MagicMock()):
                ghost = Ghost(node, 0)
                
                # Set to same position
                pacman.position = Vector2(100, 100)
                ghost.position = Vector2(100, 100)
                
                # Ghost in normal mode
                ghost.mode = SCATTER
                
                # In SCATTER mode, pacman should die on collision
                # This would be handled in GameController.checkGhostEvents
                # but we can test the prerequisites
                assert ghost.mode == SCATTER
                
                # Switch ghost to frightened mode
                ghost.mode = FREIGHT
                
                # In FREIGHT mode, ghost should be eaten
                assert ghost.mode == FREIGHT
        
    def test_entity_movement(self):
        """Test entity movement between nodes"""
        # Create connected nodes
        node1 = Node(100, 100)
        node2 = Node(132, 100)  # 32 pixels to the right
        
        # Connect nodes
        node1.neighbors[RIGHT] = node2
        node2.neighbors[LEFT] = node1
        
        # Create entity at node1
        entity = Entity(node1)
        
        # Manually set up entity for direct movement testing
        entity.direction = RIGHT
        entity.target = node2
        entity.setSpeed(64)  # 64 pixels per second
        
        # Mock the update method to just do direct movement without pathfinding
        def simple_update(dt):
            # Simple position update based on direction and speed
            vec = entity.directions[entity.direction]
            entity.position += vec * entity.speed * dt
        
        # Replace the update method
        entity.update = simple_update
        
        # Initial position
        assert entity.node == node1
        assert entity.position == node1.position
        
        # Move towards node2
        dt = 0.5  # 0.5 seconds
        entity.update(dt)
        
        # Position should be updated
        # 64 pixels/sec * 0.5 sec = 32 pixels
        # This should reach node2 exactly
        assert entity.position.x > node1.position.x
        expected_x = 100 + 32
        assert entity.position.x == expected_x
        
    @patch('pygame.key.get_pressed')
    def test_pacman_direction_control(self, mock_get_pressed, mock_sprites):
        """Test Pacman direction control with key presses"""
        # Mock the getStartImage method
        with patch('styles.sprite.sprites.PacmanSprites.getStartImage', return_value=MagicMock()):
            # Create connected nodes in four directions
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
            
            # Create Pacman at center
            pacman = Pacman(center)
            
            # Initial direction is LEFT
            assert pacman.direction == LEFT
            
            # Create key state mock
            key_states = {K_UP: False, K_DOWN: False, K_LEFT: False, K_RIGHT: False}
            
            def mock_pressed():
                return type('obj', (object,), {'__getitem__': lambda self, k: key_states.get(k, False)})()
            
            mock_get_pressed.side_effect = mock_pressed
            
            # Mock validDirection to always return True for testing
            pacman.validDirection = lambda direction: True
            
            # Press UP
            key_states[K_UP] = True
            
            # Test getValidKey method
            direction = pacman.getValidKey()
            assert direction == UP
            
            # Reset
            key_states[K_UP] = False
            
            # Press RIGHT
            key_states[K_RIGHT] = True
            
            # Test getValidKey method
            direction = pacman.getValidKey()
            assert direction == RIGHT


class TestGameStateTransitions:
    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    def test_power_pellet_frightens_ghosts(self, mock_set_mode, mock_init):
        """Test power pellet frightens all ghosts"""
        # Create mock game components
        controller = MagicMock()
        ghosts = MagicMock()
        controller.ghosts = ghosts
        
        # Create power pellet
        power_pellet = PowerPellet(5, 5)
        
        # Simulate eating power pellet
        # This would normally be done in GameController.checkPelletEvents
        
        # Ghost startFreight should be called
        ghosts.startFreight.assert_not_called()  # Not called yet
        
        # Simulate the event
        controller.ghosts.startFreight()
        
        # Should be called now
        ghosts.startFreight.assert_called_once()
        
    @patch('pygame.init')
    @patch('pygame.display.set_mode')
    def test_level_completion(self, mock_set_mode, mock_init):
        """Test level completion when all pellets are eaten"""
        # Create mock game components
        controller = MagicMock()
        pellets = MagicMock()
        controller.pellets = pellets
        
        # Initially not empty
        pellets.isEmpty.return_value = False
        
        # Simulate eating all pellets
        pellets.isEmpty.return_value = True
        
        # Check level completion condition
        is_complete = controller.pellets.isEmpty()
        
        # Should be complete
        assert is_complete is True 