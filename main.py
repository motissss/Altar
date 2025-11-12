import os, sys, pygame
from settings import *
from classes.player import Player
from classes.gnome import Gnome

pygame.init()

# Pamata ceļš un assets funkcija
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
def asset(path):
    return os.path.join(BASE_DIR, "assets", path)

# Ekrāna izmēri
display_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
pygame.display.toggle_fullscreen()
pygame.display.set_caption("Altar")
clock = pygame.time.Clock()

# Fons
bg_path = asset("background.png")
bg = pygame.image.load(bg_path).convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Spēlētāja un Gnome pozīcijas
SPAWN_X = SCREEN_WIDTH * 0.21
GROUND_Y = SCREEN_HEIGHT * 0.62
player = Player(SPAWN_X, GROUND_Y)
gnome = Gnome(SCREEN_WIDTH * 0.7, GROUND_Y)

# Fonts
font = pygame.font.SysFont(None, 36)
dialog_font = pygame.font.SysFont(None, 28)

# Dialogue
show_dialogue = False
dialogue_line1 = "Hello, fellow soul."
dialogue_line2 = "You may choose one of the 3 classes to progress and survive"

# Pogas
button_width, button_height = 120, 40
button_gap = 10
classes = ["Warrior", "Archer", "Mage"]
buttons = []
for i, cls in enumerate(classes):
    rect = pygame.Rect(
        gnome.rect.centerx - (button_width + button_gap) + i * (button_width + button_gap),
        gnome.rect.bottom + 10,
        button_width,
        button_height
    )
    buttons.append((rect, cls))

running = True
while running:
    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()

    # --- Event loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if show_dialogue:
                mouse_pos = pygame.mouse.get_pos()
                for rect, cls in buttons:
                    if rect.collidepoint(mouse_pos):
                        print(f"You selected {cls}!")  # klikšķis tagad strādā

    # --- Spēlētāja kustība ---
    player.handle_input(keys, dt)
    player.update_animation(dt)

    # --- Gnome sekojošs spēlētājam ---
    gnome.update(player)

    # --- Dialoga loģika ---
    distance = abs(player.x - gnome.x)
    if distance <= 100 and keys[pygame.K_e]:
        show_dialogue = True
    if distance > 100:
        show_dialogue = False

    # --- Zīmēšana ---
    screen.blit(bg, (0, 0))
    player.draw(screen)
    gnome.draw(screen)

    if distance <= 100 and not show_dialogue:
        prompt_surface = font.render("Press E to talk", True, (255, 255, 255))
        screen.blit(prompt_surface, (gnome.rect.centerx - prompt_surface.get_width() // 2, gnome.rect.top - 40))

    if show_dialogue:
        # divas rindas
        line1_surf = dialog_font.render(dialogue_line1, True, (255, 255, 255))
        line2_surf = dialog_font.render(dialogue_line2, True, (255, 255, 255))
        screen.blit(line1_surf, (gnome.rect.centerx - line1_surf.get_width() // 2, gnome.rect.top - 80))
        screen.blit(line2_surf, (gnome.rect.centerx - line2_surf.get_width() // 2, gnome.rect.top - 50))

        # zīmē pogas
        for rect, cls in buttons:
            pygame.draw.rect(screen, (50, 50, 200), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            text_surf = dialog_font.render(cls, True, (255, 255, 255))
            screen.blit(text_surf, (
                rect.centerx - text_surf.get_width() // 2,
                rect.centery - text_surf.get_height() // 2
            ))

    pygame.display.flip()

pygame.quit()
sys.exit()
    