import random
import pygame
from pygame.math import Vector2
 
WIDTH, HEIGHT = 640, 240
FPS = 60
 
 
class Mover:
    def __init__(self, x, y, mass):
        self.mass = mass
        self.radius = mass * 8 / 2       
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
 
    def apply_force(self, force):
        #Newton's second law with mass: A = F / M
        self.acceleration += force / self.mass
 
    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0              #clear acceleration each frame
 
    def show(self, surface):
        center = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(surface, (175, 175, 175), center, int(self.radius))
        pygame.draw.circle(surface, (0, 0, 0), center, int(self.radius), 2)
 
    def contact_edge(self):
        return (HEIGHT - (self.position.y + self.radius)) < 1
 
    def bounce_edges(self):
        if self.position.x > WIDTH - self.radius:
            self.position.x = WIDTH - self.radius
            self.velocity.x *= -1
        elif self.position.x < self.radius:
            self.position.x = self.radius
            self.velocity.x *= -1
 
        if self.position.y > HEIGHT - self.radius:
            self.position.y = HEIGHT - self.radius
            self.velocity.y *= -1
 
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Example 2.4")
    clock = pygame.time.Clock()

    n_balls = 4
    movers = [Mover(40 + i * WIDTH // n_balls, 30, random.uniform(1, 4)) for i in range(n_balls)]
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
        screen.fill((255, 255, 255))
 
        wind = Vector2(0.1, 0)
        mouse_down = pygame.mouse.get_pressed()[0]
 
        for mover in movers:
            #Gravity scaled by mass so all movers fall at the same rate
            gravity = Vector2(0, 0.1 * mover.mass)
            mover.apply_force(gravity)
 
            if mouse_down:
                mover.apply_force(wind)
 
            # Friction only applies while touching the floor
            if mover.contact_edge() and mover.velocity.length() > 0:
                mu = 0.1
                normal_force = 1                      #simplified normal force
                friction = -mover.velocity.normalize()  #opposite of velocity
                friction *= mu * normal_force         #scale by magnitude
                mover.apply_force(friction)
 
            mover.update()
            mover.bounce_edges()
            mover.show(screen)
 
        pygame.display.flip()
        clock.tick(FPS)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()