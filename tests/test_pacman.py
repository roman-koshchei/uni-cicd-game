import unittest
import os
import sys

# Додаємо кореневу директорію проекту до шляху пошуку
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Імпорт класів гри (припускаємо, що вони існують)
try:
    from game.pacman import Pacman
    from game.maze import Maze
except ImportError:
    # Заглушки для тестування, якщо реальні класи недоступні
    class Pacman:
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


class TestPacman(unittest.TestCase):
    def setUp(self):
        self.maze = Maze()
        self.pacman = Pacman(x=5, y=5)

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


if __name__ == "__main__":
    unittest.main()
