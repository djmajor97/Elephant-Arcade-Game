# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 1000
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
        self.image = pygame.image.load(path.join(img_dir, 'elephant.png'))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: self.rect.y -= 4
        if pressed[pygame.K_DOWN]: self.rect.y += 4
        if pressed[pygame.K_LEFT]:
            self.image = pygame.image.load(path.join(img_dir, 'elephant_left.png'))
            self.rect.x -= 4
        if pressed[pygame.K_RIGHT]:
            self.image = pygame.image.load(path.join(img_dir, 'elephant.png'))
            self.rect.x += 4

        if self.rect.x > WIDTH - ELEPHANT_WIDTH:
            self.rect.x = WIDTH - ELEPHANT_WIDTH
        if self.rect.y > HEIGHT - ELEPHANT_HEIGHT:
            self.rect.y = HEIGHT - ELEPHANT_HEIGHT
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0

    def shoot(self):
        water = Water(self.rect.right, self.rect.centery)
        all_sprites.add(water)
        waters.add(water)

class Catcher(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, 'catcher.png'))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH+50, WIDTH+100)
        self.rect.y = random.randrange(0, HEIGHT - self.rect.width)
        self.speedy = random.randrange(2, 10)

    def update(self):
        self.rect.x -= self.speedy
        if self.rect.x < -50:
            self.rect.x = random.randrange(WIDTH+50, WIDTH+100)
            self.rect.y = random.randrange(HEIGHT - self.rect.width)
            self.speedy = random.randrange(2, 10)

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, 'mouse.png'))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(100, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, 'water.png'))
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (50, 73))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.speedy = 10

    def update(self):
        self.rect.x += self.speedy
        if self.rect.left > WIDTH -100:
            self.kill()

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

background = pygame.image.load(path.join(img_dir, 'grass_background.jpg')).convert()
background_rect = background.get_rect()

# Sprites
all_sprites = pygame.sprite.Group()
elephant = Elephant()
all_sprites.add(elephant)

mice = pygame.sprite.Group()
for i in range(10):
    mouse = Mouse()
    all_sprites.add(mouse)
    mice.add(mouse)

catchers = pygame.sprite.Group()
for i in range(6):
    catcher = Catcher()
    all_sprites.add(catcher)
    catchers.add(catcher)

waters = pygame.sprite.Group()


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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                elephant.shoot()

    # Update
    all_sprites.update()

    # Check to see if water hit a catcher
    hits = pygame.sprite.groupcollide(waters, catchers, True, True)
    for hit in hits:
        catcher = Catcher()
        all_sprites.add(catcher)
        catchers.add(catcher)

    # check to see if a mob hit the player
    hitsE = pygame.sprite.spritecollide(elephant, mice, False)
    hitsC = pygame.sprite.spritecollide(elephant, catchers, False)
    if hitsE or hitsC:
        running = False

    # Draw / render
    screen.fill(WHITE)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()