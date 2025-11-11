import pygame, sys
from settings import *
from classes.player import Player
from objects.pillar import Pillar

pygame.init()

# Fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

pygame.display.set_caption("Altar")
clock = pygame.time.Clock()

# Background
bg = pygame.image.load("assets/background.png").convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))


rel_x = (145 / 192) * SCREEN_WIDTH
rel_y = (77 / 108) * SCREEN_HEIGHT

pillar = Pillar(rel_x, rel_y)
player = Player(400, 640)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()
    player.handle_input(keys)

    screen.blit(bg, (0, 0))
    pillar.draw(screen)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
