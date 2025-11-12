import pygame

class Gnome:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # Load sprite (default facing left)
        self.image = pygame.image.load("assets/gnome.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(midbottom=(self.x, self.y))

        self.facing_right = False  # Will update based on player

    def update(self, player):
        # Flip sprite to face player
        if player.x > self.x:
            self.facing_right = True
        else:
            self.facing_right = False

    def draw(self, screen):
        image_to_draw = self.image
        # Flip only if sprite is facing left by default
        if self.facing_right:
            image_to_draw = pygame.transform.flip(self.image, True, False)
        screen.blit(image_to_draw, self.rect)
