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
flying = False
game_over = False

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
        self.vel = 0
        self.clicked = False

    def update(self):
        global flying, game_over, ground_scroll
        if flying:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            print(self.vel)
            if self.rect.bottom < screen_height:
                self.rect.y += int(self.vel)

            if game_over == False:
                # jump
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    self.vel = -10
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

                # handle the animation
                self.counter += 1
                flap_cooldown = 10  # Adjust the flap cooldown value as needed

                if self.counter > flap_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images):
                        self.index = 0
                self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            if self.rect.bottom >= screen_height:
                # Rotate the bird to face -90 degrees when it hits the ground
                self.image = pygame.transform.rotate(self.images[self.index], -90)
                game_over = True
            else:
                # Stop the animation when not flying
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

    # draw background
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()

    # draw the ground
    screen.blit(ground_img, (ground_scroll, screen_height - ground_img.get_height()))
    screen.blit(ground_img, (ground_scroll + ground_img.get_width(), screen_height - ground_img.get_height()))

    # check if bird has hit the ground
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False

    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    flappy.vel = -10  # Set velocity upwards when space is pressed
                else:
                    # Restart the game if space is pressed and the game is over
                    flappy.rect.y = int(screen_height / 2)
                    flappy.vel = 0
                    game_over = False
                    ground_scroll = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    if not game_over:
        # check if bird has hit the ground
        if flappy.rect.bottom > screen_height:
            flying = False

        # draw and scroll the ground
        ground_scroll -= scroll_speed
        if ground_scroll <= -ground_img.get_width():
            ground_scroll = 0

    pygame.display.update()

pygame.quit()
