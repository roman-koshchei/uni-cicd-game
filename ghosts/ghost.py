from pygame.locals import *
from movement.nodes import Node
from movement.vector import Vector2
from constants import *
from pacman.pacman import Pacman
from sprites.sprite_manager import SpriteManager
from .entity import Entity
from modes.modes import ModeController
import pygame


class Ghost(Entity):
    def __init__(
        self,
        node: Node,
        pacman: Pacman | None = None,
        sprite_manager: SpriteManager | None = None,
        ghost_type="red",
    ):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.direction_method = self.goal_direction
        self.pacman = pacman
        self.mode = ModeController(self)
        self.sprite_manager = sprite_manager
        self.ghost_type = ghost_type
        self.animation_frame = 0
        self.animation_speed = 0.2  # seconds per frame
        self.animation_timer = 0

    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()

        # Update animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_frame = (
                self.animation_frame + 1
            ) % 2  # Assuming 2 frames per direction
            self.animation_timer = 0

        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

    def start_freight(self):
        self.mode.set_freight_mode()
        if self.mode.current == FREIGHT:
            self.set_speed(40)  # Slower when frightened
            self.direction_method = self.random_direction

    def normal_mode(self):
        self.set_speed(80)  # Slightly slower than Pacman in normal mode
        self.direction_method = self.goal_direction

    def spawn(self):
        self.goal = self.spawn_node.position

    def set_spawn_node(self, node):
        self.spawn_node = node

    def start_spawn(self):
        self.mode.set_spawn_mode()
        if self.mode.current == SPAWN:
            self.set_speed(120)  # Fast but not too fast when returning to spawn
            self.direction_method = self.goal_direction
            self.spawn()

    def render(self, screen):
        if self.sprite_manager and self.visible:
            # Determine which sprite set to use based on mode
            if self.mode.current == FREIGHT:
                sprite_name = "ghost_frightened"
            elif self.mode.current == SPAWN:
                sprite_name = "ghost_eyes"
            else:
                sprite_name = f"ghost_{self.ghost_type}_{self.get_direction_name()}"

            # Get the appropriate sprite
            sprite = self.sprite_manager.get_animation_frame(
                sprite_name, self.animation_frame
            )

            if sprite:
                # Calculate position to center the sprite
                position = (
                    int(self.position.x - sprite.get_width() // 2),
                    int(self.position.y - sprite.get_height() // 2),
                )
                screen.blit(sprite, position)
            else:
                # Fallback to circle if sprite not found
                pygame.draw.circle(
                    screen, self.color, self.position.as_int(), self.radius
                )
        elif self.visible:
            # Fallback to circle if no sprite manager
            pygame.draw.circle(screen, self.color, self.position.as_int(), self.radius)

    def get_direction_name(self):
        if self.direction == UP:
            return "up"
        elif self.direction == DOWN:
            return "down"
        elif self.direction == LEFT:
            return "left"
        elif self.direction == RIGHT:
            return "right"
        return "right"  # Default direction when stopped
