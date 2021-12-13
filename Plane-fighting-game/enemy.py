import pygame
from random import *
#pygame.sprite.Sprite is easy to controll the game
class MiniEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        #must call sprite's construction function to perform initialization
        pygame.sprite.Sprite.__init__(self)
        #load image material：
        self.enemy1=pygame.image.load("images/enemy1.png").convert_alpha()
        self.enemy1 = pygame.transform.rotozoom(self.enemy1, 0, 0.25)

        self.enemy=self.enemy1
        #Get the area location of the enemy aircraft：
        #obtain enemy location
        self.mask=pygame.mask.from_surface(self.enemy)
        #setup death spirit：
        self.death_spirit=list()
        #load spirit material：
        self.spirit1 = pygame.image.load("images/enemy1_down1.png").convert_alpha()
        self.spirit1 = pygame.transform.rotozoom(self.spirit1, 0, 0.25)

        self.spirit2 = pygame.image.load("images/enemy1_down2.png").convert_alpha()
        self.spirit2 = pygame.transform.rotozoom(self.spirit2, 0, 0.25)

        self.spirit3 = pygame.image.load("images/enemy1_down3.png").convert_alpha()
        self.spirit3 = pygame.transform.rotozoom(self.spirit3, 0, 0.25)

        self.spirit4 = pygame.image.load("images/enemy1_down4.png").convert_alpha()
        self.spirit4 = pygame.transform.rotozoom(self.spirit4, 0, 0.25)

        #load to the spirit list：
        self.death_spirit.extend([self.spirit1,self.spirit2,self.spirit3,self.spirit4])
        #Set sprite list play subscript
        self.spirit_index=0
        #Enemy aircraft size
        self.rect=self.enemy1.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        #Enemy aircraft speed：
        self.speed=2
        #Initialization Location：
        self.set_position()
    def move(self):
        if self.rect.top<self.height:
            self.rect.top+=self.speed
        else:
            self.set_position()
    #Set the initial position of the enemy aircraft：
    def set_position(self):
        self.survival=True
        self.spirit_index=0
        self.rect.left=randint(0,self.width-self.rect.width)
        self.rect.top=randint(-3*self.height,0)

#Medium-sized enemy aircraft：
class MediumEnemy(pygame.sprite.Sprite):
    hp=5
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        #Load material
        self.enemy2=pygame.image.load("images/enemy2.png").convert_alpha()
        self.enemy2 = pygame.transform.rotozoom(self.enemy2, 0, 0.25)
        self.enemy=self.enemy2
        #Loading of hit material
        self.enemy_hit=pygame.image.load("images/enemy2_hit.png").convert_alpha()
        self.enemy_hit = pygame.transform.rotozoom(self.enemy_hit, 0, 0.25)
        #Parameters for setting whether to be hit or not
        self.hit=False
        #Get the actual position of the enemy aircraft
        self.mask=pygame.mask.from_surface(self.enemy)
        #set up the spirite：
        self.death_spirits=list()
        # self.spirit1=pygame.image.load("images/enemy2_down1.png").convert_alpha()
        # self.spirit2=pygame.image.load("images/enemy2_down2.png").convert_alpha()
        # self.spirit3=pygame.image.load("images/enemy2_down3.png").convert_alpha()
        # self.spirit4=pygame.image.load("images/enemy2_down4.png").convert_alpha()
        self.spirit1 = pygame.image.load("images/enemy2_down1.png").convert_alpha()
        self.spirit1 = pygame.transform.rotozoom(self.spirit1, 0, 0.25)

        self.spirit2 = pygame.image.load("images/enemy2_down2.png").convert_alpha()
        self.spirit2 = pygame.transform.rotozoom(self.spirit2, 0, 0.25)

        self.spirit3 = pygame.image.load("images/enemy2_down3.png").convert_alpha()
        self.spirit3 = pygame.transform.rotozoom(self.spirit3, 0, 0.25)

        self.spirit4 = pygame.image.load("images/enemy2_down4.png").convert_alpha()
        self.spirit4 = pygame.transform.rotozoom(self.spirit4, 0, 0.25)

        self.death_spirits.extend([self.spirit1,self.spirit2,self.spirit3,self.spirit4])
        self.spirits_index=0
        self.rect=self.enemy2.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        self.speed=1.5
        self.set_position()
    def move(self):
        if self.rect.top<self.height:
            self.rect.top+=self.speed
        else:
            self.set_position()
    def set_position(self):
        self.survival=True
        self.hp=MediumEnemy.hp
        self.spirits_index=0
        self.rect.left=randint(0,self.width-self.rect.width)
        self.rect.top=randint(-5*self.height,-self.height)

