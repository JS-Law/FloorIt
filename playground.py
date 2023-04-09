import pygame
import math
from random import randint


def car_animation():
    global car_surf, car_index
    car_index += .3
    if car_index >= len(car_drive):
        car_index = 0
    car_surf = car_drive[int(car_index)]

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= rand_speed
            if obstacle_rect.bottom == 346:
                screen.blit(nme_carOne_surf, obstacle_rect)
            else:
                screen.blit(nme_carTwo_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -50]

        return obstacle_list
    else:
        return []


def display_score():
    current_time = int((pygame.time.get_ticks() / 800)) - start_time
    score_surf = test_font.render(f'Score -- {current_time}', False, "Black")
    score_rect = score_surf.get_rect(center=(60, 10))
    screen.blit(score_surf, score_rect)
    return current_time


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 701

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Scroll")

# load image
bg = pygame.image.load("Assets/scrollingbg.png").convert_alpha()
bg_width = bg.get_width()
bg_rect = bg.get_rect()

# define game variables
scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

# game loop
run = True
while run:

    clock.tick(FPS)

    # draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))
        # bg_rect.x = i * bg_width + scroll
        # pygame.draw.rect(screen, (255, 0, 0), bg_rect, 1)

    # scroll background
    scroll -= 5

    # reset scroll
    if abs(scroll) > bg_width:
        scroll = 0

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
