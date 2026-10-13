import random
import pygame
import math
import numpy as np
from pygame.math import Vector2

 
WIDTH, HEIGHT = 640, 480
FPS = 60

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

class Hunter: 
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.maxspeed = 5
        self.maxforce = 0.1

        self.r = 8 

    def update(self):
            self.velocity += self.acceleration
            self.position += self.velocity
            self.acceleration *= 0.5

    def seek(self, target):
        desired = target - self.position
        desired = desired.normalize() * self.maxspeed
        steer = desired - self.velocity
        if steer.length() > self.maxforce:
            steer.scale_to_length(self.maxforce)
        self.apply_force(steer)

    def apply_force(self, force):
        self.acceleration += force * 0.7

    def show(self, surface):
        angle = math.atan2(self.velocity.y, self.velocity.x)

        vertices = [Vector2(self.r * 2, 0),
                    Vector2(-self.r * 2, -self.r),
                    Vector2(-self.r * 2, self.r)]

        points = [self.position + v.rotate_rad(angle) for v in vertices]

        pygame.draw.polygon(surface, (127, 127, 127), points) 
        pygame.draw.polygon(surface, (0, 0, 0), points, 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Example 5.1")
    clock = pygame.time.Clock()
 
    attractor = Attractor(WIDTH // 2, HEIGHT // 2)
    hunter = Hunter(WIDTH // 2, HEIGHT // 2)

    force = Vector2(0, random.uniform(0.4, 0.6)) 
    hunter.apply_force(force)
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                hunter = Hunter(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
 
        screen.fill((255, 255, 255))

        xM, yM =pygame.mouse.get_pos()

        attractor.position = Vector2(xM, yM)

        hunter.seek(attractor.position)
 
        hunter.update()
        hunter.show(screen)
 
        pygame.display.flip()
        clock.tick(FPS)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()