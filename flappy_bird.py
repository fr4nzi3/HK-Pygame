import pygame
import random
import os

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
stop_scroll = True  # Set stop_scroll to True initially

# Set up directories
current_dir = os.path.dirname(__file__)
img_dir = os.path.join(current_dir, 'img')

#load images
bg = pygame.image.load(os.path.join(img_dir, 'bg.png')).convert_alpha()
ground_img = pygame.image.load(os.path.join(img_dir, 'ground.png')).convert_alpha()
pipe_img = pygame.image.load(os.path.join(img_dir, 'pipe.png')).convert_alpha()

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(os.path.join(img_dir, f'bird{num}.png')).convert_alpha()
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
        self.shake = 0  # Shake effect counter
        self.shake_offset = 5  # Shake offset amount

    def update(self):
        global flying, game_over, ground_scroll, stop_scroll
        if flying:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < screen_height:
                self.rect.y += int(self.vel)

            if not game_over:
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

        # Apply shake effect when game over
        if game_over:
            if self.shake > 0:
                self.rect.x += random.choice([-1, 1]) * self.shake_offset
                self.rect.y += random.choice([-1, 1]) * self.shake_offset
                self.shake -= 1
            else:
                self.shake = 0

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, top=True):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pipe_img, (100, 500))
        self.rect = self.image.get_rect()
        if top:
            self.rect.bottomleft = (x, y)  # Adjusting the position for the top pipe
        else:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.topleft = (x, y)  # Adjusting the position for the bottom pipe

    def update(self):
        global scroll_speed, stop_scroll
        if not stop_scroll:  # Only update position if scrolling is not stopped
            self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# Resize the ground image to your desired dimensions
desired_ground_width = 564  # Adjust this according to your desired width
desired_ground_height = 535  # Adjust this according to your desired height
ground_img = pygame.transform.scale(ground_img, (desired_ground_width, desired_ground_height))

pipe_group = pygame.sprite.Group()

# Function to generate pipes
def generate_pipes():
    global pipe_group
    if len(pipe_group) == 0 or pipe_group.sprites()[-1].rect.right < screen_width - 300:
        gap = 200  # Fixed vertical gap between pipes
        pipe_center = random.randint(gap, screen_height - gap)  # Randomize the center of the gap
        top_pipe_y = pipe_center - gap // 2
        bottom_pipe_y = pipe_center + gap // 2
        bottom_pipe = Pipe(screen_width, bottom_pipe_y, False)
        top_pipe = Pipe(screen_width, top_pipe_y, True)
        pipe_group.add(bottom_pipe)
        pipe_group.add(top_pipe)

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

    # check if player clicked to fly, then start scrolling pipes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True
            stop_scroll = False  # Set stop_scroll to False when player clicks to fly

    if not stop_scroll:  # Only generate and scroll pipes if stop_scroll is False
        # generate and scroll pipes
        generate_pipes()
        pipe_group.draw(screen)
        pipe_group.update()

        # check if bird has hit the ground or pipes
        if flappy.rect.bottom >= screen_height or pygame.sprite.spritecollide(flappy, pipe_group, False):
            game_over = True
            flying = False
            stop_scroll = True  # Stop scrolling when collision occurs
            flappy.shake = 10  # Start the shake effect when collision occurs
            # Remove the bird and pipes from their sprite groups
            bird_group.remove(flappy)
            pipe_group.empty()

    # Handle events and update the display
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
                    pipe_group.empty()
                    stop_scroll = False  # Reset scroll flag
        elif event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    if not game_over:
        # check if bird has hit the ground
        if flappy.rect.bottom > screen_height:
            game_over = True
            flying = False
            stop_scroll = True  # Stop scrolling when bird hits the ground

        # draw and scroll the ground
        ground_scroll -= scroll_speed
        if ground_scroll <= -ground_img.get_width():
            ground_scroll = 0

    pygame.display.update()

pygame.quit()
