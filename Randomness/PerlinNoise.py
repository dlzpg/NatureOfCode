import numpy as np
import pygame
 
WIDTH, HEIGHT = 640, 640
INCREMENT = 0.02  #zoom del ruido
  
# 8 direcciones de gradiente típicas
GRAD2 = np.array(
    [
        (1, 1), (-1, 1), (1, -1), (-1, -1),
        (1, 0), (-1, 0), (0, 1), (0, -1),
    ],
    dtype=np.float64,
)
 
def build_permutation(seed=None):
    rng = np.random.default_rng(seed)
    perm = np.arange(256, dtype=np.int32)
    rng.shuffle(perm)
    return np.concatenate([perm, perm])
 
def fade(t):
    return t**3 * (t * (t * 6 - 15) + 10)
 
def lerp(t, a, b):
    return a + t * (b - a)
 
def grad2(hash_arr, x, y):
    h = hash_arr & 7
    g = GRAD2[h]
    return g[..., 0] * x + g[..., 1] * y
 
def perlin_noise_2d(x, y, perm):
    xi = np.floor(x).astype(np.int32) & 255
    yi = np.floor(y).astype(np.int32) & 255
    xf = x - np.floor(x)
    yf = y - np.floor(y)
 
    u = fade(xf)
    v = fade(yf)
 
    aa = perm[perm[xi] + yi]
    ab = perm[perm[xi] + yi + 1]
    ba = perm[perm[xi + 1] + yi]
    bb = perm[perm[xi + 1] + yi + 1]
 
    x1 = lerp(u, grad2(aa, xf, yf), grad2(ba, xf - 1, yf))
    x2 = lerp(u, grad2(ab, xf, yf - 1), grad2(bb, xf - 1, yf - 1))
 
    return lerp(v, x1, x2)
 
def generate_noise_field(seed=None):
    perm = build_permutation(seed)
 
    xs = np.arange(WIDTH) * INCREMENT
    ys = np.arange(HEIGHT) * INCREMENT
    xx, yy = np.meshgrid(xs, ys, indexing="ij")
 
    raw = perlin_noise_2d(xx, yy, perm)
 
    #Normalizamos con el rango real obtenido, igual que map(r,0,1,0,255).
    r_min, r_max = raw.min(), raw.max()
    normalized = (raw - r_min) / (r_max - r_min)  # a [0, 1]
    brightness = (normalized * 255).astype(np.uint8)
 
    return brightness
 
def brightness_to_surface(brightness):
    # pygame.surfarray espera un array (W, H, 3)
    rgb = np.stack([brightness, brightness, brightness], axis=-1)
    return pygame.surfarray.make_surface(rgb)
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Noise 2D")
 
    brightness = generate_noise_field()
    surface = brightness_to_surface(brightness)
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    brightness = generate_noise_field()
                    surface = brightness_to_surface(brightness)

        screen.blit(surface, (0, 0))
        pygame.display.flip()
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()