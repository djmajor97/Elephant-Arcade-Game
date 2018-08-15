# Pygame template - skeleton for a new pygame project
import pygame
import random

WIDTH = 480
HEIGHT = 600
FPS = 30

ELEPHANT_WIDTH = 71
ELEPHANT_HEIGHT = 58

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Elephant(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('elephant.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: self.rect.y -= 4
        if pressed[pygame.K_DOWN]: self.rect.y += 4
        if pressed[pygame.K_LEFT]:
            self.image = pygame.image.load('elephant_left.png')
            self.rect.x -= 4
        if pressed[pygame.K_RIGHT]:
            self.image = pygame.image.load('elephant.png')
            self.rect.x += 4

        if self.rect.x > WIDTH - ELEPHANT_WIDTH:
            self.rect.x = WIDTH - ELEPHANT_WIDTH
        if self.rect.y > HEIGHT - ELEPHANT_HEIGHT:
            self.rect.y = HEIGHT - ELEPHANT_HEIGHT
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Sprites
all_sprites = pygame.sprite.Group()
elephant = Elephant()
all_sprites.add(elephant)
for i in range(20):
    mouse= Mouse()
    all_sprites.add(mouse)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()