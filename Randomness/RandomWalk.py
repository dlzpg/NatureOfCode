import random
import pygame
 
WIDTH, HEIGHT = 640, 240
BACKGROUND = (255, 255, 255)
POINT_COLOR = (0, 0, 0)
 
 
class Walker:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
 
    def step(self):
        choice = random.randint(0, 3) 
 
        if choice == 0:
            self.x += 1
        elif choice == 1:
            self.x -= 1
        elif choice == 2:
            self.y += 1
        else:
            self.y -= 1
 
        #Mantener al caminante dentro del lienzo
        self.x = max(0, min(WIDTH - 1, self.x))
        self.y = max(0, min(HEIGHT - 1, self.y))
 
    def show(self, surface):
        surface.set_at((int(self.x), int(self.y)), POINT_COLOR)
 
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Random Walk")
    clock = pygame.time.Clock()
 
    walker = Walker()
 
    screen.fill(BACKGROUND)
 
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Presiona r para reiniciar el caminante y limpiar el lienzo
                if event.key == pygame.K_r:
                    screen.fill(BACKGROUND)
                    walker = Walker()
                if event.key == pygame.K_SPACE:
                    paused = not paused
 
        if not paused:
            walker.step()
            walker.show(screen)
 
        pygame.display.flip()
        clock.tick(60) 
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()