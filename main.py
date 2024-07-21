import pygame, sys
import random
from pygame import mixer
import time



size = width, height = 1280,720
screen = pygame.display.set_mode(size)


LIGHT_BLUE = (51, 153, 255)
RED = (240, 20, 20)
GOLD = (255, 205, 0)
OCEAN_BLUE = (51, 153, 255)


pygame.init()
mixer.init()
sound = pygame.mixer.Sound("assets/sounds/612116__scriptel__tactic.mp3")
sound.set_volume(1)
sound.play()


eat_sfx = pygame.mixer.Sound("assets/sounds/457475__princessemilu__open-mouth-chomp.wav")
eat_sfx.set_volume(1.5)


death_sfx = pygame.mixer.Sound("assets/sounds/220634__albertrella__scream.wav")
death_sfx.set_volume(1.5)


clock = pygame.time.Clock()


ocean_background = pygame.image.load("assets/images/background.png")
background_width, background_height = 1280, 720
ocean_background = pygame.transform.scale(ocean_background, (background_width, background_height))
background_rect = ocean_background.get_rect()


player_image = pygame.image.load("assets/images/fish.png")
player_width, player_height = 80, 60
player_image = pygame.transform.scale(player_image, (player_width, player_height))
player_rect = player_image.get_rect()


minnow_image = pygame.image.load("assets/images/pixel-art-shrimp-seafood-sticker-u635a-x450.png")
minnow_width, minnow_height = 40, 30
minnow_image = pygame.transform.scale(minnow_image, (minnow_width, minnow_height))
minnow_rect = minnow_image.get_rect()


shark_image = pygame.image.load("assets/images/shark.png")
shark_width, shark_height = 180, 140
shark_image = pygame.transform.scale(shark_image, (shark_width, shark_height))
shark_rect = shark_image.get_rect()


font = pygame.font.Font(None, 90)
white = (255, 255, 255)
black = (0, 0, 0)
RED = (240, 20, 20)
GREEN = (40, 230, 20)


lose_msg = font.render("YOU LOSE!", True, RED)
lose_rect = lose_msg.get_rect()
lose_rect.center = (width // 2, height // 2)






running = True


collision_count = 0
coin_count = 0


pygame.mouse.set_pos(5, height/2)
pygame.mouse.set_visible(False)


player_rect.center = (width // 2, height //2)


puffer_speed = 10
collision_occurred = False
collision_timer = 0
food_counter = 0
food_font = pygame.font.Font(None, 1)


intro_font = pygame.font.Font(None, 150)
play_button_font = pygame.font.Font(None, 48)
instruction_font = pygame.font.Font(None, 24)




def show_intro_screen():
    intro_text = intro_font.render("Welcome to Fishgario!", True, white)
    play_button_text = play_button_font.render("Play Game", True, GREEN)
    instruction_text1 = instruction_font.render("Eat the Srimp, avoid the Shark!", True, RED)
    instruction_text2 = instruction_font.render("Click 'Play Game' to start.", True, RED)


    intro_rect = intro_text.get_rect(center=(width // 2, height // 2 - 100))
    instruction_rect1 = instruction_text1.get_rect(center=(width // 2, height // 2 - 35))
    instruction_rect2 = instruction_text2.get_rect(center=(width // 2, height // 2 - 15))
    play_button_rect = play_button_text.get_rect(center=(width // 2, height // 2 + 50))


    pygame.mouse.set_visible(True)


    screen.fill(black)
    screen.blit(intro_text, intro_rect)
    screen.blit(instruction_text1, instruction_rect1)
    screen.blit(instruction_text2, instruction_rect2)
    pygame.draw.rect(screen, RED, play_button_rect, 0)
    screen.blit(play_button_text, play_button_rect)


    pygame.display.flip()


    # Wait for the player to click the "Play Game" button
    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    waiting_for_click = False




def game_loop():
    global running, food_counter, puffer_speed


    pygame.mouse.set_visible(False)


    collision_occurred = False
    collision_timer = 0
    coin_count = 0


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False


        screen.blit(ocean_background, background_rect)


        screen.blit(player_image, player_rect)
        # pygame.draw.rect(screen, RED, obstacle_top)
        # pygame.draw.rect(screen, RED, obstacle_bottom)
        screen.blit(minnow_image, minnow_rect)
        screen.blit(shark_image, shark_rect)


        minnow_rect.centerx += random.randint(-15, 15)
        minnow_rect.centery += random.randint(-15, 15)


        minnow_rect.centerx = max(minnow_rect.centerx, 0)
        minnow_rect.centery = max(minnow_rect.centery, 0)
        minnow_rect.centerx = min(minnow_rect.centerx, width)
        minnow_rect.centery = min(minnow_rect.centery, height)


        """puffer_rect.centerx += random.randint(-20, 20)
        puffer_rect.centery += random.randint(-20, 20)"""


        shark_rect.centerx = max(shark_rect.centerx, 0)
        shark_rect.centery = max(shark_rect.centery, 0)
        shark_rect.centerx = min(shark_rect.centerx, width)
        shark_rect.centery = min(shark_rect.centery, height)


        """for obstacle in obstacles_list:
            if player_rect.colliderect(obstacle):
                pygame.mouse.set_pos(5, height/2)
                collision_count += 1
                if collision_count == 10:
                    running = False"""
       
        counter_text = font.render(f"Fish Eaten: {food_counter}", True, RED)
        screen.blit(counter_text, (10, 10))


        if player_rect.colliderect(minnow_rect):
            eat_sfx.play()
            coin_count += 1
            food_counter += 1
            minnow_rect.centerx = random.randint(25, width - 25)
            minnow_rect.centery = random.randint(25, height - 25)
            if coin_count == 100:
                print("YOU WON!")
                running = False
            puffer_speed += 2


        shark_rect.centerx += random.randint(-puffer_speed, puffer_speed)
        shark_rect.centery += random.randint(-puffer_speed, puffer_speed)


    # WHen you eat a fish, the puffer fish gets faster




        if player_rect.colliderect(shark_rect):
            death_sfx.play()
            print("YOU LOST!!!")
            collision_occurred = True
            collision_timer = pygame.time.get_ticks()  # Record the time of collision


        if collision_occurred:
            elapsed_time = pygame.time.get_ticks() - collision_timer
            if elapsed_time < 2500:  # Display "YOU LOSE" for 3 seconds
                screen.fill(black)
                screen.blit(lose_msg, lose_rect)
            else:
                running = False


        """if player_rect.colliderect(shark_rect):


            print("YOU LOST!!!")
            screen.fill(black)
            screen.blit(lose_msg, lose_rect)
            time.sleep(5)
            running = False"""
           




        player_rect.center = pygame.mouse.get_pos()




        pygame.display.flip()


        clock.tick(60)


# Show intro screen
show_intro_screen()


# Start the game loop after the intro screen
game_loop()


# Clean up
pygame.quit()
sys.exit()