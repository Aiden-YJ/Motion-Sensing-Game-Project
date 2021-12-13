import pygame
from pygame.locals import *
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
import time
import board
import adafruit_bno055
import serial
import busio

i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)



class Plane(pygame.sprite.Sprite):
    def __init__(self,bg_size):

        pygame.sprite.Sprite.__init__(self)
        self.plane1 = pygame.image.load("images/plane1.png").convert_alpha()
        self.plane1 = pygame.transform.rotozoom(self.plane1, 0, 0.25)
        self.plane2 = pygame.image.load("images/plane2.png").convert_alpha()
        self.plane2 = pygame.transform.rotozoom(self.plane2, 0, 0.25)

        self.plane = self.plane1
        self.mask = pygame.mask.from_surface(self.plane)
        self.death_spirits = list()
        self.spirit1 = pygame.image.load("images/plane_blowup_n1.png").convert_alpha()
        self.spirit1 = pygame.transform.rotozoom(self.spirit1, 0, 0.25)
        self.spirit2 = pygame.image.load("images/plane_blowup_n2.png").convert_alpha()
        self.spirit2 = pygame.transform.rotozoom(self.spirit2, 0, 0.25)
        self.spirit3 = pygame.image.load("images/plane_blowup_n3.png").convert_alpha()
        self.spirit3 = pygame.transform.rotozoom(self.spirit3, 0, 0.25)
        self.death_spirits.extend([self.spirit1, self.spirit2, self.spirit3])
        self.spirits_index = 0
        self.swich = True
        self.count = 3
        self.scaler = self.count
        self.rect = self.plane1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 5
        self.eurInitial = sensor.euler
        self.set_position()
        self.history = [self.rect.left,self.rect.right,self.rect.top,self.rect.bottom]


    def moveUp(self):
        eur = sensor.euler
        if not eur[0]:
            eur = [0,0,0]
        if self.rect.top > 0:
            self.rect.top += max((eur[2] - self.eurInitial[2])/10,-5)
        else:
            self.rect.top = 0
            print('top')
            #self.rect.top += 5
    def moveDown(self):
        eur = sensor.euler
        if not eur[0]:
            eur = [0,0,0]
        if self.rect.bottom < self.height - 20:
            self.rect.bottom += min((eur[2] - self.eurInitial[2])/10,5)
        else:
            print('buttom')
            self.rect.bottom =self.height - 20
    def moveLeft(self):
        eur = sensor.euler
        if not eur[0]:
            eur = [0,0,0]
        if self.rect.left > 0:
            self.rect.left += max((eur[1] - self.eurInitial[1])/10,-5)
        else:
            print('left')
            self.rect.left = 0
    def moveRight(self):
        eur = sensor.euler
        if not eur[0]:
            eur = [0,0,0]
        if self.rect.right < self.width:
            self.rect.right += min((eur[1] - self.eurInitial[1])/10,5)
        else:
            print('right')
            self.rect.right = self.width
    def move(self):
    
        acc = sensor.acceleration
        eur = sensor.euler
        if not eur[0]:
            eur = [0,0,0]
        # if not eur or eur ==[]:
        #     eur = [0,0,0]
        self.key_pressed = pygame.key.get_pressed()
        if GPIO.input(27) == 0 or eur[2] - self.eurInitial[2]<= 0:
            self.moveUp()
            #print('hhh')
        if GPIO.input(23) == 0 or eur[2] - self.eurInitial[2] > 0:
            self.moveDown()
        if GPIO.input(22) == 0 or eur[1] - self.eurInitial[1] <= 0:
	        self.moveLeft()
        if GPIO.input(17) == 0 or eur[1] - self.eurInitial[1] > 0:
            self.moveRight() 
        # if self.key_pressed[K_w] or self.key_pressed[K_UP]:
        #     self.moveUp()
        # if self.key_pressed[K_s] or self.key_pressed[K_DOWN]:
        #     self.moveDown()
        # if self.key_pressed[K_a] or self.key_pressed[K_LEFT]:
        #     self.moveLeft()
        # if self.key_pressed[K_d] or self.key_pressed[K_RIGHT]:
        #     self.moveRight()
        # 
        if self.swich:
            self.plane = self.plane1
            #print('ss')
        else:
            #print('ss')
            self.plane = self.plane2
        if self.scaler == 0:
            self.swich = not self.swich
            self.scaler = self.count
        self.scaler -= 1
        #print(self.history,self.rect)
        if self.rect.left-self.history[0] >20 or self.rect.left - self.history[0] < - 20 or \
            self.rect.top-self.history[2] >20 or self.rect.top-self.history[2] < - 20 or\
            self.rect.right-self.history[1] >20 or self.rect.right-self.history[1] < - 20 or\
            self.rect.bottom-self.history[3] >20 or self.rect.bottom-self.history[3] < - 20:
            self.rect.left,self.rect.right,self.rect.top,self.rect.bottom = self.history[0], \
                self.history[1],self.history[2],self.history[3]
            print('!!!')
        self.history = [self.rect.left,self.rect.right,self.rect.top,self.rect.bottom]
        
        
    def set_position(self):
        self.survival = True
        self.spirits_index = 0
        self.rect.left = (self.width - self.rect.width) / 2
        self.rect.top = self.height - self.rect.height - 20
        self.history = [self.rect.left,self.rect.right,self.rect.top,self.rect.bottom]
    
