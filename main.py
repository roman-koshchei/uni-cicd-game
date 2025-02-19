import pygame
from pygame.locals import *
import boards
from constants import *
from pacman.pacman import Pacman
from movement.nodes import NodeGroup
from ghosts.ghost import GhostGroup
from pellets.pellets import PelletGroup
from sprites.sprite_manager import SpriteManager
import copy
from math import pi as PI


class GameController(object):
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.background = None
        self.sprite_manager = SpriteManager()
        self.load_sprites()
        self.level = copy.deepcopy(
            boards.boards
        )  # Create a deep copy of the boards array
        self.flicker = False  # Add flicker state for power pellets
        self.timer = 0  # Timer for power pellet flicker
        self.flicker_speed = 0.2  # Seconds between flicker states

    def load_sprites(self):
        # Load Pacman sprites from GIFs
        sprite_dir = "assets/sprites"

        # Load directional animations for Pacman
        for direction in ["u", "d", "l", "r"]:
            self.sprite_manager.load_direction_animations(sprite_dir, direction)

        # Map the direction letters to the full names for compatibility
        self.sprite_manager.animations["pacman_up"] = (
            self.sprite_manager.animations.get("pacman_u", [])
        )
        self.sprite_manager.animations["pacman_down"] = (
            self.sprite_manager.animations.get("pacman_d", [])
        )
        self.sprite_manager.animations["pacman_left"] = (
            self.sprite_manager.animations.get("pacman_l", [])
        )
        self.sprite_manager.animations["pacman_right"] = (
            self.sprite_manager.animations.get("pacman_r", [])
        )

        # Load Ghost animations
        self.sprite_manager.load_ghost_animations(sprite_dir)

        # Create simple circle sprites for pellets if not found
        pellet_surface = pygame.Surface(
            (TILEWIDTH // 2, TILEWIDTH // 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            pellet_surface,
            YELLOW,
            (TILEWIDTH // 4, TILEWIDTH // 4),
            int(TILEWIDTH * 0.125),
        )
        self.sprite_manager.sprites["pellet"] = pellet_surface

        powerpellet_surface = pygame.Surface((TILEWIDTH, TILEWIDTH), pygame.SRCALPHA)
        pygame.draw.circle(
            powerpellet_surface,
            YELLOW,
            (TILEWIDTH // 2, TILEWIDTH // 2),
            int(TILEWIDTH * 0.35),
        )
        self.sprite_manager.sprites["powerpellet"] = powerpellet_surface

        # Create simple eyes sprite for ghost spawn state if not found
        eyes_surface = pygame.Surface((TILEWIDTH, TILEWIDTH), pygame.SRCALPHA)
        dark_blue = (0, 0, 128)  # Darker blue for better visibility
        # Left eye
        pygame.draw.circle(
            eyes_surface, WHITE, (TILEWIDTH // 4, TILEWIDTH // 2), TILEWIDTH // 4
        )
        pygame.draw.circle(
            eyes_surface, dark_blue, (TILEWIDTH // 4, TILEWIDTH // 2), TILEWIDTH // 8
        )
        # Right eye
        pygame.draw.circle(
            eyes_surface, WHITE, (3 * TILEWIDTH // 4, TILEWIDTH // 2), TILEWIDTH // 4
        )
        pygame.draw.circle(
            eyes_surface,
            dark_blue,
            (3 * TILEWIDTH // 4, TILEWIDTH // 2),
            TILEWIDTH // 8,
        )
        self.sprite_manager.sprites["ghost_eyes"] = eyes_surface

    def set_background(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(MAZE_BLACK)

    def start_game(self):
        self.set_background()
        # Use the board numbers directly
        self.nodes = NodeGroup(self.level)

        # Initialize game objects
        self.pacman = Pacman(self.nodes.start_temp_node(), self.sprite_manager)
        self.pellets = PelletGroup(
            self.level, self.sprite_manager
        )  # Pass the level array directly

        self.ghosts = GhostGroup(self.nodes.start_temp_node(), self.pacman)
        # Set ghost spawn position to middle of ghost house
        self.ghosts.set_spawn_node(self.nodes.node_from_tiles(14, 14))

    def draw_board(self):
        cell_height = TILEHEIGHT
        cell_width = TILEWIDTH

        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                x = j * cell_width
                y = i * cell_height
                center_x = x + (0.5 * cell_width)
                center_y = y + (0.5 * cell_height)

                cell = self.level[i][j]

                # Draw different elements based on the number in the level array
                if cell == 3:  # Vertical wall
                    pygame.draw.line(
                        self.screen,
                        MAZE_BLUE,
                        (center_x, y),
                        (center_x, y + cell_height),
                        3,
                    )
                elif cell == 4:  # Horizontal wall
                    pygame.draw.line(
                        self.screen,
                        MAZE_BLUE,
                        (x, center_y),
                        (x + cell_width, center_y),
                        3,
                    )
                elif cell == 5:  # Top-right corner
                    pygame.draw.arc(
                        self.screen,
                        MAZE_BLUE,
                        [x - (cell_width * 0.4) - 2, center_y, cell_width, cell_height],
                        0,
                        PI / 2,
                        3,
                    )
                elif cell == 6:  # Top-left corner
                    pygame.draw.arc(
                        self.screen,
                        MAZE_BLUE,
                        [x + (cell_width * 0.5), center_y, cell_width, cell_height],
                        PI / 2,
                        PI,
                        3,
                    )
                elif cell == 7:  # Bottom-left corner
                    pygame.draw.arc(
                        self.screen,
                        MAZE_BLUE,
                        [
                            x + (cell_width * 0.5),
                            y - (0.4 * cell_height),
                            cell_width,
                            cell_height,
                        ],
                        PI,
                        3 * PI / 2,
                        3,
                    )
                elif cell == 8:  # Bottom-right corner
                    pygame.draw.arc(
                        self.screen,
                        MAZE_BLUE,
                        [
                            x - (cell_width * 0.4) - 2,
                            y - (0.4 * cell_height),
                            cell_width,
                            cell_height,
                        ],
                        3 * PI / 2,
                        2 * PI,
                        3,
                    )
                elif cell == 9:  # Ghost house door
                    pygame.draw.line(
                        self.screen,
                        "white",
                        (x, center_y),
                        (x + cell_width, center_y),
                        3,
                    )

    def update(self):
        dt = self.clock.tick(30) / 1000.0

        # Update flicker state
        self.timer += dt
        if self.timer >= self.flicker_speed:
            self.flicker = not self.flicker
            self.timer = 0

        self.pacman.update(dt)
        self.pellets.update(dt)
        self.ghosts.update(dt)

        # Pellet events
        pellet = self.pacman.eat_pellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.eaten_count += 1
            self.pellets.pellet_list.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.start_freight()

        # Ghost events
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current is FREIGHT:
                    ghost.start_spawn()

        # Pygame events
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        self.render()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_board()
        # self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
