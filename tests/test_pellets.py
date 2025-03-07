import pytest
import pygame
import numpy as np
from food.pellets import Pellet, PowerPellet, PelletGroup
from movement.vector import Vector2
from constants import *
from unittest.mock import patch, MagicMock, mock_open


class TestPellet:
    def test_pellet_initialization(self):
        """Test pellet initialization with row and column"""
        row, col = 5, 10
        pellet = Pellet(row, col)

        # Check pellet properties
        assert pellet.name == PELLET
        assert pellet.position.x == col * TILEWIDTH
        assert pellet.position.y == row * TILEHEIGHT
        assert pellet.color == WHITE
        assert pellet.radius == int(2 * TILEWIDTH / 16)
        assert pellet.collideRadius == int(2 * TILEWIDTH / 16)
        assert pellet.points == 10
        assert pellet.visible is True

    def test_pellet_render(self, mock_screen):
        """Test pellet rendering"""
        with patch("pygame.draw.circle") as mock_draw:
            pellet = Pellet(5, 10)
            pellet.render(mock_screen)

            # Verify circle was drawn
            mock_draw.assert_called_once()

            # Test with visible=False
            mock_draw.reset_mock()
            pellet.visible = False
            pellet.render(mock_screen)

            # Should not render when not visible
            mock_draw.assert_not_called()


class TestPowerPellet:
    def test_power_pellet_initialization(self):
        """Test power pellet initialization"""
        row, col = 5, 10
        power_pellet = PowerPellet(row, col)

        # Check power pellet specific properties
        assert power_pellet.name == POWERPELLET
        assert power_pellet.radius == int(8 * TILEWIDTH / 16)
        assert power_pellet.points == 50
        assert power_pellet.flashTime == 0.2
        assert power_pellet.timer == 0

    def test_power_pellet_update(self):
        """Test power pellet flashing behavior"""
        power_pellet = PowerPellet(5, 10)

        # Initially visible
        assert power_pellet.visible is True

        # Update with less than flash time
        power_pellet.update(0.1)
        assert power_pellet.timer == 0.1
        assert power_pellet.visible is True  # Still visible

        # Update again to exceed flash time
        power_pellet.update(0.1)
        assert power_pellet.timer == 0.0  # Timer reset
        assert power_pellet.visible is False  # Toggled to invisible

        # Update once more to toggle back
        power_pellet.update(0.2)
        assert power_pellet.visible is True  # Toggled back to visible


class TestPelletGroup:
    @patch("food.pellets.PelletGroup.readPelletfile")
    def test_pellet_group_initialization(self, mock_read):
        """Test pellet group creation from file data"""
        # Mock the pellet file data
        mock_data = np.array([[".", ".", "P"], [".", " ", " "], ["P", " ", "."]])
        mock_read.return_value = mock_data

        # Create pellet group
        pellet_group = PelletGroup("fake_file.txt")

        # Count the number of pellets created
        regular_pellets = sum(1 for p in pellet_group.pelletList if p.name == PELLET)
        power_pellets = len(pellet_group.powerpellets)

        # Verify pellet counts
        assert regular_pellets == 4  # 4 dots
        assert power_pellets == 2  # 2 power pellets
        assert len(pellet_group.pelletList) == 6  # Total of 6 pellets
        assert pellet_group.numEaten == 0

    def test_pellet_group_is_empty(self):
        """Test isEmpty method"""
        with patch("food.pellets.PelletGroup.readPelletfile") as mock_read:
            mock_read.return_value = np.array([])

            # Create empty pellet group
            pellet_group = PelletGroup("fake_file.txt")

            # Should be empty
            assert pellet_group.isEmpty() is True

            # Add a pellet
            pellet_group.pelletList.append(Pellet(0, 0))

            # Should not be empty anymore
            assert pellet_group.isEmpty() is False

    def test_pellet_group_update(self):
        """Test updating all power pellets in group"""
        with patch("food.pellets.PelletGroup.readPelletfile") as mock_read:
            # Create data with 2 power pellets
            mock_read.return_value = np.array([["P", "P"]])

            # Create pellet group
            pellet_group = PelletGroup("fake_file.txt")

            # Verify we have 2 power pellets
            assert len(pellet_group.powerpellets) == 2

            # All should be initially visible
            for pp in pellet_group.powerpellets:
                assert pp.visible is True

            # Update with enough time to toggle visibility
            pellet_group.update(0.3)

            # All should have toggled to invisible
            for pp in pellet_group.powerpellets:
                assert pp.visible is False

    def test_pellet_group_render(self, mock_screen):
        """Test rendering all pellets in group"""
        with patch("food.pellets.PelletGroup.readPelletfile") as mock_read:
            # Create data with 2 pellets
            mock_read.return_value = np.array([[".", "."]])

            # Create pellet group
            pellet_group = PelletGroup("fake_file.txt")

            # Mock the pellet render method
            with patch.object(Pellet, "render") as mock_render:
                # Render pellet group
                pellet_group.render(mock_screen)

                # Each pellet's render should be called
                assert mock_render.call_count == 2
