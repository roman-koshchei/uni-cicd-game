import unittest
import os
import sys
import pytest
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from pacman.pacman import Pacman
from movement.vector import Vector2
from constants import *
from unittest.mock import patch, MagicMock

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock classes for legacy tests
class PacmanMock:
    def __init__(self, x=5, y=5):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == "right":
            self.x += 1
        elif direction == "left":
            self.x -= 1
        elif direction == "up":
            self.y -= 1
        elif direction == "down":
            self.y += 1

class Maze:
    def __init__(self):
        self.width = 10
        self.height = 10
        # Стіни на координатах (3,3), (3,4), (3,5)
        self.walls = [(3, 3), (3, 4), (3, 5)]

    def is_wall(self, x, y):
        return (x, y) in self.walls

    def is_valid_move(self, x, y):
        return (
            0 <= x < self.width and 0 <= y < self.height and not self.is_wall(x, y)
        )

# Legacy unittest-based tests
class TestPacmanLegacy(unittest.TestCase):
    def setUp(self):
        self.maze = Maze()
        self.pacman = PacmanMock(x=5, y=5)

    def test_pacman_initial_position(self):
        """Тест перевіряє початкову позицію Pacman"""
        self.assertEqual(self.pacman.x, 5)
        self.assertEqual(self.pacman.y, 5)

    def test_pacman_movement(self):
        """Тест перевіряє рух Pacman у різних напрямках"""
        # Рух вправо
        self.pacman.move("right")
        self.assertEqual(self.pacman.x, 6)
        self.assertEqual(self.pacman.y, 5)

        # Рух вниз
        self.pacman.move("down")
        self.assertEqual(self.pacman.x, 6)
        self.assertEqual(self.pacman.y, 6)

        # Рух вліво
        self.pacman.move("left")
        self.assertEqual(self.pacman.x, 5)
        self.assertEqual(self.pacman.y, 6)

        # Рух вгору
        self.pacman.move("up")
        self.assertEqual(self.pacman.x, 5)
        self.assertEqual(self.pacman.y, 5)

    def test_wall_detection(self):
        """Тест перевіряє, чи стіни блокують рух"""
        # Перевіряємо, що у стіни в лабіринті дійсно існують
        self.assertTrue(self.maze.is_wall(3, 3))
        self.assertTrue(self.maze.is_wall(3, 4))
        self.assertTrue(self.maze.is_wall(3, 5))

        # Перевіряємо, що це дійсно блокує рух
        self.assertFalse(self.maze.is_valid_move(3, 3))
        self.assertTrue(self.maze.is_valid_move(5, 5))

# Pytest-based tests for the actual Pacman class
@pytest.fixture
def mock_pacman_sprites(monkeypatch):
    """Mock the PacmanSprites class to avoid loading images"""
    from styles.sprite.sprites import PacmanSprites
    
    def mock_init(self, entity):
        self.entity = entity
        self.sprites = {}
    
    monkeypatch.setattr(PacmanSprites, "__init__", mock_init)
    
    def mock_update(self, dt):
        pass
    
    monkeypatch.setattr(PacmanSprites, "update", mock_update)
    
    def mock_get_start_image(self):
        return MagicMock()
    
    monkeypatch.setattr(PacmanSprites, "getStartImage", mock_get_start_image)
    
    def mock_reset(self):
        pass
    
    monkeypatch.setattr(PacmanSprites, "reset", mock_reset)
    
    return True

