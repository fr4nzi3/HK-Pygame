import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 564
screen_height = 535

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define game variables
ground_scroll = 0
scroll_speed = 2

#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        # Resize the bird image to your desired dimensions
        desired_bird_width = 50  # Adjust this according to your desired width
        desired_bird_height = 40  # Adjust this according to your desired height
        self.images = [pygame.transform.scale(img, (desired_bird_width, desired_bird_height)) for img in self.images]
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        # handle the animation
        self.counter += 1
        flap_cooldown = 10  # Adjust the flap cooldown value as needed

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# Resize the ground image to your desired dimensions
desired_ground_width = 564  # Adjust this according to your desired width
desired_ground_height = 535  # Adjust this according to your desired height
ground_img = pygame.transform.scale(ground_img, (desired_ground_width, desired_ground_height))

run = True
while run:
    clock.tick(fps)

    #draw background
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()

    #draw and scroll the ground
    screen.blit(ground_img, (ground_scroll, screen_height - ground_img.get_height()))
    screen.blit(ground_img, (ground_scroll + ground_img.get_width(), screen_height - ground_img.get_height()))
    ground_scroll -= scroll_speed
    if ground_scroll < -ground_img.get_width():
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