# Large enemy aircraft
class LargeEnemy(pygame.sprite.Sprite):
    hp = 15
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.enemy3_n1 = pygame.image.load("images/enemy3_n1.png").convert_alpha()
        self.enemy3_n1 = pygame.transform.rotozoom(self.enemy3_n1, 0, 0.25)

        self.enemy3_n2 = pygame.image.load("images/enemy3_n2.png").convert_alpha()
        self.enemy3_n2 = pygame.transform.rotozoom(self.enemy3_n2, 0, 0.25)

        self.enemy = self.enemy3_n1
        self.enemy_hit = pygame.image.load("images/enemy3_hit.png").convert_alpha()
        self.enemy_hit = pygame.transform.rotozoom(self.enemy_hit, 0, 0.25)

        self.hit = False
        self.mask = pygame.mask.from_surface(self.enemy)
        self.death_spirits = list()
        self.spirit1 = pygame.image.load("images/enemy3_down1.png").convert_alpha()
        self.spirit1 = pygame.transform.rotozoom(self.spirit1, 0, 0.25)

        self.spirit2 = pygame.image.load("images/enemy3_down2.png").convert_alpha()
        self.spirit2 = pygame.transform.rotozoom(self.spirit2, 0, 0.25)

        self.spirit3 = pygame.image.load("images/enemy3_down3.png").convert_alpha()
        self.spirit3 = pygame.transform.rotozoom(self.spirit3, 0, 0.25)

        self.spirit4 = pygame.image.load("images/enemy3_down4.png").convert_alpha()
        self.spirit4 = pygame.transform.rotozoom(self.spirit4, 0, 0.25)

        self.spirit5 = pygame.image.load("images/enemy3_down5.png").convert_alpha()
        self.spirit5 = pygame.transform.rotozoom(self.spirit5, 0, 0.25)

        self.spirit6 = pygame.image.load("images/enemy3_down6.png").convert_alpha()
        self.spirit6 = pygame.transform.rotozoom(self.spirit6, 0, 0.25)

        self.death_spirits.extend([self.spirit1, self.spirit2, self.spirit3, self.spirit4, self.spirit5, self.spirit6])
        self.spirits_index = 0
        self.switch = True
        self.count = 5
        self.scaler = self.count
        self.rect = self.enemy3_n1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1#
        self.set_position()
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.set_position()
        if self.switch:
            self.enemy = self.enemy3_n1
        else:
            self.enemy = self.enemy3_n2
        # Counter Judgment
        if self.scaler == 0:
            self.switch = not self.switch
            self.scaler = self.count
        # Counter counting
        self.scaler -= 1

    def set_position(self):
        self.survival = True
        self.hp = LargeEnemy.hp
        self.spirits_index = 0
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-6 * self.height, -3 * self.height)

def add_enemies(size,bg_size,group1,group2,num):
    for i in range(num):
        enemy=MediumEnemy(bg_size)
        if size=='mimi':
            enemy=MiniEnemy(bg_size)
        if size=='medium':
            enemy=MediumEnemy(bg_size)
        if size=='large':
            enemy=LargeEnemy(bg_size)
        group1.add(enemy)
        group2.add(enemy)

#Cue enemy aircraft speed
def up_speed(group,index):
    for each in group:
        each.speed+=index

def get_level(num):
    result=0
    if num>=4092:
        num2=1
        while num2<num:
            num2*=2
            result+=1
        result-=12
    return result