import pygame
from classes.player import Player

class Warrior(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.attack_power = 10
        self.hp = 150
        self.class_name = "Warrior"
        self.y_offset = 13  # tweak if feet don't sit on ground

        try:
            warrior_img = pygame.image.load("assets/Warrior.png").convert_alpha()
        except:
            warrior_img = pygame.image.load("assets/Character_Template.png").convert_alpha()

        # Scale preserving aspect ratio
        original_w, original_h = warrior_img.get_size()
        target_height = 150
        target_width = int(original_w * (target_height / original_h))
        warrior_img = pygame.transform.scale(warrior_img, (target_width, target_height))

        self.frames_stand = [warrior_img] * self.num_frames_stand
        self.frames_walk = [warrior_img] * self.num_frames_walk

        self.image = warrior_img
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))
        self.rect.y -= self.y_offset

    def attack(self):
        print("Warrior slashes with sword!")