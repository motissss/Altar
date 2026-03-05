import os, sys, pygame
from settings import *
from classes.player import Player
from classes.gnome import Gnome

pygame.init()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

def asset(path):
    return os.path.join(BASE_DIR, "assets", path)

display_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
pygame.display.toggle_fullscreen()
pygame.display.set_caption("Altar")
clock = pygame.time.Clock()

# --- Assets ---
bg = pygame.transform.scale(pygame.image.load(asset("background.png")).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Grass tile for top-down
try:
    grass_tile = pygame.transform.scale(pygame.image.load(asset("Grass_Top_Down.png")).convert(), (320, 320))
except:
    grass_tile = pygame.Surface((320, 320))
    grass_tile.fill((34, 139, 34))

SPAWN_X = SCREEN_WIDTH * 0.21
GROUND_Y = SCREEN_HEIGHT * 0.62
player = Player(SPAWN_X, GROUND_Y)
gnome = Gnome(SCREEN_WIDTH * 0.7, GROUND_Y)

font = pygame.font.SysFont(None, 36)
dialog_font = pygame.font.SysFont(None, 28)

show_dialogue = False
dialogue_line1 = "Hello, fellow soul."
dialogue_line2 = "You may choose one of the 3 classes to progress and survive"

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

# --- Game state ---
STATE_SIDEVIEW = "sideview"
STATE_TOPDOWN = "topdown"
game_state = STATE_SIDEVIEW
class_chosen = False
td_player_img = None

# Top-down player position
td_x = SCREEN_WIDTH // 2
td_y = SCREEN_HEIGHT // 2
TD_SPEED = 300

running = True
while running:
    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if show_dialogue:
                mouse_pos = pygame.mouse.get_pos()
                for rect, cls in buttons:
                    if rect.collidepoint(mouse_pos):
                        if cls == "Warrior":
                            from classes.warrior import Warrior
                            player = Warrior(player.x, player.y)
                            class_chosen = True
                        elif cls == "Archer":
                            from classes.archer import Archer
                            player = Archer(player.x, player.y)
                            class_chosen = True
                        elif cls == "Mage":
                            from classes.mage import Mage
                            player = Mage(player.x, player.y)
                            class_chosen = True
                        show_dialogue = False

    # ======= SIDE VIEW =======
    if game_state == STATE_SIDEVIEW:
        player.handle_input(keys, dt)
        player.update_animation(dt)
        gnome.update(player)

        distance = abs(player.x - gnome.x)
        if distance <= 100 and keys[pygame.K_e]:
            show_dialogue = True
        if distance > 100:
            show_dialogue = False

        # Trigger top-down only if class has been chosen
        if player.rect.right >= SCREEN_WIDTH - 5 and class_chosen:
            # Try to load class-specific top-down texture
            try:
                td_player_img = pygame.transform.scale(
                    pygame.image.load(asset(f"{player.class_name.lower()}_top_down.png")).convert_alpha(),
                    (64, 64)
                )
            except:
                td_player_img = None  # falls back to red circle
            game_state = STATE_TOPDOWN
            td_x = SCREEN_WIDTH // 2
            td_y = SCREEN_HEIGHT // 2
            show_dialogue = False

        # Draw
        screen.blit(bg, (0, 0))
        player.draw(screen)
        gnome.draw(screen)

        if distance <= 100 and not show_dialogue:
            prompt = font.render("Press E to talk", True, (255, 255, 255))
            screen.blit(prompt, (gnome.rect.centerx - prompt.get_width() // 2, gnome.rect.top - 40))

        if show_dialogue:
            line1 = dialog_font.render(dialogue_line1, True, (255, 255, 255))
            line2 = dialog_font.render(dialogue_line2, True, (255, 255, 255))
            screen.blit(line1, (gnome.rect.centerx - line1.get_width() // 2, gnome.rect.top - 80))
            screen.blit(line2, (gnome.rect.centerx - line2.get_width() // 2, gnome.rect.top - 50))
            for rect, cls in buttons:
                pygame.draw.rect(screen, (50, 50, 200), rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 2)
                text_surf = dialog_font.render(cls, True, (255, 255, 255))
                screen.blit(text_surf, (
                    rect.centerx - text_surf.get_width() // 2,
                    rect.centery - text_surf.get_height() // 2
                ))

    # ======= TOP DOWN VIEW =======
    elif game_state == STATE_TOPDOWN:
        if keys[pygame.K_a]: td_x -= TD_SPEED * dt
        if keys[pygame.K_d]: td_x += TD_SPEED * dt
        if keys[pygame.K_w]: td_y -= TD_SPEED * dt
        if keys[pygame.K_s]: td_y += TD_SPEED * dt

        # Clamp to screen
        td_x = max(32, min(SCREEN_WIDTH - 32, td_x))
        td_y = max(32, min(SCREEN_HEIGHT - 32, td_y))

        # Tile grass across full screen
        tile_w, tile_h = grass_tile.get_size()
        for gy in range(0, SCREEN_HEIGHT, tile_h):
            for gx in range(0, SCREEN_WIDTH, tile_w):
                screen.blit(grass_tile, (gx, gy))

        # Draw player — texture or red circle fallback
        if td_player_img:
            screen.blit(td_player_img, (int(td_x) - 32, int(td_y) - 32))
        else:
            pygame.draw.circle(screen, (220, 30, 30), (int(td_x), int(td_y)), 24)

    pygame.display.flip()

pygame.quit()
sys.exit()