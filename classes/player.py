import pygame
from settings import *

class Player:
    def __init__(self, x=400, y=601):
        self.x = x
        self.y = y

        # --- Standing sprite sheet ---
        self.sheet_stand = pygame.image.load("assets/Player_no_class.png").convert_alpha()
        self.frame_width, self.frame_height = 64, 64
        self.num_frames_stand = 14
        self.frames_stand = []

        for i in range(self.num_frames_stand):
            frame = self.sheet_stand.subsurface(
                pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            frame = pygame.transform.scale(frame, (126, 150))
            self.frames_stand.append(frame)

        # --- Walking sprite sheet ---
        self.sheet_walk = pygame.image.load("assets/Player_no_class_walking.png").convert_alpha()
        self.num_frames_walk = 7
        self.frames_walk = []

        for i in range(self.num_frames_walk):
            frame = self.sheet_walk.subsurface(
                pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            frame = pygame.transform.scale(frame, (126, 150))
            self.frames_walk.append(frame)

        # Animation setup
        self.current_frame = 0
        self.animation_speed = 0.15  # seconds per frame
        self.animation_timer = 0
        self.state = "stand"  # "stand" or "walk"
        self.facing_right = True   # New: track facing direction

        self.image = self.frames_stand[self.current_frame]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.speed = PLAYER_SPEED
        self.class_name = "No Class"

    def handle_input(self, keys, dt):
        moving = False
        if keys[pygame.K_a]:
            self.x -= self.speed * dt
            moving = True
            self.facing_right = False
        if keys[pygame.K_d]:
            self.x += self.speed * dt
            moving = True
            self.facing_right = True

        # Lock Y
        self.y = 590

        # Screen bounds
        if self.rect.width // 2 > self.x:
            self.x = self.rect.width // 2
        if self.x > SCREEN_WIDTH - self.rect.width // 2:
            self.x = SCREEN_WIDTH - self.rect.width // 2

        self.rect.center = (self.x, self.y)

        # Animation state
        new_state = "walk" if moving else "stand"
        if new_state != self.state:
            self.state = new_state
            self.current_frame = 0   # Reset animation frame when state changes
            self.animation_timer = 0


    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if self.state == "stand":
                self.current_frame = (self.current_frame + 1) % self.num_frames_stand
                self.image = self.frames_stand[self.current_frame]
            elif self.state == "walk":
                self.current_frame = (self.current_frame + 1) % self.num_frames_walk
                self.image = self.frames_walk[self.current_frame]



    def draw(self, screen):
        image_to_draw = self.image
        if not self.facing_right:
            image_to_draw = pygame.transform.flip(self.image, True, False)
        screen.blit(image_to_draw, self.rect)

