import pygame
from pygame.locals import *
import sys
import os
import traceback
import plane3 as plane
import enemy
import bullet
import supply
from enemy import *
##
import RPi.GPIO as GPIO
import time
import numpy as np 

##

# from scipy.spatial import distance as dist
# from imutils.video import VideoStream
# from imutils import face_utils
# from threading import Thread
# import numpy as np
# import argparse
# import imutils
# import time
# import dlib
# import cv2
##
import time
import board
import adafruit_bno055
import serial
import busio

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

##

GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.IN,pull_up_down = GPIO.PUD_UP)    
def GPIO22_callback(channel):
    global CODERUN  
    CODERUN = False
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)

##
def mouth_aspect_ratio(mouth):
	# compute the euclidean distances between the two sets of
	# vertical mouth landmarks (x, y)-coordinates
	A = dist.euclidean(mouth[2], mouth[10]) # 51, 59
	B = dist.euclidean(mouth[4], mouth[8]) # 53, 57

	# compute the euclidean distance between the horizontal
	# mouth landmark (x, y)-coordinates
	C = dist.euclidean(mouth[0], mouth[6]) # 49, 55

	# compute the mouth aspect ratio
	mar = (A + B) / (2.0 * C)

	# return the mouth aspect ratio
	return mar
##


# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.putenv('SDL_FBDEV', '/dev/fb1') # Display on PiTFT
# os.putenv('SDL_MOUSEDRV', 'TSLIB')
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

##
pygame.init()
pygame.mixer.init()

# pygame.mouse.set_visible(False)

#Set size parameters:
#bg_size=width,height=480,700
bg_size=width,height=320,240
screen=pygame.display.set_mode(bg_size)
pygame.display.set_caption("plane war")
icon=pygame.image.load("images/icon.ico").convert_alpha()
#Set the form icon
pygame.display.set_icon(icon)
#Load background image:
background=pygame.image.load("images/bg.png").convert()
game_start=pygame.image.load("images/game_start.png").convert_alpha()
#Loading game restart screen.
game_restart=pygame.image.load("images/game_restart.png").convert_alpha()
game_restart = pygame.transform.rotozoom(game_restart, 0, 0.8)
game_restart_rect=game_restart.get_rect()
game_restart_rect.left,game_restart_rect.top=40,20

#

game_quit=pygame.image.load("images/Quit.png").convert_alpha()
game_quit = pygame.transform.rotozoom(game_quit, 0, 0.5)
game_quit_rect=game_quit.get_rect()
game_quit_rect.left,game_quit_rect.right=width-game_quit_rect.width-260,100

#Loading game preparation screen.
game_loading1=pygame.image.load("images/game_loading1.png").convert_alpha()
game_loading2=pygame.image.load("images/game_loading2.png").convert_alpha()
game_loading3=pygame.image.load("images/game_loading3.png").convert_alpha()
game_loading_rect=game_loading1.get_rect()
#Loading game pause image.
game_stop=pygame.image.load("images/game_stop.png").convert_alpha()
game_stop_rect=game_stop.get_rect()
#Loading game end screen
game_over=pygame.image.load("images/game_over.png").convert()
# Load pause button picture
game_pause_nor = pygame.image.load("images/game_pause_nor.png").convert_alpha()
game_pause_pressed = pygame.image.load("images/game_pause_pressed.png").convert_alpha()
# Load continue key image
game_resume_nor = pygame.image.load("images/game_resume_nor.png").convert_alpha()
game_resume_pressed = pygame.image.load("images/game_resume_pressed.png").convert_alpha()
#tuichu

quit_rect = game_pause_nor.get_rect()
quit_rect.left, quit_rect.top = 10,10
# Pause button range value
paused_rect = game_pause_nor.get_rect()
paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
paused_image = game_pause_nor
resume_image = game_resume_nor
# Loading bomb pictures
bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
bomb_rect = bomb_image.get_rect()
bomb_font = pygame.font.Font("font/font.ttf",45)
bomb_num = 3
# Load Life Number Image
life_image = pygame.image.load("images/life.png").convert_alpha()
life_rect = life_image.get_rect()
life_num = 3