class TestPacman:
    def test_pacman_initialization(self, node, mock_pacman_sprites):
        """Test Pacman initialization with a node"""
        # Mock the sprites
        with patch('styles.sprite.sprites.PacmanSprites', return_value=MagicMock()) as mock_sprites:
            pacman = Pacman(node)
            pacman.sprites = mock_sprites.return_value
            
            # Check Pacman specific properties
            assert pacman.name == PACMAN
            assert pacman.direction == LEFT  # Initial direction
            assert pacman.alive is True
            assert pacman.radius == 10
            assert pacman.collideRadius == 5
            assert pacman.color == YELLOW

    def test_pacman_reset(self, node, mock_pacman_sprites):
        """Test resetting Pacman to initial state"""
        # Mock the sprites
        with patch('styles.sprite.sprites.PacmanSprites', return_value=MagicMock()) as mock_sprites:
            pacman = Pacman(node)
            pacman.sprites = mock_sprites.return_value
            
            # Change some properties
            pacman.direction = RIGHT
            pacman.alive = False
            
            # Reset Pacman
            pacman.reset()
            
            # Verify reset values
            assert pacman.direction == LEFT
            assert pacman.alive is True

    def test_pacman_die(self, node, mock_pacman_sprites):
        """Test Pacman death functionality"""
        # Mock the sprites
        with patch('styles.sprite.sprites.PacmanSprites', return_value=MagicMock()) as mock_sprites:
            pacman = Pacman(node)
            pacman.sprites = mock_sprites.return_value
            
            # Initially alive
            assert pacman.alive is True
            
            # Kill Pacman
            pacman.die()
            
            # Should be dead and stopped
            assert pacman.alive is False
            assert pacman.direction == STOP

    @patch('styles.sprite.sprites.PacmanSprites')
    def test_pacman_update(self, MockPacmanSprites, node, mock_pacman_sprites):
        """Test Pacman update method"""
        # Setup mock
        mock_sprites = MockPacmanSprites.return_value
        
        # Create Pacman with mock sprites
        pacman = Pacman(node)
        pacman.sprites = mock_sprites
        
        # Mock the getValidKey method to avoid pygame.key.get_pressed()
        pacman.getValidKey = MagicMock(return_value=STOP)
        
        # Call update with time delta
        dt = 0.1
        pacman.update(dt)
        
        # Verify sprites update was called
        mock_sprites.update.assert_called_once_with(dt)
        
    def test_pacman_valid_directions(self, connected_nodes, mock_pacman_sprites):
        """Test Pacman's valid direction checks"""
        # Mock the sprites
        with patch('styles.sprite.sprites.PacmanSprites', return_value=MagicMock()) as mock_sprites:
            # Create Pacman at center node
            pacman = Pacman(connected_nodes['center'])
            pacman.sprites = mock_sprites.return_value
            
            # All directions should be valid from center
            assert pacman.validDirection(UP)
            assert pacman.validDirection(DOWN)
            assert pacman.validDirection(LEFT)
            assert pacman.validDirection(RIGHT)
            
            # Move to left node where only RIGHT is valid
            pacman.node = connected_nodes['left']
            pacman.target = connected_nodes['left']
            
            # Only RIGHT should be valid from left node
            assert not pacman.validDirection(UP)
            assert not pacman.validDirection(DOWN)
            assert not pacman.validDirection(LEFT)
            assert pacman.validDirection(RIGHT)
        
    @patch('pygame.key.get_pressed')
    def test_pacman_key_pressed_handler(self, mock_get_pressed, connected_nodes, mock_pacman_sprites):
        """Test Pacman's key press handling"""
        # Mock the sprites
        with patch('styles.sprite.sprites.PacmanSprites', return_value=MagicMock()) as mock_sprites:
            # Create Pacman at center node
            pacman = Pacman(connected_nodes['center'])
            pacman.sprites = mock_sprites.return_value
            
            # Initial direction is LEFT
            assert pacman.direction == LEFT
            
            # Create key state mock
            key_states = {K_UP: False, K_DOWN: False, K_LEFT: False, K_RIGHT: False}
            
            def mock_pressed():
                return type('obj', (object,), {'__getitem__': lambda self, k: key_states.get(k, False)})()
            
            mock_get_pressed.side_effect = mock_pressed
            
            # Mock validDirection to always return True for testing
            pacman.validDirection = lambda direction: True
            
            # Test getValidKey method
            
            # Press UP
            key_states[K_UP] = True
            direction = pacman.getValidKey()
            assert direction == UP
            
            # Reset
            key_states[K_UP] = False
            
            # Press RIGHT
            key_states[K_RIGHT] = True
            direction = pacman.getValidKey()
            assert direction == RIGHT

if __name__ == "__main__":
    unittest.main()
