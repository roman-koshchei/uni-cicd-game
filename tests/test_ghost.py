import pytest
from ghosts.ghost import Ghost, GhostGroup, Blinky, Pinky, Inky, Clyde
from ghosts.entity import Entity
from movement.vector import Vector2
from movement.nodes import Node
from constants import *
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_ghost_sprites(monkeypatch):
    """Mock the GhostSprites class to avoid loading images"""
    from styles.sprite.sprites import GhostSprites

    def mock_init(self, entity):
        self.entity = entity
        self.sprites = {}

    monkeypatch.setattr(GhostSprites, "__init__", mock_init)

    def mock_update(self, dt):
        pass

    monkeypatch.setattr(GhostSprites, "update", mock_update)

    return True


class TestGhost:
    def test_ghost_initialization(self, node, mock_ghost_sprites):
        """Test Ghost initialization with a node"""
        # Mock the sprites
        with patch(
            "styles.sprite.sprites.GhostSprites", return_value=MagicMock()
        ) as mock_sprites:
            ghost = Ghost(node, 0)  # Pass index 0 for first ghost
            ghost.sprites = mock_sprites.return_value

            # Check Ghost inherits from Entity
            assert isinstance(ghost, Entity)

            # Check Ghost specific properties
            assert ghost.name == GHOST
            assert ghost.points == 200
            assert ghost.goal is not None

            # Check mode controller
            assert hasattr(ghost, "mode")
            assert ghost.mode.current in [SCATTER, CHASE]

    def test_ghost_reset(self, node, mock_ghost_sprites):
        """Test resetting Ghost to initial state"""
        # Mock the sprites
        with patch(
            "styles.sprite.sprites.GhostSprites", return_value=MagicMock()
        ) as mock_sprites:
            ghost = Ghost(node, 0)
            ghost.sprites = mock_sprites.return_value

            # Change some properties
            ghost.visible = False

            # Reset ghost
            ghost.reset()

            # Verify reset values
            assert ghost.visible is True
            assert ghost.points == 200

    def test_ghost_update(self, node, monkeypatch, mock_ghost_sprites):
        """Test ghost update method with mocked movement"""
        # Mock the sprites
        with patch(
            "styles.sprite.sprites.GhostSprites", return_value=MagicMock()
        ) as mock_sprites:
            ghost = Ghost(node, 0)
            ghost.sprites = mock_sprites.return_value

            # Mock the mode controller
            mock_mode = MagicMock()
            mock_mode.current = SCATTER
            ghost.mode = mock_mode

            # Mock the scatter method
            ghost.scatter = MagicMock()

            # Mock the Entity update method
            original_update = Entity.update
            entity_update_called = False

            def mock_entity_update(self, dt):
                nonlocal entity_update_called
                entity_update_called = True

            # Apply the mock
            monkeypatch.setattr(Entity, "update", mock_entity_update)

            # Call ghost update
            ghost.update(0.1)

            # Verify methods were called
            mock_mode.update.assert_called_once_with(0.1)
            ghost.scatter.assert_called_once()
            assert entity_update_called is True

            # Restore original method
            monkeypatch.setattr(Entity, "update", original_update)

    def test_ghost_mode_transitions(self, node, mock_ghost_sprites):
        """Test ghost mode transitions between SCATTER and CHASE"""
        # Mock the sprites
        with patch(
            "styles.sprite.sprites.GhostSprites", return_value=MagicMock()
        ) as mock_sprites:
            ghost = Ghost(node, 0)
            ghost.sprites = mock_sprites.return_value

            # Mock the mode controller
            mock_mode = MagicMock()
            mock_mode.current = SCATTER
            ghost.mode = mock_mode

            # Test freight mode
            ghost.startFreight()

            # Verify mode controller was called
            mock_mode.setFreightMode.assert_called_once()

            # Test normal mode
            ghost.normalMode()

            # Verify speed was set back to normal
            assert ghost.speed == 100

    def test_ghost_freight_mode(self, node, mock_ghost_sprites):
        """Test ghost frightened state when power pellet is eaten"""
        # Mock the sprites
        with patch(
            "styles.sprite.sprites.GhostSprites", return_value=MagicMock()
        ) as mock_sprites:
            ghost = Ghost(node, 0)
            ghost.sprites = mock_sprites.return_value

            # Mock the mode controller
            mock_mode = MagicMock()
            mock_mode.current = SCATTER
            ghost.mode = mock_mode

            # Initial speed
            initial_speed = ghost.speed

            # Set to frightened mode
            ghost.startFreight()

            # Verify the freight mode was set
            mock_mode.setFreightMode.assert_called_once()

            # Test normal mode
            ghost.normalMode()

            # Verify speed was set back to normal
            assert ghost.speed == 100