# Set music variables
bg_music = pygame.mixer.music
game_achievement_sound = pygame.mixer
game_over_sound = pygame.mixer
bullet_sound = pygame.mixer
enemy1_down_sound = pygame.mixer
enemy2_out_sound = pygame.mixer
enemy2_down_sound = pygame.mixer
enemy3_out_sound = pygame.mixer
enemy3_down_sound = pygame.mixer
pygame.mixer.set_num_channels(15)      # Setting the audio track channel
volume = 0.2

# Load game music, set volume
bg_music.load("music/game_music.mp3")
game_achievement_sound = game_achievement_sound.Sound("music/game_achievement.wav")
game_over_sound = game_over_sound.Sound("music/game_over.wav")
bullet_sound = bullet_sound.Sound("music/bullet.wav")
enemy1_down_sound = enemy1_down_sound.Sound("music/enemy1_down.wav")
enemy2_out_sound = enemy2_out_sound.Sound("music/enemy2_out.wav")
enemy2_down_sound = enemy2_down_sound.Sound("music/enemy2_down.wav")
enemy3_out_sound = enemy3_out_sound.Sound("music/enemy3_out.wav")
enemy3_down_sound = enemy3_down_sound.Sound("music/enemy3_down.wav")
bg_music.set_volume(volume)
game_achievement_sound.set_volume(volume)
game_over_sound.set_volume(volume)
bullet_sound.set_volume(volume)
enemy1_down_sound.set_volume(volume)
enemy2_out_sound.set_volume(volume)
enemy2_down_sound.set_volume(volume)
enemy3_out_sound.set_volume(volume)
enemy3_down_sound.set_volume(volume)

# Basic parameters
WHITE = (255,255,255)  # white
GREEN = (0, 255, 0)    # green
RED = (255, 0, 0)      # red
destroy_speed = 2      # Speed of destruction
bullet_speed = 10      # Initial velocity of bullets
msec = 45 * 1000       # Milliseconds



frame_width = 640
frame_height = 360

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
#time.sleep(1.0)




