import random
import pygame
import math
import numpy as np
from pygame.math import Vector2
 
WIDTH, HEIGHT = 640, 480
FPS = 60
NUM_MOVERS = 9

G= 1.0 #Gravitational constant

class Attractor:
    def __init__(self, x, y):
        self.position= Vector2(x, y)
        self.mass = 50
 
    def calculate_drag(self, mover):
        force = Vector2(self.position.x -mover.position.x, self.position.y - mover.position.y)
        distance = (force.x**2 + force.y**2)**0.5
        distance = max(5, min(distance, 25))

        strength = (G * self.mass * mover.mass) / (distance * distance)
        force= force / np.linalg.norm(force) * strength
        return force

class Mover:
    def __init__(self, x, y, mass):
        self.mass = mass
        self.radius = mass * 8
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.angle = 0 
 
    def apply_force(self, force):
        #Segunda ley de Newton: A = F / M
        self.acceleration += force / self.mass
 
    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0.5
 
    def show(self, surface):
        w, h = self.radius, self.radius / 2
        corners = [Vector2(-w / 2, -h / 2), Vector2(w / 2, -h / 2),
                   Vector2(w / 2, h / 2), Vector2(-w / 2, h / 2)]

        #Rotar cada esquina según self.angle y moverla a la posición del mover
        points = [self.position + c.rotate_rad(self.angle) for c in corners]

        pygame.draw.polygon(surface, (127, 127, 127), points)  
        pygame.draw.polygon(surface, (0, 0, 0), points, 2) 
    
    def check_edges(self):
        # Suelo
        if self.position.y > HEIGHT - self.radius:
            self.position.y = HEIGHT - self.radius
            self.velocity.y *= -0.5  
        # Techo
        elif self.position.y < self.radius:
            self.position.y = self.radius
            self.velocity.y *= -0.5

        # Pared derecha
        if self.position.x > WIDTH - self.radius:
            self.position.x = WIDTH - self.radius
            self.velocity.x *= -0.5
        # Pared izquierda
        elif self.position.x < self.radius:
            self.position.x = self.radius
            self.velocity.x *= -0.5

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Example 2.5")
    clock = pygame.time.Clock()
 
    attractor = Attractor(WIDTH // 2, HEIGHT // 2)
    mover = Mover(random.uniform(0, WIDTH), random.uniform(0, HEIGHT), random.uniform(1, 3))

    force = Vector2(0, random.uniform(0.4, 0.6)*mover.mass) 
    mover.apply_force(force)
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mover = Mover(random.uniform(0, WIDTH), random.uniform(0, HEIGHT), random.uniform(6, 8))
 
        screen.fill((255, 255, 255))

        xM, yM =pygame.mouse.get_pos()
        mover.angle = math.atan2(yM - mover.position.y, xM - mover.position.x)

        attractor.position = Vector2(xM, yM)
        mover.apply_force(attractor.calculate_drag(mover))
 
        mover.update()
        mover.check_edges()
        mover.show(screen)
 
        pygame.display.flip()
        clock.tick(FPS)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()