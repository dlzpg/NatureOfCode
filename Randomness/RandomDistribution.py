import random
import pygame
 
WIDTH, HEIGHT = 640, 360
BACKGROUND = (255, 255, 255)
BAR_COLOR = (50, 50, 50)
AXIS_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
 
MEAN = 0.0
STD_DEV = 1.0
 
# Configuración del histograma
NUM_BUCKETS = 41          
RANGE_MIN = -4.0         
RANGE_MAX = 4.0
SAMPLES_PER_FRAME = 5  
 
 
class GaussianHistogram:
    def __init__(self):
        self.buckets = [0] * NUM_BUCKETS
        self.bucket_width = (RANGE_MAX - RANGE_MIN) / NUM_BUCKETS
        self.max_count = 1  #evita división por cero al escalar barras
 
    def add_sample(self, value):
        # Ubicar el valor dentro de un bucket
        index = int((value - RANGE_MIN) / self.bucket_width)
        if 0 <= index < NUM_BUCKETS:
            self.buckets[index] += 1
            if self.buckets[index] > self.max_count:
                self.max_count = self.buckets[index]
 
    def step(self):
        for _ in range(SAMPLES_PER_FRAME):
            value = random.gauss(MEAN, STD_DEV)
            self.add_sample(value)
 
    def show(self, surface, font):
        margin_bottom = 40
        plot_height = HEIGHT - margin_bottom - 20
        bar_width = WIDTH / NUM_BUCKETS
 
        for i, count in enumerate(self.buckets):
            bar_height = (count / self.max_count) * plot_height
            x = i * bar_width
            y = HEIGHT - margin_bottom - bar_height
            rect = pygame.Rect(x + 1, y, max(1, bar_width - 2), bar_height)
            pygame.draw.rect(surface, BAR_COLOR, rect)
 
        # Eje horizontal
        pygame.draw.line(
            surface, AXIS_COLOR,
            (0, HEIGHT - margin_bottom), (WIDTH, HEIGHT - margin_bottom), 2
        )
 
        # Total de muestras
        total = sum(self.buckets)
        label = font.render(f"Muestras: {total}", True, TEXT_COLOR)
        surface.blit(label, (10, HEIGHT - margin_bottom + 10))
 
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Distribución Normal en vivo")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
 
    histogram = GaussianHistogram()
 
    running = True
    paused= False 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    histogram = GaussianHistogram()
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            histogram.step()
 
            screen.fill(BACKGROUND)
            histogram.show(screen, font)
    
            pygame.display.flip()
            clock.tick(60)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()