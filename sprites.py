
import pygame as pg
from random import randint as rand
from settings import *
from math import sin,cos
from pygame.math import Vector2 as vec2


class Spritesheet:
    def __init__(self,file):
        self.sheet = pg.image.load('./Images/%s'%file).convert_alpha()
    
    def get_image(self,r,c,w,h,scale=1):
        surf = pg.Surface((w,h),pg.SRCALPHA)
        surf.blit(self.sheet,(0,0),[r*w,c*h,w,h])
        if scale!=1:
            surf = pg.transform.scale(surf,scale)
        
        return surf
        

sheets={}
bubbleColors = [[
    #00
    [(162,235,242),(121,215,234)],
    #01
    [(195,242,162),(130,209,137)],
    #02
    [(210,198,250),(167,145,2375)],
]]

class Egg(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        if 'egg' not in sheets:
            sheets['egg'] = Spritesheet('eggs.png')
        self.width = 64-8
        self.height = 64-8
        self.x = rand(BOUNDARY+self.width,WIDTH-BOUNDARY-self.width)
        self.y = -self.height
        self.vel = rand(1,8)/10
        #self.image = pg.Surface((self.width,self.height))
        #self.image.fill((rand(0,255),rand(0,255),rand(0,255)))
        self.image = sheets['egg'].get_image(rand(0,3),rand(0,2),self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.game = game
        self.start = pg.time.get_ticks()

        
    
    def update(self):
        if self.y > HEIGHT - BOUNDARY:
            #Crash egg
            self.game.currentEggs -=1
            self.kill()
        
      
       
        t = (pg.time.get_ticks()-self.start)/200
        self.y+=self.vel*t
            
        
        self.rect.y = self.y




class Bubble(pg.sprite.Sprite):
    def __init__(self,game,pos=None,vec=None,image=None):
        super().__init__()
        self.width = 64
        self.height = 64
       

        self.image = pg.Surface((self.width,self.height),pg.SRCALPHA)
        if 'bubble' not in sheets:
            sheets['bubble'] = Spritesheet('bubbles.png')

        if image:
            self.image = image
        else:
            self.change_image()
        #self.image.fill((rand(0,255),rand(0,255),rand(0,255)))
        self.pos = pos
        self.vec = vec
        #pg.draw.circle(self.image,color,(self.width//2,self.height//2),self.width//2)

        self.rect = self.image.get_rect()
        
        self.rect.x = WIDTH//2
        self.rect.bottom = HEIGHT-self.height//4 + 8
        self.pos = self.rect.center
        if self.vec:
            self.rect.x+= self.vec.x*64*2 +16
            self.rect.y+= self.vec.y*64*2 +16
        
        
            
        #self.rect.y = self.y
        self.game = game
        self.start = pg.time.get_ticks()
        self.update_thres = 100
        self.vel = rand(1,20)/10
    
    def change_image(self):
        self.image = sheets['bubble'].get_image(rand(0,2),0,self.width,self.height)
    
    def update(self):
        now = pg.time.get_ticks()
        t = (pg.time.get_ticks()-self.start)/200
        if self.vec:
            self.rect.x+= self.vec.x*self.vel*t
            self.rect.y+= self.vec.y*self.vel*t
          
        
        if self.rect.x<=BOUNDARY or self.rect.y <= 0 or self.rect.x>=WIDTH-BOUNDARY or self.rect.y>=HEIGHT:
            self.kill()



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
        self.position = (WIDTH//2,HEIGHT-self.height*2)

        

    

    def update(self):
        

        
        self.direction = vec2(pg.mouse.get_pos())-vec2(self.origRect.center)
        self.angle = self.direction.angle_to((0,-1))

        self.image = pg.transform.rotate(self.origImage,self.angle)
        self.rect = self.image.get_rect(center=self.origRect.center)
        self.direction = self.direction.normalize()
        


class Particle(pg.sprite.Sprite):
    def __init__(self,pos,radius=rand(2,64),color=(rand(0,255),rand(0,255),rand(0,255))):
        super().__init__()
        self.radius = radius
        self.image = pg.Surface((self.radius*2,self.radius*2),pg.SRCALPHA)
        pg.draw.circle(self.image,color,(0,0),self.radius)
        self.pos = pos
        self.vec = vec2()
    

    def update(self):
        pass
        
