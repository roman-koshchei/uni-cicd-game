import unittest
from unittest.mock import Mock


class TestPacmanMovement(unittest.TestCase):
    def setUp(self):
        # Це заглушки, які потрібно замінити на реальний код
        self.maze = Mock()
        self.maze.is_valid_position = lambda x, y: 0 <= x < 10 and 0 <= y < 10

        # Початкова позиція Pacman
        self.pacman_x = 5
        self.pacman_y = 5

    def test_pacman_can_move_in_valid_directions(self):
        """Тест перевіряє, що Pacman може рухатися у валідних напрямках"""
        # Рух вправо
        new_x, new_y = self.pacman_x + 1, self.pacman_y
        self.assertTrue(self.maze.is_valid_position(new_x, new_y))

        # Рух вліво
        new_x, new_y = self.pacman_x - 1, self.pacman_y
        self.assertTrue(self.maze.is_valid_position(new_x, new_y))

        # Рух вгору
        new_x, new_y = self.pacman_x, self.pacman_y - 1
        self.assertTrue(self.maze.is_valid_position(new_x, new_y))

        # Рух вниз
        new_x, new_y = self.pacman_x, self.pacman_y + 1
        self.assertTrue(self.maze.is_valid_position(new_x, new_y))

    def test_pacman_cannot_move_through_walls(self):
        """Тест перевіряє, що Pacman не може рухатися крізь стіни"""
        # Мокуємо стіну у певній позиції
        self.maze.is_valid_position = lambda x, y: not (x == 6 and y == 5)

        # Спроба руху вправо (там стіна)
        new_x, new_y = self.pacman_x + 1, self.pacman_y
        self.assertFalse(self.maze.is_valid_position(new_x, new_y))


if __name__ == "__main__":
    unittest.main()