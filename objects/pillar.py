import pygame

class Pillar:
    def __init__(self, x, y):
        # Load both textures
        self.pillar_img = pygame.image.load("assets/pillar.png").convert_alpha()
        self.sword_img = pygame.image.load("assets/sword.png").convert_alpha()

        # Scale pillar and sword 10x bigger
        self.pillar_img = pygame.transform.scale_by(self.pillar_img, 8)
        self.sword_img = pygame.transform.scale_by(self.sword_img, 5)

        # Position
        self.pillar_rect = self.pillar_img.get_rect(center=(x, y))
        self.sword_rect = self.sword_img.get_rect(midbottom=self.pillar_rect.midtop)

    def draw(self, screen):
        screen.blit(self.pillar_img, self.pillar_rect)
        screen.blit(self.sword_img, self.sword_rect)
