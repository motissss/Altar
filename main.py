import pygame, sys
from settings import *
from classes.player import Player
from classes.gnome import Gnome

pygame.init()

# Fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Altar")
clock = pygame.time.Clock()

# Background
bg = pygame.image.load("assets/background.png").convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create player and gnome
player = Player(400, 602)
gnome = Gnome(1400, 602)

# Fonts
font = pygame.font.SysFont(None, 36)
dialog_font = pygame.font.SysFont(None, 28)

# Dialogue
show_dialogue = False
dialogue_text = "Hello, fellow soul. You may choose one of the 3 classes to progress and survive"

# Button setup (once)
button_width, button_height = 120, 40
button_gap = 10
classes = ["Warrior", "Archer", "Mage"]
buttons = []
for i, cls in enumerate(classes):
    rect = pygame.Rect(
        gnome.rect.centerx - (button_width + button_gap) + i * (button_width + button_gap),
        gnome.rect.bottom + 10,  # slightly below gnome
        button_width,
        button_height
    )
    buttons.append((rect, cls))

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()
    player.handle_input(keys, dt)
    player.update_animation(dt)

    # Update to face player
    gnome.update(player)

    # Check distance
    distance = abs(player.x - gnome.x)

    # Show dialogue if player presses E while close
    if distance <= 100 and keys[pygame.K_e]:
        show_dialogue = True

    # Hide dialogue if player moves away
    if distance > 100:
        show_dialogue = False

    # Draw everything
    screen.blit(bg, (0, 0))
    player.draw(screen)
    gnome.draw(screen)

    #if close and dialogue not yet shown
    if distance <= 100 and not show_dialogue:
        prompt_surface = font.render("Press E to talk", True, (255, 255, 255))
        screen.blit(prompt_surface, (gnome.rect.centerx - prompt_surface.get_width() // 2, gnome.rect.top - 40))

    #dialogue and buttons if shown
    if show_dialogue:
        dialogue_surface = dialog_font.render(dialogue_text, True, (255, 255, 255))
        screen.blit(dialogue_surface, (gnome.rect.centerx - dialogue_surface.get_width() // 2, gnome.rect.top - 80))

        #buttons
        for rect, cls in buttons:
            pygame.draw.rect(screen, (50, 50, 200), rect)        # Button background
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)   # Border
            text_surf = dialog_font.render(cls, True, (255, 255, 255))
            screen.blit(text_surf, (
                rect.centerx - text_surf.get_width() // 2,
                rect.centery - text_surf.get_height() // 2
            ))

        #clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if show_dialogue:  # Only allow clicks when dialogue/buttons visible
                    mouse_pos = pygame.mouse.get_pos()
                    for rect, cls in buttons:
                        if rect.collidepoint(mouse_pos):
                            print(f"You selected {cls}!")  # Trigger once

    pygame.display.flip()

pygame.quit()
sys.exit()
