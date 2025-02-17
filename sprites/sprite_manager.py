import pygame
import os
from PIL import Image
import glob

class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.animations = {}
        
    def load_sprite(self, name, path, scale=1):
        """Load a single sprite"""
        try:
            if path.lower().endswith('.gif'):
                # Load first frame of GIF
                img = Image.open(path)
                img = img.convert('RGBA')
                sprite_str = img.tobytes()
                sprite_size = img.size
                sprite = pygame.image.fromstring(sprite_str, sprite_size, 'RGBA')
            else:
                sprite = pygame.image.load(path).convert_alpha()
                
            if scale != 1:
                new_width = int(sprite.get_width() * scale)
                new_height = int(sprite.get_height() * scale)
                sprite = pygame.transform.scale(sprite, (new_width, new_height))
            self.sprites[name] = sprite
            return True
        except Exception as e:
            print(f"Error loading sprite: {path} - {str(e)}")
            return False
            
    def load_animation(self, name, path_pattern, frame_count, scale=1):
        """Load a sequence of sprites for animation"""
        frames = []
        for i in range(frame_count):
            path = path_pattern.format(i + 1)  # Changed to 1-based indexing for your files
            try:
                if path.lower().endswith('.gif'):
                    img = Image.open(path)
                    img = img.convert('RGBA')
                    sprite_str = img.tobytes()
                    sprite_size = img.size
                    sprite = pygame.image.fromstring(sprite_str, sprite_size, 'RGBA')
                else:
                    sprite = pygame.image.load(path).convert_alpha()
                    
                if scale != 1:
                    new_width = int(sprite.get_width() * scale)
                    new_height = int(sprite.get_height() * scale)
                    sprite = pygame.transform.scale(sprite, (new_width, new_height))
                frames.append(sprite)
            except Exception as e:
                print(f"Error loading animation frame: {path} - {str(e)}")
                return False
        self.animations[name] = frames
        return True

    def load_direction_animations(self, base_path, direction):
        """Load all animation frames for a specific direction"""
        pattern = os.path.join(base_path, f"pacman-{direction} *.gif")
        files = sorted(glob.glob(pattern))
        if files:
            frames = []
            for file in files:
                try:
                    img = Image.open(file)
                    img = img.convert('RGBA')
                    sprite_str = img.tobytes()
                    sprite_size = img.size
                    sprite = pygame.image.fromstring(sprite_str, sprite_size, 'RGBA')
                    frames.append(sprite)
                except Exception as e:
                    print(f"Error loading animation frame: {file} - {str(e)}")
            if frames:
                # Only take the first 4 frames if we have more
                frames = frames[:4]
                self.animations[f"pacman_{direction}"] = frames
                return True
        return False

    def load_ghost_animations(self, base_path):
        """Load ghost animation frames"""
        pattern = os.path.join(base_path, "ghost *.gif")
        files = sorted(glob.glob(pattern))
        if files:
            frames = []
            for file in files:
                try:
                    img = Image.open(file)
                    img = img.convert('RGBA')
                    sprite_str = img.tobytes()
                    sprite_size = img.size
                    sprite = pygame.image.fromstring(sprite_str, sprite_size, 'RGBA')
                    frames.append(sprite)
                except Exception as e:
                    print(f"Error loading animation frame: {file} - {str(e)}")
            if frames:
                # Store the ghost animation frames
                self.animations["ghost"] = frames
                # Use the same frames for all ghost types and directions
                for ghost_type in ["red", "pink", "blue", "orange"]:
                    for direction in ["up", "down", "left", "right"]:
                        self.animations[f"ghost_{ghost_type}_{direction}"] = frames
                # Use for frightened state too
                self.animations["ghost_frightened"] = frames
                return True
        return False
    
    def get_sprite(self, name):
        """Get a single sprite by name"""
        return self.sprites.get(name)
    
    def get_animation_frame(self, name, frame_index):
        """Get a specific frame from an animation"""
        if name in self.animations:
            frames = self.animations[name]
            return frames[frame_index % len(frames)]
        return None 