import pygame
from pygame.locals import *
from constants import *
from pacman.pacman import Pacman
from movement.nodes import NodeGroup
from ghosts.ghost import Ghost
from pellets.pellets import PelletGroup
from sprites.sprite_manager import SpriteManager

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.background = None
        self.sprite_manager = SpriteManager()
        self.load_sprites()

    def load_sprites(self):
        # Load Pacman sprites from GIFs
        sprite_dir = "assets/sprites"
        
        # Load directional animations for Pacman
        for direction in ["u", "d", "l", "r"]:
            self.sprite_manager.load_direction_animations(sprite_dir, direction)
            
        # Map the direction letters to the full names for compatibility
        self.sprite_manager.animations["pacman_up"] = self.sprite_manager.animations.get("pacman_u", [])
        self.sprite_manager.animations["pacman_down"] = self.sprite_manager.animations.get("pacman_d", [])
        self.sprite_manager.animations["pacman_left"] = self.sprite_manager.animations.get("pacman_l", [])
        self.sprite_manager.animations["pacman_right"] = self.sprite_manager.animations.get("pacman_r", [])
        
        # Load Ghost animations
        self.sprite_manager.load_ghost_animations(sprite_dir)
        
        # Create simple circle sprites for pellets if not found
        pellet_surface = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(pellet_surface, YELLOW, (4, 4), 2)
        self.sprite_manager.sprites["pellet"] = pellet_surface
        
        powerpellet_surface = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(powerpellet_surface, YELLOW, (8, 8), 6)
        self.sprite_manager.sprites["powerpellet"] = powerpellet_surface
        
        # Create simple eyes sprite for ghost spawn state if not found
        eyes_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        dark_blue = (0, 0, 128)  # Darker blue for better visibility
        # Left eye
        pygame.draw.circle(eyes_surface, WHITE, (8, 16), 4)
        pygame.draw.circle(eyes_surface, dark_blue, (8, 16), 2)
        # Right eye
        pygame.draw.circle(eyes_surface, WHITE, (24, 16), 4)
        pygame.draw.circle(eyes_surface, dark_blue, (24, 16), 2)
        self.sprite_manager.sprites["ghost_eyes"] = eyes_surface

    def set_background(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(MAZE_BLACK)  # Using MAZE_BLACK for consistency

    def start_game(self):
        self.set_background()    
        self.nodes = NodeGroup("maze1.txt")
        homekey = self.nodes.create_home_nodes(11.5, 14)
        self.nodes.connect_home_nodes(homekey, (12,14), LEFT)
        self.nodes.connect_home_nodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.start_temp_node(), self.sprite_manager)
        self.pellets = PelletGroup("maze1.txt", self.sprite_manager)
        self.ghost = Ghost(self.nodes.start_temp_node(), self.pacman, self.sprite_manager, "red")
        self.ghost.set_spawn_node(self.nodes.node_from_tiles(2+11.5, 3+14))

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.pellets.update(dt)
        self.ghost.update(dt)
        self.check_pellet_events()
        self.check_ghost_events()
        self.check_events()
        self.render()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
               self.ghost.start_freight()

    def check_ghost_events(self):
        if self.pacman.collide_ghost(self.ghost):
            if self.ghost.mode.current is FREIGHT:
               self.ghost.start_spawn()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
