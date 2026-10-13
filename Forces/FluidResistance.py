import random
import pygame
from pygame.math import Vector2
 
WIDTH, HEIGHT = 640, 480
FPS = 60
NUM_MOVERS = 9
 
 
class Liquid:
    def __init__(self, x, y, w, h, c):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.c = c  #coeficiente de arrastre
 
    def contains(self, mover):
        pos = mover.position
        return (self.x < pos.x < self.x + self.w and
                self.y < pos.y < self.y + self.h)
 
    def calculate_drag(self, mover):
        #Magnitud: coeficiente * velocidad^2
        speed = mover.velocity.length()
        if speed == 0:
            return Vector2(0, 0)
        drag_magnitude = self.c * speed * speed
        drag = -mover.velocity.normalize()
        drag *= drag_magnitude
        return drag
 
    def show(self, surface):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(surface, (200, 200, 200), rect)
 
 
class Mover:
    def __init__(self, x, y, mass):
        self.mass = mass
        self.radius = mass * 8 / 2
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
 
    def apply_force(self, force):
        #Segunda ley de Newton: A = F / M
        self.acceleration += force / self.mass
 
    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0
 
    def show(self, surface):
        center = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(surface, (127, 127, 127), center, int(self.radius))
        pygame.draw.circle(surface, (0, 0, 0), center, int(self.radius), 2)
 
    def check_edges(self):
        if self.position.y > HEIGHT - self.radius:
            self.position.y = HEIGHT - self.radius
            self.velocity.y *= -0.9  #rebote con pérdida de energía
 
 
def reset():
    n_balls = 5
    movers = [
        Mover(40 + j * WIDTH // n_balls, 0, random.uniform(0.5, 3))
        for j in range(n_balls)
    ]
    return movers
 
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Example 2.5")
    clock = pygame.time.Clock()
 
    liquid = Liquid(0, HEIGHT / 2, WIDTH, HEIGHT / 2, 0.1)
    movers = reset()
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                movers = reset()
 
        screen.fill((255, 255, 255))
        liquid.show(screen)
 
        for mover in movers:
            # Arrastre solo si el mover está dentro del líquido
            if liquid.contains(mover):
                mover.apply_force(liquid.calculate_drag(mover))
 
            #Gravedad escalada por la masa
            mover.apply_force(Vector2(0, 0.1 * mover.mass))
 
            mover.update()
            mover.check_edges()
            mover.show(screen)
 
        pygame.display.flip()
        clock.tick(FPS)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()