import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int((pygame.time.get_ticks() / 800)) - start_time
    score_surf = test_font.render(f'Score -- {current_time}', False, "Black")
    score_rect = score_surf.get_rect(center=(60, 10))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= rand_speed
            if obstacle_rect.bottom == 346:
                screen.blit(car_two, obstacle_rect)
            else:
                screen.blit(car_three, obstacle_rect)

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


# Main Variables
pygame.init()
screen = pygame.display.set_mode((550, 367))  # (height, width) DISPLAY SURFACE
pygame.display.set_caption('Floor It!')
clock = pygame.time.Clock()
test_font = pygame.font.Font("Assets/karmatic-arcade/ka1.ttf", 16)  # (Font Type, Font Size(int))
game_active = False
start_time = 0
score = 0

# Image Sizing
building_resize = (160, 230)
DEFAULT_IMAGE_SIZE = (550, 367)
shrink = (10, 20)
car_resize = (180, 58)

# WORLD BOXES
skybox = pygame.image.load('Assets/country-platform-files/layers/country-platform-back.png').convert_alpha()
skybox = pygame.transform.scale(skybox, DEFAULT_IMAGE_SIZE)

menu_bg = pygame.image.load('Assets/background_0.png').convert_alpha()
menu_bg = pygame.transform.scale(menu_bg, DEFAULT_IMAGE_SIZE)

menu_fg = pygame.image.load('Assets/background_1.png')
menu_fg = pygame.transform.scale(menu_fg, DEFAULT_IMAGE_SIZE)
forest = pygame.image.load('Assets/country-platform-files/layers/country-platform-forest.png').convert_alpha()
forest = pygame.transform.scale(forest, DEFAULT_IMAGE_SIZE)

# BUILDINGS AND ROADS
building_one = pygame.image.load('Assets/cityassets/turfwars_buildingtiles01/restaurant01.png').convert_alpha()
building_one_rect = building_one.get_rect(bottomleft=(0, 367))

building_two = pygame.image.load('Assets/cityassets/turfwars_buildingtiles01/policestation01.png').convert_alpha()
building_two_rect = building_two.get_rect(bottomleft=(100, 367))

building_three = pygame.image.load('Assets/cityassets/turfwars_buildingtiles01/apartment03.png').convert_alpha()
building_three_rect = building_three.get_rect(bottomleft=(200, 367))

building_four = pygame.image.load('Assets/cityassets/turfwars_buildingtiles01/apartment02.png').convert_alpha()
building_four_rect = building_four.get_rect(bottomleft=(300, 367))

building_five = pygame.image.load('Assets/cityassets/turfwars_buildingtiles01/park01.png').convert_alpha()
building_five_rect = building_five.get_rect(bottomleft=(400, 367))

building_six = pygame.image.load('Assets/cityassets/turfwars_buildingtiles01/apartment04.png').convert_alpha()
building_six_rect = building_six.get_rect(bottomleft=(200, 367))

# HUMAN SURFACES
me = pygame.image.load('Assets/pxArt.png').convert_alpha()
me = pygame.transform.scale(me, shrink)
me_rect = me.get_rect(midbottom=(100, 325))

jesam_surf = pygame.image.load('Assets/jesam.png')
jesam_surf = pygame.transform.scale(jesam_surf, shrink)
jesam_rect = jesam_surf.get_rect(midbottom=(350, 225))

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
menu_car_rect = menu_car.get_rect(center=(275, 270))

# Obstacles!
car_rect_list = []
car_three = pygame.image.load("Assets/cityassets/2DPixelCars/Cars3 copy 2.png").convert_alpha()
car_two = pygame.image.load("Assets/cityassets/2DPixelCars/Cars2 copy.png").convert_alpha()
# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1900)

# MAIN GAME LOOP
while True:
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
                start_time = int(pygame.time.get_ticks() / 800)
                car_rect.left = 100
        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                car_rect_list.append(car_two.get_rect(bottomright=(randint(900, 1100), 360)))
                rand_speed = randint(1, 10)
            else:
                car_rect_list.append(car_three.get_rect(bottomright=(randint(900, 1100), 346)))
                rand_speed = randint(1, 6)
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
        if car_rect.bottom >= 366:
            car_rect.bottom = 366
        if car_rect.bottom <= 340:
            car_rect.bottom = 340
        # Collisions
        game_active = collisions(car_rect, car_rect_list)

        screen.blit(skybox, (0, 0))  # (x,y) (0,0) starts at top left
        screen.blit(forest, (0, 0))
        score = display_score()
        screen.blit(building_one, building_one_rect)
        screen.blit(building_two, (100, 199))
        screen.blit(building_three, (200, 196))
        screen.blit(building_four, (300, 215))
        screen.blit(building_five, (400, 239))
        screen.blit(building_six, (500, 206))
        screen.blit(me, me_rect)
        screen.blit(jesam_surf, jesam_rect)

        # Obstacle Movement
        car_rect_list = obstacle_movement(car_rect_list)

        car_animation()
        screen.blit(car_surf, car_rect)


    # Menu Screen
    else:
        screen.blit(menu_bg, (0, 0))  # (x,y) (0,0) starts at top left
        screen.blit(menu_car, menu_car_rect)
        menu_car_rect.x += 7
        if menu_car_rect.left >= 550:
            menu_car_rect.right = 0
        screen.blit(menu_fg, (0, 0))
        score_message = test_font.render(f'Your score-{score}', False, "Black")
        score_message_rect = score_message.get_rect(center=(275, 310))
        car_rect_list.clear()
        car_rect.center = (20, 360)

        if score == 0:
            screen.blit(title_surface, title_rect)
            screen.blit(prompt_surface, prompt_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)  # while loop should not run more than 60 times per second
