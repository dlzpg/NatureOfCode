import math
import random
import numpy as np
import pygame
 
from FlowField import build_permutation, _noise_2d
 
WIDTH, HEIGHT = 1800, 900
BACKGROUND = (255, 255, 255)
TRAIL_COLOR = (255, 255, 255)
FLIER_COLOR = (40, 90, 200)
 
RESOLUTION = 15     # tamaño de celda
NOISE_INC = 0.09     # "zoom" del ruido
 
NUM_FLIERS = 1000
FLIER_SPEED = 1.5   # píxeles que avanza cada flier por frame
TRAIL_FADE_ALPHA = 15  # qué tan rápido se desvanece la estela (más alto se borra más rápido)
 
 
def build_angle_field(seed=None):
    """
    Devuelve un array numpy (cols, rows) con el ángulo (en radianes)
    asignado a cada celda de la grid.
    """
    perm = build_permutation(seed)
    cols = WIDTH // RESOLUTION
    rows = HEIGHT // RESOLUTION
 
    angles = np.zeros((cols, rows), dtype=np.float64)
    for row in range(rows):
        yoff = row * NOISE_INC + 0.001
        for col in range(cols):
            xoff = col * NOISE_INC + 0.001
            noise_value = _noise_2d(xoff, yoff, perm)
            normalized = min(max((noise_value + 1) / 2, 0.0), 1.0)
            angles[col, row] = normalized * 2 * math.pi
 
    return angles
 
 
class Flier:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
 
    def follow(self, angle_field):
        cols, rows = angle_field.shape
        col = min(int(self.x // RESOLUTION), cols - 1)
        row = min(int(self.y // RESOLUTION), rows - 1)
        angle = angle_field[col, row]
 
        self.x += math.cos(angle) * FLIER_SPEED
        self.y += math.sin(angle) * FLIER_SPEED
 
        # Wrap around
        if self.x < 0:
            self.x = WIDTH - 1
        elif self.x >= WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT - 1
        elif self.y >= HEIGHT:
            self.y = 0
 
    def show(self, surface):
        pygame.draw.circle(surface, FLIER_COLOR, (int(self.x), int(self.y)), 1)
 
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flow Field Simulation")
    clock = pygame.time.Clock()
 
    angle_field = build_angle_field()
    fliers = [Flier() for _ in range(NUM_FLIERS)]
 
    #se dibuja sobre el lienzo cada frame parair desvaneciendo el rastro anterior
    fade_overlay = pygame.Surface((WIDTH, HEIGHT))
    fade_overlay.fill(TRAIL_COLOR)
    fade_overlay.set_alpha(TRAIL_FADE_ALPHA)
 
    screen.fill(BACKGROUND)
 
    paused = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    angle_field = build_angle_field()
                    fliers = [Flier() for _ in range(NUM_FLIERS)]
                    screen.fill(BACKGROUND)
 
        if not paused:
            screen.blit(fade_overlay, (0, 0)) 
            for flier in fliers:
                flier.follow(angle_field)
                flier.show(screen)
 
        pygame.display.flip()
        clock.tick(60)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()