class TestGhostGroup:
    @patch("ghosts.ghost.Blinky")
    @patch("ghosts.ghost.Pinky")
    @patch("ghosts.ghost.Inky")
    @patch("ghosts.ghost.Clyde")
    def test_ghost_group_initialization(
        self, MockClyde, MockInky, MockPinky, MockBlinky, node
    ):
        """Test GhostGroup initialization and ghost creation"""
        # Setup mock instances
        mock_blinky = MagicMock()
        mock_pinky = MagicMock()
        mock_inky = MagicMock()
        mock_clyde = MagicMock()

        MockBlinky.return_value = mock_blinky
        MockPinky.return_value = mock_pinky
        MockInky.return_value = mock_inky
        MockClyde.return_value = mock_clyde

        # Create GhostGroup with mocked pacman
        mock_pacman = MagicMock()
        ghost_group = GhostGroup(node, mock_pacman)

        # Verify ghosts are created
        assert len(ghost_group.ghosts) == 4
        assert MockBlinky.call_count == 1
        assert MockPinky.call_count == 1
        assert MockInky.call_count == 1
        assert MockClyde.call_count == 1

    @patch("ghosts.ghost.Blinky")
    @patch("ghosts.ghost.Pinky")
    @patch("ghosts.ghost.Inky")
    @patch("ghosts.ghost.Clyde")
    def test_ghost_group_update(self, MockClyde, MockInky, MockPinky, MockBlinky, node):
        """Test updating all ghosts in the group"""
        # Setup mock instances
        mock_blinky = MagicMock()
        mock_pinky = MagicMock()
        mock_inky = MagicMock()
        mock_clyde = MagicMock()

        MockBlinky.return_value = mock_blinky
        MockPinky.return_value = mock_pinky
        MockInky.return_value = mock_inky
        MockClyde.return_value = mock_clyde

        # Create GhostGroup with mocked pacman
        mock_pacman = MagicMock()
        ghost_group = GhostGroup(node, mock_pacman)

        # Update the group
        ghost_group.update(0.1)

        # Verify each ghost's update was called
        mock_blinky.update.assert_called_once_with(0.1)
        mock_pinky.update.assert_called_once_with(0.1)
        mock_inky.update.assert_called_once_with(0.1)
        mock_clyde.update.assert_called_once_with(0.1)

    @patch("ghosts.ghost.Blinky")
    @patch("ghosts.ghost.Pinky")
    @patch("ghosts.ghost.Inky")
    @patch("ghosts.ghost.Clyde")
    def test_ghost_group_start_freight(
        self, MockClyde, MockInky, MockPinky, MockBlinky, node
    ):
        """Test starting frightened mode for all ghosts"""
        # Setup mock instances
        mock_blinky = MagicMock()
        mock_pinky = MagicMock()
        mock_inky = MagicMock()
        mock_clyde = MagicMock()

        MockBlinky.return_value = mock_blinky
        MockPinky.return_value = mock_pinky
        MockInky.return_value = mock_inky
        MockClyde.return_value = mock_clyde

        # Create GhostGroup with mocked pacman
        mock_pacman = MagicMock()
        ghost_group = GhostGroup(node, mock_pacman)

        # Start freight mode
        ghost_group.startFreight()

        # Verify each ghost's startFreight was called
        mock_blinky.startFreight.assert_called_once()
        mock_pinky.startFreight.assert_called_once()
        mock_inky.startFreight.assert_called_once()
        mock_clyde.startFreight.assert_called_once()

    @patch("ghosts.ghost.Blinky")
    @patch("ghosts.ghost.Pinky")
    @patch("ghosts.ghost.Inky")
    @patch("ghosts.ghost.Clyde")
    def test_ghost_group_reset(self, MockClyde, MockInky, MockPinky, MockBlinky, node):
        """Test resetting all ghosts in the group"""
        # Setup mock instances
        mock_blinky = MagicMock()
        mock_pinky = MagicMock()
        mock_inky = MagicMock()
        mock_clyde = MagicMock()

        MockBlinky.return_value = mock_blinky
        MockPinky.return_value = mock_pinky
        MockInky.return_value = mock_inky
        MockClyde.return_value = mock_clyde

        # Create GhostGroup with mocked pacman
        mock_pacman = MagicMock()
        ghost_group = GhostGroup(node, mock_pacman)

        # Reset the group
        ghost_group.reset()

        # Verify each ghost's reset was called
        mock_blinky.reset.assert_called_once()
        mock_pinky.reset.assert_called_once()
        mock_inky.reset.assert_called_once()
        mock_clyde.reset.assert_called_once()
