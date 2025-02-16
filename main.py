import pygame
from pygame.locals import *
from constants import *
from pacman.pacman import Pacman
from movement.nodes import NodeGroup
from ghosts.ghost import Ghost
from pellets.pellet import PelletGroup

class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.background = None

    def set_background(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def start_game(self):
        self.set_background()    
        self.nodes = NodeGroup("maze.txt")
        home_key = self.nodes.create_home_nodes(11.5, 14)
        self.nodes.connect_home_nodes(home_key, (12,14), LEFT)
        self.nodes.connect_home_nodes(home_key, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.start_remp_node())
        self.pellet = PelletGroup("maze.txt")
        self.ghost = Ghost(self.nodes.getStartTempNode(), self.pacman)
        self.ghost.set_spawn_node(self.nodes.get_node_from_tiles(2+11.5, 3+14))

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.pellet.update(dt)
        self.ghost.update(dt)
        self.check_pellet_events()
        self.check_ghost_events()
        self.check_events()
        self.render()

    def check_ghost_events(self):
        if self.pacman.collide_ghost(self.ghost):
            if self.ghost.mode.current is FREIGHT:
               self.ghost.start_spawn()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pelletist)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
               self.ghost.start_freight()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellet.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
