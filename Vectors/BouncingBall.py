import random
import pygame
 
 
WIDTH, HEIGHT = 640, 240
BACKGROUND = (255, 255, 255)
STROKE_COLOR = (0, 0, 0)
FILL_COLOR = (127, 127, 127)
CIRCLE_DIAMETER = 48


class Walker:
    def __init__(self):
        self.position = pygame.Vector2(
            random.randint(CIRCLE_DIAMETER // 2, WIDTH - CIRCLE_DIAMETER // 2),
            random.randint(CIRCLE_DIAMETER // 2, HEIGHT - CIRCLE_DIAMETER // 2)
        )
        self.dir= pygame.Vector2(
            random.choice([-1, 1]),
            random.choice([-1, 1])
        )

    def step(self):
        self.position.x += self.dir.x * 2
        self.position.y += self.dir.y * 2
 
        # Rebotar en los bordes
        if self.position.x < CIRCLE_DIAMETER / 2 or self.position.x > WIDTH - CIRCLE_DIAMETER / 2:
            self.dir.x *= -1
        if self.position.y < CIRCLE_DIAMETER / 2 or self.position.y > HEIGHT - CIRCLE_DIAMETER / 2:
            self.dir.y *= -1

    def show(self, surface):
        pygame.draw.circle(
            surface, FILL_COLOR, (int(self.position.x), int(self.position.y)), CIRCLE_DIAMETER // 2
        )
        pygame.draw.circle(
            surface, STROKE_COLOR, (int(self.position.x), int(self.position.y)), CIRCLE_DIAMETER // 2, 2
        )


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball")
    clock = pygame.time.Clock()
    screen.fill(BACKGROUND)

    walker = Walker()

    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    screen.fill(BACKGROUND)
                    walker = Walker()
                if event.key == pygame.K_SPACE:
                    paused = not paused
        if not paused:  
            screen.fill(BACKGROUND)
            walker.step()
            walker.show(screen)
    
            pygame.display.flip()
            clock.tick(60)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()