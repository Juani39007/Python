import pygame
from config import *

class Player:
    """The player controlled by the user"""

    def __init__(self, x, y, color=PLAYER_COLOR, speed=PLAYER_SPEED):
        """Initialize the player with a position and size"""
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.speed = speed

        self.lives = INITIAL_LIVES  # Challenge 10
        self.invulnerable_until = 0  # Challenge 10: game time (ms) when the invulnerability ends
        self.boost = 0  # Challenge 11: extra speed while a speed boost is active
        self.boost_until = 0  # Challenge 11: game time (ms) when the speed boost ends

    def moveArrows(self):
        """Update the player's position based on keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons
        speed = self.speed + self.boost  # Challenge 11: speed including the boost

        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed
        if keys[pygame.K_UP]:
            self.rect.y -= speed
        if keys[pygame.K_DOWN]:
            self.rect.y += speed
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))  # Keep the player inside the window

    def moveWASD(self):
        """Update the player's position based on WASD keyboard input"""
        keys = pygame.key.get_pressed()  # Get the state of all keyboard buttons
        speed = self.speed + self.boost  # Challenge 11: speed including the boost

        if keys[pygame.K_a]:
            self.rect.x -= speed
        if keys[pygame.K_d]:
            self.rect.x += speed
        if keys[pygame.K_w]:
            self.rect.y -= speed
        if keys[pygame.K_s]:
            self.rect.y += speed
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))  # Keep the player inside the window

    def draw(self, surface):
        """Draw the player on the given surface"""
        pygame.draw.rect(surface, self.color, self.rect)

    def is_alive(self):
        """Challenge 10: the player is alive while it has lives left"""
        return self.lives > 0

    def is_invulnerable(self, now):
        """Challenge 10: the player cannot be hurt until invulnerable_until"""
        return now < self.invulnerable_until

    def hit(self, now):
        """Challenge 10: lose one life and be invulnerable for two seconds"""
        self.lives -= 1
        self.invulnerable_until = now + INVULNERABLE_TIME

    def heal(self):
        """Challenge 11: recover one life (never more than the initial lives)"""
        self.lives = min(self.lives + 1, INITIAL_LIVES)

    def start_boost(self, now):
        """Challenge 11: start the temporary speed boost"""
        self.boost = SPEED_BOOST_BONUS
        self.boost_until = now + SPEED_BOOST_DURATION

    def update_effects(self, now):
        """Challenge 11: the speed boost disappears when its time is over"""
        if now >= self.boost_until:
            self.boost = 0

    def change_speed(self, amount):
        """Change the speed, always between the minimum and the maximum"""
        self.speed = max(MIN_PLAYER_SPEED, min(MAX_PLAYER_SPEED, self.speed + amount))