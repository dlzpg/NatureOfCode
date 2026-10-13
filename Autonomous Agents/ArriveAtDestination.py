import pygame
import math
from pygame.math import Vector2

WIDTH, HEIGHT = 640, 480
FPS = 60

G= 1.0 #Gravitational constant


class Vehicle: 
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.maxspeed = 5
        self.maxforce = 0.1

        self.r = 8 
        self.angle = 0

    def update(self):
            self.velocity += self.acceleration
            self.position += self.velocity
            self.acceleration *= 0.5

    def arrive(self, target):
        desired = target - self.position
        d = desired.length()

        if d < 3:
            self.position = Vector2(target)
            self.velocity = Vector2(0, 0)
            self.acceleration = Vector2(0, 0)
            return

        braking_distance = self.velocity.length_squared() / (2 * self.maxforce)
        slow_radius = max(50, braking_distance * 1.2)   # 20% safety margin

        # Desired speed shrinks
        if d < slow_radius:
            speed = self.maxspeed * d / slow_radius
        else:
            speed = self.maxspeed
        speed = min(speed, d)   # never ask for a step bigger than the remaining distance

        if d > 0:
            desired = desired.normalize() * speed
        else:
            desired = Vector2(0, 0)

        steer = desired - self.velocity
        if steer.length() > self.maxforce:
            steer = steer.normalize() * self.maxforce

        self.apply_force(steer)

    def apply_force(self, force):
        self.acceleration += force * 0.7

    def show(self, surface):
        if self.velocity.length_squared() > 0.001:
            self.angle = math.atan2(self.velocity.y, self.velocity.x)

        vertices = [Vector2(self.r * 2, 0),
                    Vector2(-self.r * 2, -self.r),
                    Vector2(-self.r * 2, self.r)]

        points = [self.position + v.rotate_rad(self.angle) for v in vertices]

        pygame.draw.polygon(surface, (127, 127, 127), points)
        pygame.draw.polygon(surface, (0, 0, 0), points, 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Example 5.2 AND 5.3")
    clock = pygame.time.Clock()
 
    vehicle = Vehicle(WIDTH // 2, HEIGHT // 2)

    location = Vector2(vehicle.position.x, vehicle.position.y) 
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
 
        screen.fill((255, 255, 255))

        vehicle.arrive(location)
 
        vehicle.update()
        vehicle.show(screen)
        pygame.draw.circle(screen, (255, 0, 0), (int(location.x), int(location.y)), 5)
 
        pygame.display.flip()
        clock.tick(FPS)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()