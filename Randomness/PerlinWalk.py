import math
import random
import pygame
 
 
WIDTH, HEIGHT = 640, 240
BACKGROUND = (255, 255, 255)
STROKE_COLOR = (0, 0, 0)
FILL_COLOR = (127, 127, 127)
CIRCLE_DIAMETER = 48
 
NOISE_INCREMENT = 0.01
OCTAVES = 4
PERSISTENCE = 0.5
LACUNARITY = 2.0
 
 
class PerlinNoise:
    def __init__(self, seed=None):
        rng = random.Random(seed)
        perm = list(range(256))
        rng.shuffle(perm)
        self.perm = perm + perm  # tabla duplicada para evitar overflow de índices
 
    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)
 
    def _lerp(self, t, a, b):
        return a + t * (b - a)
 
    def _grad(self, hash_value, x):
        return x if (hash_value & 1) == 0 else -x
 
    def noise(self, x):
        xi = int(math.floor(x)) & 255
        xf = x - math.floor(x)
 
        u = self._fade(xf)
 
        a = self.perm[xi]
        b = self.perm[xi + 1]
 
        result = self._lerp(u, self._grad(a, xf), self._grad(b, xf - 1))
        return (result + 1) / 2  # normalizado a [0, 1]
 
    def fbm(self, x, octaves=OCTAVES, persistence=PERSISTENCE, lacunarity=LACUNARITY):
        total = 0.0
        amplitude = 1.0
        frequency = 1.0
        max_value = 0.0
 
        for _ in range(octaves):
            total += self.noise(x * frequency) * amplitude
            max_value += amplitude
            amplitude *= persistence
            frequency *= lacunarity
 
        return total / max_value  
 
 
class Walker:
    def __init__(self, noise_gen):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.tx = random.uniform(0, 10000)
        self.ty = random.uniform(0, 10000)
        self.noise_gen = noise_gen
 
    def step(self):
        nx = self.noise_gen.fbm(self.tx)
        ny = self.noise_gen.fbm(self.ty)
 
        self.x = self._map(nx, 0, 1, 0, WIDTH)
        self.y = self._map(ny, 0, 1, 0, HEIGHT)
 
        self.tx += NOISE_INCREMENT
        self.ty += NOISE_INCREMENT
 
    def _map(self, value, start1, stop1, start2, stop2):
        return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))
 
    def show(self, surface):
        pygame.draw.circle(
            surface, FILL_COLOR, (int(self.x), int(self.y)), CIRCLE_DIAMETER // 2
        )
        pygame.draw.circle(
            surface, STROKE_COLOR, (int(self.x), int(self.y)), CIRCLE_DIAMETER // 2, 2
        )
 
 
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Perlin Noise Walker")
    clock = pygame.time.Clock()
    screen.fill(BACKGROUND)
 
    noise_gen = PerlinNoise() 
    walker = Walker(noise_gen)
 
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    screen.fill(BACKGROUND)
                    noise_gen = PerlinNoise()
                    walker = Walker(noise_gen)
                if event.key == pygame.K_SPACE:
                    paused = not paused
        if not paused:  
            walker.step()
    
            #screen.fill(BACKGROUND)
            walker.show(screen)
    
            pygame.display.flip()
            clock.tick(60)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()