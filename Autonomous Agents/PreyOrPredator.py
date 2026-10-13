import random
import pygame
import math
from pygame.math import Vector2

 
WIDTH, HEIGHT = 640, 480
FPS = 60

G= 1.0 #Gravitational constant

class Animal():
    def __init__(self, x, y):
        self.position= Vector2(x, y)
        speed= 3.5
        self.velocity = Vector2(random.uniform(-speed, speed), random.uniform(-speed, speed))

    def detect_edges(self):
            if self.position.x <= 0 or self.position.x >= WIDTH or self.position.y <= 0 or self.position.y >= HEIGHT:
                return True
            return False

    def detect_colision(self, hunter):
            distance = (self.position - hunter.position).length()
            if distance < 8 + hunter.r:
                return True
            return False

class Prey(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)
        type= 0 #prey type

    def show(self, surface):
        center = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(surface, (127, 127, 127), center, 8)
        pygame.draw.circle(surface, (0, 0, 0), center, 8, 1)

    def detect_colision(self, hunter):
        distance = (self.position - hunter.position).length()
        if distance < 8 + hunter.r:
            return True
        return False

    def update(self):
        self.position += self.velocity

class Predator(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)
        type= 1 #predator type

    def show(self, surface):
            center = (int(self.position.x), int(self.position.y))
            pygame.draw.polygon(surface, (127, 127, 127), [(center[0], center[1] - 8), (center[0] - 8, center[1] + 8), (center[0] + 8, center[1] + 8)])
            pygame.draw.polygon(surface, (0, 0, 0), [(center[0], center[1] - 8), (center[0] - 8, center[1] + 8), (center[0] + 8, center[1] + 8)], 1)
    
    def detect_colision(self, hunter):
        distance = (self.position - hunter.position).length()
        if distance < 8 + hunter.r:
            return True
        return False
    
    def update(self):
        self.position += self.velocity

class Hunter: 
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

    def seek(self, target):
        if isinstance(target, Prey):
            self.hunt(target)
        elif isinstance(target, Predator):
            self.avoid(target)
            
    def hunt(self, target):
        desired = target.position - self.position
        desired = desired.normalize() * self.maxspeed
        steer = desired - self.velocity
        if steer.length() > self.maxforce:
            steer= steer.normalize() * self.maxforce
        self.apply_force(steer)

    def avoid(self, target, danger_radius=120):
        predator_future_pos = target.position + target.velocity * 20
        away = self.position - predator_future_pos
        distance = away.length()

        if 0 < distance < danger_radius:
            desired = away.normalize() * self.maxspeed
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
    pygame.display.set_caption("Exercise 5.2 AND 5.3")
    clock = pygame.time.Clock()
 
    animal = Prey(int(random.uniform(0, WIDTH)),  int(random.uniform(0, HEIGHT)))
    hunter = Hunter(WIDTH // 2, HEIGHT // 2)
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                hunter = Hunter(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
                if(random.random() < 0.65):
                    animal = Prey(int(random.uniform(1, WIDTH - 1)),  int(random.uniform(1, HEIGHT - 1)))
                else:
                    animal = Predator(int(random.uniform(1, WIDTH - 1)),  int(random.uniform(1, HEIGHT - 1)))
 
        screen.fill((255, 255, 255))

        if(animal.detect_edges() or animal.detect_colision(hunter)):
            if(random.random() < 0.8):
                animal = Prey(int(random.uniform(1, WIDTH - 1)),  int(random.uniform(1, HEIGHT - 1)))
            else:
                animal = Predator(int(random.uniform(1, WIDTH - 1)),  int(random.uniform(1, HEIGHT - 1)))

        hunter.seek(animal)
 
        hunter.update()
        animal.update()
        hunter.show(screen)
        animal.show(screen)
 
        pygame.display.flip()
        clock.tick(FPS)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()