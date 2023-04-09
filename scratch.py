import pygame
from sys import exit
from random import randint
import math
import time


def display_score():
    current_time = int((pygame.time.get_ticks() / 200)) - start_time
    score_surf = test_font.render(f'Score -- {current_time}', False, "Black")
    score_rect = score_surf.get_rect(center=(60, 10))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= rand_speed
            if obstacle_rect.bottom == 691:
                screen.blit(nme_carOne_surf, obstacle_rect)
            else:
                screen.blit(nme_carTwo_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -50]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def car_animation():
    global car_surf, car_index
    car_index += .3
    if car_index >= len(car_drive):
        car_index = 0
    car_surf = car_drive[int(car_index)]


def enemy_one_animation():
    global nme_carOne_surf, nme_carOne_frame_index
    nme_carOne_frame_index += .3
    if nme_carOne_frame_index >= len(nme_car_one_frames):
        nme_carOne_frame_index = 0
    nme_carOne_surf = nme_car_one_frames[int(nme_carOne_frame_index)]


def enemy_two_animation():
    global nme_carTwo_surf, nme_carTwo_frame_index
    nme_carTwo_frame_index += .3
    if nme_carTwo_frame_index >= len(nme_car_two_frames):
        nme_carTwo_frame_index = 0
    nme_carTwo_surf = nme_car_two_frames[int(nme_carTwo_frame_index)]


# Main Variables
pygame.init()
pygame.display.set_caption('Floor It!')
clock = pygame.time.Clock()
test_font = pygame.font.Font("Assets/karmatic-arcade/ka1.ttf", 16)  # (Font Type, Font Size(int))
game_active = False
start_time = 0
score = 0

clock = pygame.time.Clock()
FPS = 60
DEFAULT_IMAGE_SIZE = (1200, 701)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 701

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Floor It!")

# load image
bg = pygame.image.load("Assets/scrollingbg.png").convert_alpha()
bg_width = bg.get_width()
bg_rect = bg.get_rect()
menu_bg = pygame.image.load('Assets/background_0.png').convert_alpha()
menu_bg = pygame.transform.scale(menu_bg, DEFAULT_IMAGE_SIZE)

menu_fg = pygame.image.load('Assets/background_1.png')
menu_fg = pygame.transform.scale(menu_fg, DEFAULT_IMAGE_SIZE)

# define game variables
scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
car_resize = (180, 58)

# TEXT SURFACES
title_surface = test_font.render("Floor It!", False, "Black")  # (Name, Anti-Alias, Color)
title_rect = title_surface.get_rect(center=(275, 20))

prompt_surface = test_font.render("Press space bar to play", False, "Black")  # (Name, Anti-Alias, Color)
prompt_rect = prompt_surface.get_rect(center=(275, 340))

# INTERACTABLE SURFACES
car_idle = pygame.image.load("Assets/cityassets/2DPixelCars/playeridle.png").convert_alpha()
car_driveOne = pygame.image.load("Assets/cityassets/2DPixelCars/playerdrive1.png").convert_alpha()
car_driveTwo = pygame.image.load("Assets/cityassets/2DPixelCars/playerdrive2.png").convert_alpha()
car_driveThree = pygame.image.load("Assets/cityassets/2DPixelCars/playerdrive3.png").convert_alpha()
car_drive = [car_driveOne, car_driveTwo, car_driveThree]
car_index = 0
car_surf = car_drive[car_index]

car_rect = car_idle.get_rect(center=(20, 360))
menu_car = pygame.transform.scale(car_idle, car_resize)
menu_car_rect = menu_car.get_rect(center=(275, 520))

# Obstacles!
car_rect_list = []
nme_car_two = pygame.image.load("Assets/cityassets/2DPixelCars/nmecar4.png").convert_alpha()
nme_car_two_frame_2 = pygame.image.load("Assets/cityassets/2DPixelCars/nmecar5.png").convert_alpha()
nme_car_two_frame_3 = pygame.image.load("Assets/cityassets/2DPixelCars/nmecar6.png").convert_alpha()
nme_car_two_frames = [nme_car_two, nme_car_two_frame_2, nme_car_two_frame_3]
nme_carTwo_frame_index = 0
nme_carTwo_surf = nme_car_two_frames[nme_carTwo_frame_index]

nme_car_one = pygame.image.load("Assets/cityassets/2DPixelCars/nmecar1.png").convert_alpha()
nme_car_one_frame_1 = pygame.image.load("Assets/cityassets/2DPixelCars/nmecar2.png").convert_alpha()
nme_car_one_frame_2 = pygame.image.load("Assets/cityassets/2DPixelCars/nmecar3.png").convert_alpha()
nme_car_one_frames = [nme_car_one, nme_car_one_frame_1, nme_car_one_frame_2]
nme_carOne_frame_index = 0
nme_carOne_surf = nme_car_one_frames[nme_carOne_frame_index]

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

carOne_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(carOne_animation_timer, 500)

carTwo_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(carTwo_animation_timer, 500)

# MAIN GAME LOOP
while True:
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))
        # bg_rect.x = i * bg_width + scroll
        # pygame.draw.rect(screen, (255, 0, 0), bg_rect, 1)

    # scroll background
    scroll -= 4

    # reset scroll
    if abs(scroll) > bg_width:
        scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 200)
                car_rect.left = 100
        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    car_rect_list.append(nme_car_one.get_rect(bottomright=(randint(1200, 1400), 691)))
                    rand_speed = randint(6, 14)
                else:
                    car_rect_list.append(nme_car_two.get_rect(bottomright=(randint(1200, 1400), 650)))
                    rand_speed = randint(6, 14)

    if game_active:
        # Actual Game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            car_rect.x += 4
        if keys[pygame.K_a]:
            car_rect.x -= 2
        if keys[pygame.K_s]:
            car_rect.y += 3
        if keys[pygame.K_w]:
            car_rect.y -= 3
        # Road Boundaries
        if car_rect.bottom >= 700:
            car_rect.bottom = 700
        if car_rect.bottom <= 632:
            car_rect.bottom = 632
        # Collisions
        game_active = collisions(car_rect, car_rect_list)

        score = display_score()

        # Obstacle Movement
        car_rect_list = obstacle_movement(car_rect_list)
        enemy_one_animation()
        enemy_two_animation()
        car_animation()
        screen.blit(car_surf, car_rect)


    # Menu Screen
    else:
        screen.blit(menu_bg, (0, 0))  # (x,y) (0,0) starts at top left
        screen.blit(menu_car, menu_car_rect)
        menu_car_rect.x += 7
        if menu_car_rect.left >= 1200:
            menu_car_rect.right = 0
        screen.blit(menu_fg, (0, 0))
        score_message = test_font.render(f'Your score-{score}', False, "Black")
        score_message_rect = score_message.get_rect(center=(600, 310))
        car_rect_list.clear()
        # car_rect.center = (20, 460)

        if score == 0:
            screen.blit(title_surface, title_rect)
            screen.blit(prompt_surface, prompt_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(FPS)  # while loop should not run more than 60 times per second
