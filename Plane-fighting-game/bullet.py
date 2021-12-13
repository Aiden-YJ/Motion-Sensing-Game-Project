import pygame
class Bullet(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.bullet=pygame.image.load("images/bullet.png")
        self.bullet = pygame.transform.rotozoom(self.bullet, 0, 0.25)
        self.mask=pygame.mask.from_surface(self.bullet)
        self.rect=self.bullet.get_rect()
        self.set_position(position)
        self.speed=15
    def move(self):
        self.rect.top-=self.speed
        if self.rect.top<0:
            self.active=False
    def set_position(self,position):
        self.survival=True
        self.rect.left,self.rect.top=position