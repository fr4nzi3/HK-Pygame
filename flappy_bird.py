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

# Resize the ground image to your desired dimensions
desired_ground_width = 564  # Adjust this according to your desired width
desired_ground_height = 535  # Adjust this according to your desired height
ground_img = pygame.transform.scale(ground_img, (desired_ground_width, desired_ground_height))

run = True
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg, (0, 0))

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
