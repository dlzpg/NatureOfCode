import math
import pygame
from pygame.math import Vector2
 
WIDTH, HEIGHT = 640, 240
FPS = 60
 
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Exercise 3.1")
    clock = pygame.time.Clock()
 
    angle = 0.0
    paused = False
    center = Vector2(WIDTH / 2, HEIGHT / 2)
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    angle = 0.0
 
        screen.fill((255, 255, 255))
 
        # Baton endpoints in local space: (-60, 0) and (60, 0)
        # rotate(angle): rotate around the origin (the baton's center)
        # translate: move to the center of the window
        a = Vector2(-60, 0).rotate_rad(angle) + center
        b = Vector2(60, 0).rotate_rad(angle) + center
 
        
        pygame.draw.line(screen, (0, 0, 0), a, b, 2)
        for end in (a, b):
            pos = (int(end.x), int(end.y))
            pygame.draw.circle(screen, (127, 127, 127), pos, 16)   
            pygame.draw.circle(screen, (0, 0, 0), pos, 16, 2)      
 
        if not paused:
            angle += 0.1
            angle %= math.tau
 
        pygame.display.flip()
        clock.tick(FPS)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()