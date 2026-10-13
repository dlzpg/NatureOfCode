import random
import math
import pygame
from pygame.math import Vector2

WIDTH, HEIGHT = 640, 480
FPS = 60


class Path:
    def __init__(self):
        self.start = Vector2(0, random.randint(0, HEIGHT))
        self.end = Vector2(WIDTH, random.randint(0, HEIGHT))
        self.radius = 20    

    def show(self, surface):
        pygame.draw.line(surface, (200, 200, 200), self.start, self.end, self.radius * 2)
        pygame.draw.line(surface, (0, 0, 0), self.start, self.end, 1)

class Vehicle:
    def __init__(self, x, y, maxspeed=4, maxforce=0.1):
        self.position = Vector2(x, y)
        self.velocity = Vector2(maxspeed, 0)
        self.acceleration = Vector2(0, 0)
        self.maxspeed = maxspeed
        self.maxforce = maxforce
        self.r = 4
        self.angle = 0

        # Datos para el modo debug
        self.future = Vector2(x, y)
        self.normal = Vector2(x, y)
        self.target = Vector2(x, y)

    def apply_force(self, force):
        self.acceleration += force

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > self.maxspeed:
            self.velocity = self.velocity.normalize() * self.maxspeed
        self.position += self.velocity
        self.acceleration *= 0   # se reinicia cada frame

    def seek(self, target):
        desired = target - self.position
        if desired.length() == 0:
            return
        desired = desired.normalize() * self.maxspeed

        steer = desired - self.velocity
        if steer.length() > self.maxforce:
            steer = steer.normalize() * self.maxforce
        self.apply_force(steer)

    def follow(self, path):
        if self.velocity.length() > 0:
            predict = self.velocity.normalize() * 25
        else:
            predict = Vector2(0, 0)
        self.future = self.position + predict

        self.normal = get_normal_point(self.future, path.start, path.end)

        direction = (path.end - path.start).normalize() * 25
        self.target = self.normal + direction

        distance = self.future.distance_to(self.normal)
        if distance > path.radius:
            self.seek(self.target)

    def borders(self, path):
        if self.position.x > path.end.x + self.r:
            self.position.x = path.start.x - self.r
            self.position.y = path.start.y + (self.position.y - path.end.y)
            self.position.y = max(0, min(HEIGHT, self.position.y))

    def show(self, surface):
        if self.velocity.length_squared() > 0.001:
            self.angle = math.atan2(self.velocity.y, self.velocity.x)

        vertices = [Vector2(self.r * 2, 0),
                    Vector2(-self.r * 2, -self.r),
                    Vector2(-self.r * 2, self.r)]
        points = [self.position + v.rotate_rad(self.angle) for v in vertices]

        pygame.draw.polygon(surface, (127, 127, 127), points)
        pygame.draw.polygon(surface, (0, 0, 0), points, 1)

    def show_debug(self, surface):
        pygame.draw.line(surface, (0, 0, 0), self.position, self.future, 1)
        pygame.draw.circle(surface, (0, 0, 0), self.future, 4)
        pygame.draw.line(surface, (0, 0, 0), self.future, self.normal, 1)
        pygame.draw.circle(surface, (0, 0, 0), self.normal, 4)
        #rojo si el vehículo se está saliendo del camino
        pygame.draw.circle(surface, (255, 0, 0), self.target, 6)

def get_normal_point(p, a, b):
    ap = p - a
    ab = (b - a).normalize()
    ab *= ap.dot(ab)          # longitud de la proyección sobre la dirección
    return a + ab


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Example 5.6: Simple Path Following")
    clock = pygame.time.Clock()

    path = Path()
    vehicle = Vehicle(0, path.start.y + 30)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    path = Path()
                    vehicle = Vehicle(0, random.randint(0, HEIGHT))
                elif event.key == pygame.K_d:
                    debug = not debug

        screen.fill((255, 255, 255))

        path.show(screen)

        vehicle.follow(path)
        vehicle.update()
        vehicle.borders(path)
        vehicle.show(screen)
        vehicle.show_debug(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()