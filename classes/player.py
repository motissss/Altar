import pygame
from settings import *

class Player:
    def __init__(self, x=400, y=640):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/Player_no_class.png").convert_alpha()
        
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = PLAYER_SPEED
        self.class_name = "No Class"

    def handle_input(self, keys):
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

    # Lock y position at 640
        self.y = 640

    # Keep player inside screen bounds
        if self.rect.width // 2 > self.x:
            self.x = self.rect.width // 2
        if self.x > SCREEN_WIDTH - self.rect.width // 2:
            self.x = SCREEN_WIDTH - self.rect.width // 2

        self.rect.center = (self.x, self.y)


    def draw(self, screen):
        screen.blit(self.image, self.rect)


class PlayerWarrior(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("assets/Player_warrior.png").convert_alpha()
        self.speed = PLAYER_SPEED
        self.class_name = "Warrior"

class PlayerArcher(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("assets/Player_archer.png").convert_alpha()
        self.speed = PLAYER_SPEED + 2
        self.class_name = "Archer"

class PlayerMage(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("assets/Player_mage.png").convert_alpha()
        self.speed = PLAYER_SPEED + 1
        self.class_name = "Mage"
