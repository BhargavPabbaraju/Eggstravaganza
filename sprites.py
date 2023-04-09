
import pygame as pg
from random import randint as rand
from settings import *
from math import pi,atan2,degrees
from pygame.math import Vector2 as vec2


class Egg(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.width = 64
        self.height = 64
        self.x = rand(self.width,WIDTH-self.width)
        self.y = -self.height
        self.vel = rand(1,8)/10
        self.image = pg.Surface((self.width,self.height))
        self.image.fill((rand(0,255),rand(0,255),rand(0,255)))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.game = game
        self.start = pg.time.get_ticks()

        
    
    def update(self):
        if self.y > HEIGHT - self.height*2:
            #Crash egg
            self.game.currentEggs -=1
            self.kill()
        
      
       
        t = (pg.time.get_ticks()-self.start)/200
        self.y+=self.vel*t
            
        
        self.rect.y = self.y




class Bubble(pg.sprite.Sprite):
    def __init__(self,game,pos=None,vec=None):
        super().__init__()
        self.width = 64
        self.height = 64
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)

       
        #self.image.fill((rand(0,255),rand(0,255),rand(0,255)))
        self.pos = pos
        self.vec = vec
        pg.draw.circle(self.image,(0,255,0),(self.width//2,self.height//2),self.width//2)

        self.rect = self.image.get_rect()
        if not pos:
            self.rect.x = WIDTH//2
            self.rect.bottom = HEIGHT-self.height//4 + 8
        else:
            self.rect.center = self.pos
        #self.rect.y = self.y
        self.game = game
        self.start = pg.time.get_ticks()



class Arrow(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.width = 64*3
        self.height = 64*3
        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)

       
        #self.image.fill((rand(0,255),rand(0,255),rand(0,255)))
        
        

        self.rect = self.image.get_rect()
        

        pg.draw.line(self.image,(255,0,0),(self.width//2,0),(self.width//2,self.height//3),width=4)
        #self.rect.y = self.y
        self.game = game
        self.start = self.rect.center
        
        self.last_update = pg.time.get_ticks()
        self.update_thres = 100
        self.angle = 0
        self.origImage = self.image
        self.origRect = self.rect
        self.rect.center = self.game.shooter.rect.center
        self.direction = vec2(WIDTH//2,0)
    

        

    

    def update(self):
        

        
        self.direction = vec2(pg.mouse.get_pos())-vec2(self.origRect.center)
        self.angle = self.direction.angle_to((0,-1))

        self.image = pg.transform.rotate(self.origImage,self.angle)
        self.rect = self.image.get_rect(center=self.origRect.center)
    
