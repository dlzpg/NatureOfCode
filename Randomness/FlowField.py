import math
import numpy as np
import pygame
 
from PerlinNoise import build_permutation
 
WIDTH, HEIGHT = 900, 900
BACKGROUND = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
 
RESOLUTION = 20   # tamaño de cada celda de la grilla, en píxeles
NOISE_INC = 0.15   # qué tan rápido cambia el ruido de una celda a la siguiente
 
 
ANGLES = np.arange(256) * (2 * math.pi / 256)
GRADIENTS = np.stack([np.cos(ANGLES), np.sin(ANGLES)], axis=-1)
 
 
def _fade(t):
    return t**3 * (t * (t * 6 - 15) + 10)
 
 
def _lerp(t, a, b):
    return a + t * (b - a)
 
 
def _grad(hash_value, x, y):
    gx, gy = GRADIENTS[hash_value]
    return gx * x + gy * y
 
 
def _noise_2d(x, y, perm):
    xi = int(math.floor(x)) & 255
    yi = int(math.floor(y)) & 255
    xf = x - math.floor(x)
    yf = y - math.floor(y)
 
    u = _fade(xf)
    v = _fade(yf)
 
    aa = perm[perm[xi] + yi]
    ab = perm[perm[xi] + yi + 1]
    ba = perm[perm[xi + 1] + yi]
    bb = perm[perm[xi + 1] + yi + 1]
 
    x1 = _lerp(u, _grad(aa, xf, yf), _grad(ba, xf - 1, yf))
    x2 = _lerp(u, _grad(ab, xf, yf - 1), _grad(bb, xf - 1, yf - 1))
 
    return _lerp(v, x1, x2)
 
 
def build_flow_field(seed=None):
    """
    Devuelve una lista de (x, y, angle) — una entrada por celda de la
    grilla, con su posición en pantalla y el ángulo (en radianes) que
    le asignó el ruido Perlin en esa coordenada.
    """
    perm = build_permutation(seed)
 
    cols = WIDTH // RESOLUTION
    rows = HEIGHT // RESOLUTION
 
    field = []
    for row in range(rows):
        # Pequeño offset para no caer justo en yi=0 (borde de gradientes)
        yoff = row * NOISE_INC + 0.001
        for col in range(cols):
            xoff = col * NOISE_INC + 0.001
 
            noise_value = _noise_2d(xoff, yoff, perm)
            # El ruido crudo cae aproximadamente en [-1, 1]; lo normalizamos a [0, 1] antes de mapearlo a un ángulo.
            normalized = (noise_value + 1) / 2
            normalized = min(max(normalized, 0.0), 1.0)  # por seguridad, recortar
            angle = normalized * 2 * math.pi
 
            x = col * RESOLUTION
            y = row * RESOLUTION
            field.append((x, y, angle))
 
    return field
 
def draw_flow_field(surface, field):
    half = RESOLUTION / 2
    for x, y, angle in field:
        cx = x + half
        cy = y + half
        dx = math.cos(angle) * half
        dy = math.sin(angle) * half
 
        start = (cx - dx, cy - dy)
        end = (cx + dx, cy + dy)
        pygame.draw.line(surface, LINE_COLOR, start, end, 1)
        pygame.draw.circle(surface, LINE_COLOR, (int(end[0]), int(end[1])), 2)
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flow Field with Perlin Noise")
 
    field = build_flow_field()
 
    screen.fill(BACKGROUND)
    draw_flow_field(screen, field)
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    screen.fill(BACKGROUND)
                    field = build_flow_field()
                    draw_flow_field(screen, field)

        pygame.display.flip()
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()