def main():
    run = True                      # Cycle control parameters
    start = False                   # Game start parameters
    paussed = True                  # Pause flag parameters
    clock = pygame.time.Clock()     # Frame rate control
    delay = 100                     # Delay Settings
    score = 0                       # Set Score
    grade1 = 50                     # Small enemy aircraft score
    grade2 = 300                    # Medium-sized enemy aircraft score
    grade3 = 600                    # Large enemy aircraft score
    level = 1                       # Grade Level
    life_num = 3                    # Number of lives
    # Font Settings
    score_font = pygame.font.Font("font/font.ttf",35)
    game_over_font = pygame.font.Font("font/font.ttf",30)
    # Set the "Game Ready" image wizard
    game_loadings = list()
    game_loadings_index = 0
    game_loadings_num = 3
    game_loadings.append(game_loading1)
    game_loadings.append(game_loading2)
    game_loadings.append(game_loading3)
    # Background music playing
    bg_music.play(-1)
    # Instantiate our aircraft
    hero = plane.Plane(bg_size)
    # Instantiated enemy units
    enemies = pygame.sprite.Group()
    # Instantiated small type 2 enemy aircraft
    mini_enemise = pygame.sprite.Group()
    add_enemies('mini',bg_size,mini_enemise,enemies,16)
    #Instantiated medium enemy aircraft
    medium_enemise = pygame.sprite.Group()
    add_enemies('medium', bg_size, medium_enemise, enemies, 8)
    # Instantiation of large enemy aircraft
    large_enemise = pygame.sprite.Group()
    add_enemies('large',bg_size,large_enemise,enemies,4)
    # Instantiated Bullets
    bullets = []
    # Bullet index subscript
    bullets_index = 0
    # Number of bullets
    bullet_num = 4
    # Number of shells
    bomb_num = 3
    for i in range(bullet_num):
        bullets.append(bullet.Bullet(hero.rect.midtop))
    # Instantiated replenishment
    bomb_supply = supply.Bomb_Supply(bg_size)
    # Set a timed event
    supply_time =  USEREVENT
    pygame.time.set_timer(supply_time, msec)




    isOpen = 0
    countK = 0
    bombG = 1
    clearcd = 0
    # Game Loop
    while run:
        ##
        acc = sensor.linear_acceleration
        if not acc[0]:
            acc = [0,0,0]
        
        countK+=1
        if bombG == 0:
            clearcd += 1
        if clearcd >= 100:
            bombG = 1
            clearcd = 0
        # print(acc)
        f = open('bomb')
        a = f.read()

        if (acc[2] <-6 or a == '0') and bombG == 1:
            bombG = 0
            if bomb_num:
                print(bomb_num)
                bomb_num -= 1
                for each in enemies:
                    if each.rect.bottom > 0:
                        each.survival = False
            f = open('bomb','w')
            f.write('1')
        elif acc[1]>6 and bombG == 1 and bomb_num<3:
            bomb_num += 1
            bombG = 0
        
        for event in pygame.event.get():
            # Top right corner off button detection
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Mouse click detection
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Game Start
                    start = True
                if event.button == 1 and quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paussed = not paussed
                    if not paussed:
                        pygame.time.set_timer(supply_time, 0)
                        # Pause Sound
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(supply_time, msec)
                        # Restore sound effects
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                if event.button == 1 and game_restart_rect.collidepoint(event.pos):
                    # Restart
                    main()


            # Mouse placement coordinate detection
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paussed:
                        paused_image = game_resume_pressed
                    else:
                        paused_image = game_pause_pressed
                else:
                    if paussed:
                        paused_image = game_resume_nor
                    else:
                        paused_image = game_pause_nor
            # Keyboard key detection
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        enemy3_down_sound.play()
                        # Press space to destroy all enemy planes on the screen
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.survival = False
            # Timing time detection
            elif event.type == supply_time:
                bomb_supply.set_position()
                print('set_position')

        # Level up as appropriate
        if level < get_level(score) + 1:
            level += 1
            game_achievement_sound.play()
            # Increase the number of enemy planes in a certain batch
            add_enemies('mini', bg_size, mini_enemise, enemies, 3)
            add_enemies('medium', bg_size, medium_enemise, enemies, 2)
            add_enemies('large', bg_size, large_enemise, enemies, 1)
            # Boost the speed of small enemy aircraft
            up_speed(mini_enemise, 1)
            print('Level Up')
            if not (level % 2) and bullet_num < 6:
                # Add one round for every two boosts of enemy aircraft, capped at 6
                print('Increase in the number of bullets')
                bullet_num += 1
                bullets.append(bullet.Bullet(hero.rect.midtop))

        # Game Start
        if start:
            screen.blit(game_quit,quit_rect)
            # Drawing the background image
            screen.blit(background, (0, 0))
            
            # Plotting fractions
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (50,5))

            ##quit
            screen.blit(game_quit,quit_rect)
            # Drawing bombs
            bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image,(10,height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))
            # Draw the pause button
            screen.blit(paused_image, paused_rect)

            if life_num and paussed:
                # Collision Detection
                enemies_down = pygame.sprite.spritecollide(hero,enemies, False, pygame.sprite.collide_mask)
                if enemies_down:
                    hero.survival = False
                    for enemy_down in enemies_down:
                        enemy_down.survival = False

                # Firing bullets
                if not(delay % bullet_speed):
                    bullets[bullets_index].set_position(hero.rect.midtop)
                    bullets_index = (bullets_index + 1) % bullet_num

                # Bullet collision detection
                for b in bullets:
                    if b.survival:
                        b.move()
                        screen.blit(b.bullet, b.rect)
                        enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                        # hit
                        if enemy_hit:
                            b.survival = False
                            for e in enemy_hit:
                                if e in medium_enemise or e in large_enemise:
                                    e.hp -= 1
                                    e.hit = True
                                    if e.hp == 0: e.survival = False
                                else: e.survival = False

                # Mapping bomb replenishment
                if bomb_supply.survival:
                    bomb_supply.move()
                    screen.blit(bomb_supply.bomb, bomb_supply.rect)
                    # Bomb resupply collision detection
                    if pygame.sprite.collide_mask(bomb_supply, hero):
                        if bomb_num < 3:
                            bomb_num += 1
                        # Destroy bomb resupply
                        bomb_supply.survival = False

                # Mapping small enemy aircraft
                for mini_enemy in mini_enemise:
                    # Survival judgment
                    if mini_enemy.survival:
                        # Small enemy aircraft movement
                        mini_enemy.move()
                        # Drawing images
                        screen.blit(mini_enemy.enemy,mini_enemy.rect)
                    else:
                        # Destroy enemy aircraft
                        if not(delay % destroy_speed):
                            if mini_enemy.spirits_index == 0:
                                # Play enemy aircraft destruction sound
                                enemy1_down_sound.play()
                            # Draw the destruction animation
                            screen.blit(mini_enemy.death_spirits[mini_enemy.spirits_index], mini_enemy.rect)
                            mini_enemy.spirits_index = mini_enemy.spirits_index + 1
                            if mini_enemy.spirits_index == 4:
                                # Increase the score
                                score += grade1
                                # Reset enemy aircraft
                                mini_enemy.set_position()

                # Mapping of medium-sized enemy aircraft
                for medium_enemy in medium_enemise:
                    # Survival judgment
                    if medium_enemy.survival:
                        # Medium-sized enemy aircraft movement
                        medium_enemy.move()
                        # Judgment of being hit
                        if medium_enemy.hit:
                            screen.blit(medium_enemy.enemy_hit,medium_enemy.rect)
                            medium_enemy.hit = False
                        else:
                            # Drawing images
                            screen.blit(medium_enemy.enemy,medium_enemy.rect)
                        # Drawing blood slots
                        draw_start = (medium_enemy.rect.left, medium_enemy.rect.top - 5)
                        draw_end = (medium_enemy.rect.right, medium_enemy.rect.top - 5)
                        pygame.draw.line(screen, RED, draw_start, draw_end, 2)
                        # Calculate remaining blood volume set_position
                        surplus_hp = medium_enemy.hp / enemy.MediumEnemy.hp
                        draw_end = (medium_enemy.rect.left + medium_enemy.rect.width * surplus_hp, medium_enemy.rect.top - 5)
                        pygame.draw.line(screen, GREEN, draw_start, draw_end, 2)
                    else:
                        # Destroy enemy aircraft
                        if not(delay % destroy_speed):
                            if medium_enemy.spirits_index == 0:
                                # Play enemy aircraft destruction sound
                                enemy2_down_sound.play()
                            # Draw the destruction animation
                            screen.blit(medium_enemy.death_spirits[medium_enemy.spirits_index], medium_enemy.rect)
                            medium_enemy.spirits_index = medium_enemy.spirits_index + 1
                            if medium_enemy.spirits_index == 4:
                                # Increase the score
                                score += grade2
                                # Reset enemy aircraft
                                medium_enemy.set_position()


                # Mapping large enemy aircraft
                for large_enemy in large_enemise:
                    # Survival judgment
                    if large_enemy.survival:
                        # Large enemy aircraft movement
                        large_enemy.move()
                        # Judgment of being hit
                        if large_enemy.hit:
                            screen.blit(large_enemy.enemy_hit,large_enemy.rect)
                            large_enemy.hit = False
                        else:
                            # Plotting enemy aircraft graphics
                            screen.blit(large_enemy.enemy,large_enemy.rect)
                        # Drawing blood slots
                        draw_start = (large_enemy.rect.left,large_enemy.rect.top - 5)
                        draw_end = (large_enemy.rect.right,large_enemy.rect.top - 5)
                        pygame.draw.line(screen,RED, draw_start, draw_end,2)
                        # Calculate remaining blood volume
                        surplus_hp = large_enemy.hp / enemy.LargeEnemy.hp
                        draw_end = (large_enemy.rect.left + large_enemy.rect.width * surplus_hp, large_enemy.rect.top - 5)
                        pygame.draw.line(screen,GREEN, draw_start, draw_end, 2)
                        if large_enemy.rect.bottom > -50:
                            # Play the sound of enemy aircraft flying
                            enemy3_out_sound.play(-1)
                    else:
                        # Destroy enemy aircraft
                        if not(delay % destroy_speed):
                            if large_enemy.spirits_index == 0:
                                # Play enemy aircraft destruction sound
                                enemy3_down_sound.play()
                            # Draw the destruction animation
                            screen.blit(large_enemy.death_spirits[large_enemy.spirits_index],large_enemy.rect)
                            large_enemy.spirits_index = large_enemy.spirits_index + 1
                            if large_enemy.spirits_index == 6:
                                # Increase the score
                                score += grade3
                                # Turn off sound effects
                                enemy3_out_sound.stop()
                                # Reset enemy aircraft
                                large_enemy.set_position()

                # Drawing aircraft images
                if hero.survival:
                    # Detect the keyboard and control the movement of our aircraft
                    hero.move()
                    screen.blit(hero.plane,hero.rect)
                else:
                    enemy2_down_sound.play()
                    if not(delay % destroy_speed):
                        # Draw the destruction animation
                        screen.blit(hero.death_spirits[hero.spirits_index], hero.rect)
                        hero.spirits_index = hero.spirits_index + 1
                        if hero.spirits_index == 3:
                            print("Code Over")
                            life_num -= 1
                            # Resetting the fighter
                            print('set_hero')
                            hero.set_position()

                # Plotting the number of aircraft lives
                if life_num:
                    for i in range(life_num):
                        life_left = width - 10 - (i + 1) * life_rect.width
                        life_top = height - 10 - life_rect.height
                        screen.blit(life_image, (life_left, life_top))
            elif life_num == 0:
                # Read the highest score ever
                highest_score = int()
                # Determine if the record file exists, and create it if it does not.
                if not os.path.exists("score.txt"):
                    #os.mknod("score.txt")
                    highest_score = 0
                else:
                    # The file exists to be read
                    with open("score.txt","r") as f:
                        highest_score = int(f.read())
                        f.close()
                # If the record is broken, the score is rewritten
                if score > highest_score:
                    with open("score.txt","w+") as f:
                        f.write(str(score))
                        f.close()
                # Draw the game end background image
                screen.blit(game_over, (0, 0))
                # Plotting the final score
                if score < highest_score:
                    game_over_text = game_over_font.render("%s" % str(score), True, WHITE)
                else:
                    game_over_text = game_over_font.render("%s" % str(score), True, WHITE)
                over_text_width = str(score).__len__() + 50
                screen.blit(game_over_text, ((width - over_text_width) / 2, height / 2 ))
                # Mapping history
                game_over_text = game_over_font.render("%s" % "Highest Score: " + str(highest_score), True, WHITE)
                over_text_width = (str(highest_score).__len__() + 15) * 12
                screen.blit(game_over_text, ((width - over_text_width) / 2, height / 2 + 60))
                # Drawing the Restart button
                screen.blit(game_restart, game_restart_rect)
                game_player=pygame.image.load("1.jpg").convert_alpha()
                game_player = pygame.transform.rotozoom(game_player, 0, 0.2)
                game_player_rect=game_player.get_rect()
                game_player_rect.left,game_player_rect.top=200,20
                screen.blit(game_player, game_player_rect)

                # Stop the background music
                pygame.mixer.music.pause()
                # Stop Sound
                pygame.mixer.pause()
            else:
                # Drawing the game stop sign map
                screen.blit(game_stop, ((width - game_stop_rect.width) / 2, (height - game_stop_rect.height) / 2))
            
        else:
            # Drawing the background image
            screen.blit(background, (0, 0))
            # Draw the name of the game
            screen.blit(game_start, (0, 0))
            
            # Drawing loading images
            game_loading_X = (width - game_loading_rect.width) / 2
            game_loading_Y = (height - game_loading_rect.height) / 2 + 50
            screen.blit(game_loadings[game_loadings_index], (game_loading_X, game_loading_Y))
            # loading Subscript change
            if not (delay % 8):
                game_loadings_index = (game_loadings_index + 1) % game_loadings_num

        # loading Subscript change
        pygame.display.flip()
        # Frame Rate Settings
        clock.tick(30)
        delay -= 1
        if delay == 0:delay = 10


if __name__ == '__main__':
    main()
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()