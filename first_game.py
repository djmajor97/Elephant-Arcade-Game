import pygame
import random
from pygame.locals import *
import random, os.path

RANDOM_FACTOR = 2
MOUSE_WIDTH = 26
MOUSE_HEIGHT = 25
ELEPHANT_WIDTH = 71
ELEPHANT_HEIGHT = 58

class Mouse(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

def top_left_hit(y_m, y_e):
    if (y_m + MOUSE_HEIGHT > y_e) and y_m < y_e:
        return True

def bottom_left_hit(y_m, y_e):
    if (y_m + MOUSE_HEIGHT > y_e + ELEPHANT_HEIGHT) and y_m < y_e + ELEPHANT_HEIGHT:
        return True


def main():

    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    info = pygame.display.Info()
    WIDTH = info.current_w
    HEIGHT = info.current_h
    done = False
    is_blue = True
    elephant_x = 30
    elephant_y = 30
    mouses_x = []
    mouses_y = []
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()

    elephant_image = pygame.image.load('elephant.png')
    mouse_image = pygame.image.load('mouse.png')

    pygame.mixer.music.load('guitar.mp3')
    #pygame.mixer.music.play(-1)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_blue = not is_blue

        screen.fill((0, 0, 0))
        clock.tick(60)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: elephant_y -= 4
        if pressed[pygame.K_DOWN]: elephant_y += 4
        if pressed[pygame.K_LEFT]:
            elephant_image = pygame.image.load('elephant_left.png')
            elephant_x -= 4
        if pressed[pygame.K_RIGHT]:
            elephant_image = pygame.image.load('elephant.png')
            elephant_x += 4

        rand = random.randint(1, 100)
        if rand <= RANDOM_FACTOR:
            mouses_x.append(random.randint(0, WIDTH - MOUSE_WIDTH))
            mouses_y.append(0)
        for y in range(len(mouses_y)):
            if mouses_y[y] < HEIGHT + 2:
                mouses_y[y] += 1

        hit_effect = pygame.mixer.Sound('beep-03.wav')
        # Check for left collision
        for x in range(len(mouses_x)):
            if ((mouses_x[x]+MOUSE_WIDTH) > elephant_x and mouses_x[x] < elephant_x) \
                    and (top_left_hit(mouses_y[x], elephant_y) or bottom_left_hit(mouses_y[x], elephant_y)):
                hit_effect.play()


        effect = pygame.mixer.Sound('beep-03.wav')
        if elephant_x > WIDTH-71:
            elephant_x = WIDTH-71
            effect.play()
        if elephant_y > HEIGHT-58:
            elephant_y = HEIGHT-58
            effect.play()
        if elephant_x < 0:
            elephant_x = 0
            effect.play()
        if elephant_y < 0:
            elephant_y = 0
            effect.play()

        # Blit mice and elephant
        for i in range(len(mouses_y)):
            screen.blit(mouse_image, (mouses_x[i], mouses_y[i]))
        screen.blit(elephant_image, (elephant_x, elephant_y))

        pygame.display.flip()

#call the "main" function if running this script
if __name__ == '__main__': main()